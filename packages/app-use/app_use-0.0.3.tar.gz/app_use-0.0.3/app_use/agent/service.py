import asyncio
import gc
import logging
import os
import re
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeVar

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
	BaseMessage,
	HumanMessage,
	SystemMessage,
)
from pydantic import ValidationError

from app_use.agent.gif import create_history_gif
from app_use.agent.memory.service import Memory
from app_use.agent.memory.views import MemoryConfig
from app_use.agent.message_manager.service import MessageManager, MessageManagerSettings
from app_use.agent.message_manager.utils import (
	extract_json_from_model_output,
	save_conversation,
)
from app_use.agent.prompts import PlannerPrompt, SystemPrompt
from app_use.agent.views import (
	REQUIRED_LLM_API_ENV_VARS,
	ActionResult,
	AgentBrain,
	AgentError,
	AgentHistory,
	AgentHistoryList,
	AgentOutput,
	AgentSettings,
	AgentState,
	AgentStepInfo,
	AppStateHistory,
	StepMetadata,
	ToolCallingMethod,
)
from app_use.app.app import App
from app_use.controller.service import Controller

load_dotenv()
logger = logging.getLogger(__name__)

SKIP_LLM_API_KEY_VERIFICATION = os.environ.get('SKIP_LLM_API_KEY_VERIFICATION', 'false').lower()[0] in 'ty1'


def log_response(response: AgentOutput) -> None:
	"""Utility function to log the model's response."""

	if 'Success' in response.current_state.evaluation_previous_goal:
		emoji = '👍'
	elif 'Failed' in response.current_state.evaluation_previous_goal:
		emoji = '⚠'
	else:
		emoji = '🤷'

	logger.info(f'{emoji} Eval: {response.current_state.evaluation_previous_goal}')
	logger.info(f'🧠 Memory: {response.current_state.memory}')
	logger.info(f'🎯 Next goal: {response.current_state.next_goal}')
	for i, action in enumerate(response.action):
		logger.info(f'🛠️  Action {i + 1}/{len(response.action)}: {action.model_dump_json(exclude_unset=True)}')


Context = TypeVar('Context')

AgentHookFunc = Callable[['Agent'], Awaitable[None]]


class Agent(Generic[Context]):
	def __init__(
		self,
		task: str,
		llm: BaseChatModel,
		app: App,
		# Optional parameters
		controller: Controller[Context] = None,
		# Initial agent run parameters
		sensitive_data: dict[str, str] | None = None,
		initial_actions: list[dict[str, dict[str, Any]]] | None = None,
		# Agent settings
		use_vision: bool = True,
		save_conversation_path: str | None = None,
		save_conversation_path_encoding: str | None = 'utf-8',
		max_failures: int = 3,
		retry_delay: int = 10,
		override_system_message: str | None = None,
		extend_system_message: str | None = None,
		max_input_tokens: int = 128000,
		validate_output: bool = False,
		message_context: str | None = None,
		max_actions_per_step: int = 10,
		tool_calling_method: ToolCallingMethod | None = 'auto',
		page_extraction_llm: BaseChatModel | None = None,
		planner_llm: BaseChatModel | None = None,
		planner_interval: int = 1,
		is_planner_reasoning: bool = False,
		extend_planner_system_message: str | None = None,
		injected_agent_state: AgentState | None = None,
		context: Context | None = None,
		enable_memory: bool = True,
		memory_config: MemoryConfig | None = None,
		generate_gif: bool | str = False,
	):
		if page_extraction_llm is None:
			page_extraction_llm = llm

		# Generate unique IDs for this agent session and task early
		self.session_id: str = str(uuid.uuid4())
		self.task_id: str = str(uuid.uuid4())

		# Core components
		self.task = task
		self.llm = llm
		self.app = app
		self.controller = controller or Controller()
		self.sensitive_data = sensitive_data

		self.settings = AgentSettings(
			use_vision=use_vision,
			save_conversation_path=save_conversation_path,
			save_conversation_path_encoding=save_conversation_path_encoding,
			max_failures=max_failures,
			retry_delay=retry_delay,
			override_system_message=override_system_message,
			extend_system_message=extend_system_message,
			max_input_tokens=max_input_tokens,
			validate_output=validate_output,
			message_context=message_context,
			max_actions_per_step=max_actions_per_step,
			tool_calling_method=tool_calling_method,
			page_extraction_llm=page_extraction_llm,
			planner_llm=planner_llm,
			planner_interval=planner_interval,
			is_planner_reasoning=is_planner_reasoning,
			extend_planner_system_prompt=extend_planner_system_message,
			generate_gif=generate_gif,
		)

		# Memory settings
		self.enable_memory = enable_memory
		self.memory_config = memory_config

		# Initialize state
		self.state = injected_agent_state or AgentState()

		# Action setup
		self._setup_action_models()

		# Model setup
		self._set_model_names()
		self.tool_calling_method = self._set_tool_calling_method()

		# Verify we can connect to the LLM
		self._verify_llm_connection()

		# Initialize available actions for system prompt
		self.unfiltered_actions = self.controller.registry.get_prompt_description()

		# Set message context and initialize message manager
		self.settings.message_context = self._set_message_context()

		# Initialize message manager with state
		system_message = self._get_system_message()

		self._message_manager = MessageManager(
			task=task,
			system_message=system_message,
			settings=MessageManagerSettings(
				max_input_tokens=self.settings.max_input_tokens,
				message_context=self.settings.message_context,
				sensitive_data=sensitive_data,
			),
			state=self.state.message_manager_state,
		)

		# Initialize memory if enabled
		if self.enable_memory:
			try:
				self.memory = Memory(
					message_manager=self._message_manager,
					llm=self.llm,
					config=self.memory_config,
				)
			except ImportError:
				logger.warning(
					'⚠️ Agent(enable_memory=True) is set but missing some required packages, install and re-run to use memory features: pip install app-use[memory]'
				)
				self.memory = None
				self.enable_memory = False
		else:
			self.memory = None

		# Convert initial actions
		self.initial_actions = self._convert_initial_actions(initial_actions) if initial_actions else None

		# Context
		self.context: Context | None = context

		logger.info(
			f'🧠 Starting an app-use agent with base_model={self.model_name}'
			f'{" +tools" if self.tool_calling_method == "function_calling" else ""}'
			f'{" +rawtools" if self.tool_calling_method == "raw" else ""}'
			f'{" +vision" if self.settings.use_vision else ""}'
			f'{" +memory" if self.enable_memory else ""}'
			f' extraction_model={getattr(self.settings.page_extraction_llm, "model_name", None)}'
			f'{f" planner_model={self.planner_model_name}" if self.planner_model_name else ""}'
			f'{" +reasoning" if self.settings.is_planner_reasoning else ""}'
		)

		self._message_manager = MessageManager(
			task=task,
			system_message=system_message,
			settings=MessageManagerSettings(
				max_input_tokens=self.settings.max_input_tokens,
				include_attributes=self.settings.include_attributes if hasattr(self.settings, 'include_attributes') else [],
				message_context=self.settings.message_context,
				sensitive_data=sensitive_data,
				available_file_paths=None,
			),
			state=self.state.message_manager_state,
		)

		self.initial_actions = self._convert_initial_actions(initial_actions) if initial_actions else None

		# Context
		self.context = context

	def _set_message_context(self) -> str | None:
		"""Set the message context for the agent."""
		if self.tool_calling_method == 'raw':
			# For raw tool calling, only include actions with no filters initially
			if self.settings.message_context:
				self.settings.message_context += f'\n\nAvailable actions: {self.unfiltered_actions}'
			else:
				self.settings.message_context = f'Available actions: {self.unfiltered_actions}'
		return self.settings.message_context

	def _get_system_message(self) -> SystemMessage:
		"""Generate the system message for the agent using SystemPrompt"""
		action_description = self.controller.registry.get_prompt_description()
		system_prompt = SystemPrompt(
			action_description=action_description,
			max_actions_per_step=self.settings.max_actions_per_step,
			override_system_message=self.settings.override_system_message,
			extend_system_message=self.settings.extend_system_message,
		)
		return system_prompt.get_system_message()

	def _set_model_names(self) -> None:
		"""Set model names based on LLM attributes."""
		self.chat_model_library = self.llm.__class__.__name__
		self.model_name = 'Unknown'
		if hasattr(self.llm, 'model_name'):
			model = self.llm.model_name  # type: ignore
			self.model_name = model if model is not None else 'Unknown'
		elif hasattr(self.llm, 'model'):
			model = self.llm.model  # type: ignore
			self.model_name = model if model is not None else 'Unknown'

		# Set planner model name
		if self.settings.planner_llm:
			if hasattr(self.settings.planner_llm, 'model_name'):
				self.planner_model_name = self.settings.planner_llm.model_name  # type: ignore
			elif hasattr(self.settings.planner_llm, 'model'):
				self.planner_model_name = self.settings.planner_llm.model  # type: ignore
			else:
				self.planner_model_name = 'Unknown'
		else:
			self.planner_model_name = None

	def _setup_action_models(self) -> None:
		"""Setup dynamic action models from controller's registry"""
		# Initially only include actions with no filters
		self.ActionModel = self.controller.registry.create_action_model()
		# Create output model with the dynamic actions
		self.AgentOutput = AgentOutput.type_with_custom_actions(self.ActionModel)

		# used to force the done action when max_steps is reached
		self.DoneActionModel = self.controller.registry.create_action_model(include_actions=['done'])
		self.DoneAgentOutput = AgentOutput.type_with_custom_actions(self.DoneActionModel)

	def _set_tool_calling_method(self) -> ToolCallingMethod | None:
		"""Set the tool calling method based on model type and settings."""
		tool_calling_method = self.settings.tool_calling_method
		if tool_calling_method == 'auto':
			if self.chat_model_library == 'ChatGoogleGenerativeAI':
				return None
			elif self.chat_model_library == 'ChatOpenAI':
				return 'function_calling'
			elif self.chat_model_library == 'AzureChatOpenAI':
				# Azure OpenAI API requires 'tools' parameter for GPT-4
				if 'gpt-4' in self.model_name.lower():
					return 'tools'
				else:
					return 'function_calling'
			else:
				return None
		else:
			return tool_calling_method

	async def _raise_if_stopped_or_paused(self) -> None:
		"""Utility function that raises an InterruptedError if the agent is stopped or paused."""
		if self.state.stopped or self.state.paused:
			raise InterruptedError

	async def step(self, step_info: AgentStepInfo | None = None) -> None:
		"""Execute one step of the task"""
		logger.info(f'📍 Step {self.state.n_steps}')
		model_output = None
		result: list[ActionResult] = []
		step_start_time = time.time()
		tokens = 0
		app_state = None

		try:
			# Get the current app state as AppState
			original_app_state = self.app.get_app_state()

			# Create AppStateHistory using the class method for history tracking only
			app_state = AppStateHistory.from_app_state(original_app_state)

			if self.enable_memory and self.memory and self.state.n_steps % self.memory.config.memory_interval == 0:
				self.memory.create_procedural_memory(self.state.n_steps)

			await self._raise_if_stopped_or_paused()

			# Run planner if conditions are met
			await self._run_planner(step_info)

			# Use MessageManager to add state message with app state and previous results
			self._message_manager.add_state_message(
				app_state=original_app_state,
				result=self.state.last_result,
				step_info=step_info,
				use_vision=self.settings.use_vision,
			)

			# If this is the last step, add a message to use 'done' action
			if step_info and step_info.is_last_step():
				# Add last step warning if needed
				msg = 'Now comes your last step. Use only the "done" action now. No other actions - so here your action sequence must have length 1.'
				msg += '\nIf the task is not yet fully finished as requested by the user, set success in "done" to false!'
				msg += '\nIf the task is fully finished, set success in "done" to true.'
				msg += '\nInclude everything you found out for the ultimate task in the done text.'
				logger.info('Last step finishing up')
				self._message_manager._add_message_with_tokens(HumanMessage(content=msg))

				# Force the action model to only include done action
				self.ActionModel = self.controller.registry.create_action_model(include_actions=['done'])
				self.AgentOutput = AgentOutput.type_with_custom_actions(self.ActionModel)

			# Get all messages from message manager
			input_messages = self._message_manager.get_messages()
			tokens = self._message_manager.state.history.current_tokens

			try:
				# Get the model's next action based on current state
				model_output = await self.get_next_action(input_messages)
				# Check for empty actions and handle them
				if (
					not model_output.action
					or not isinstance(model_output.action, list)
					or all(action.model_dump() == {} for action in model_output.action)
				):
					logger.warning('Model returned empty action. Retrying...')

					clarification_message = HumanMessage(
						content='You forgot to return an action. Please respond only with a valid JSON action according to the expected format.'
					)

					retry_messages = input_messages + [clarification_message]
					model_output = await self.get_next_action(retry_messages)

					if not model_output.action or all(action.model_dump() == {} for action in model_output.action):
						logger.warning('Model still returned empty after retry. Inserting safe noop action.')
						action_instance = self.ActionModel(
							done={
								'success': False,
								'text': 'No next action returned by LLM!',
							}
						)
						model_output.action = [action_instance]

				# Check again for paused/stopped state after getting model output
				await self._raise_if_stopped_or_paused()

				# Increment step counter
				self.state.n_steps += 1

				# Save conversation if path is specified
				if self.settings.save_conversation_path:
					target = self.settings.save_conversation_path + f'_{self.state.n_steps}.txt'
					save_conversation(
						input_messages,
						model_output,
						target,
						self.settings.save_conversation_path_encoding,
					)

				# Remove the last state message from history (we don't want to keep the whole state)
				self._message_manager._remove_last_state_message()

				# Add model output to message history
				self._message_manager.add_model_output(model_output)
			except asyncio.CancelledError:
				# Task was cancelled due to Ctrl+C
				self._message_manager._remove_last_state_message()
				raise InterruptedError('Model query cancelled by user')
			except InterruptedError:
				# Agent was paused during get_next_action
				self._message_manager._remove_last_state_message()
				raise  # Re-raise to be caught by the outer try/except
			except Exception as e:
				# Model call failed, remove last state message from history
				self._message_manager._remove_last_state_message()
				raise e

			# Execute the model's action(s)
			result = await self.multi_act(model_output.action)
			self.state.last_result = result

			if len(result) > 0 and result[-1].is_done:
				logger.info(f'📄 Result: {result[-1].extracted_content}')

			self.state.consecutive_failures = 0

		except InterruptedError:
			logger.debug('Agent paused')
			self.state.last_result = [
				ActionResult(
					error='The agent was paused mid-step - the last action might need to be repeated',
					include_in_memory=False,
				)
			]
			return
		except asyncio.CancelledError:
			# Directly handle the case where the step is cancelled at a higher level
			self.state.last_result = [ActionResult(error='The agent was paused with Ctrl+C', include_in_memory=False)]
			raise InterruptedError('Step cancelled by user')
		except Exception as e:
			result = await self._handle_step_error(e)
			self.state.last_result = result

		finally:
			step_end_time = time.time()
			if not result:
				return

			if app_state:
				metadata = StepMetadata(
					step_number=self.state.n_steps,
					step_start_time=step_start_time,
					step_end_time=step_end_time,
					input_tokens=tokens,
				)
				self._make_history_item(model_output, app_state, result, metadata)

	async def _handle_step_error(self, error: Exception) -> list[ActionResult]:
		"""Handle all types of errors that can occur during a step"""
		include_trace = logger.isEnabledFor(logging.DEBUG)
		error_msg = AgentError.format_error(error, include_trace=include_trace)
		prefix = f'❌ Result failed {self.state.consecutive_failures + 1}/{self.settings.max_failures} times:\n '
		self.state.consecutive_failures += 1

		if isinstance(error, (ValidationError, ValueError)):
			logger.error(f'{prefix}{error_msg}')
			if 'Max token limit reached' in error_msg:
				# cut tokens from history
				self.settings.max_input_tokens = self.settings.max_input_tokens - 500
				logger.info(f'Cutting tokens from history - new max input tokens: {self.settings.max_input_tokens}')
				# TODO: Implement token cutting in message manager
				# self._message_manager.cut_messages()
			elif 'Could not parse response' in error_msg:
				# give model a hint how output should look like
				error_msg += '\n\nReturn a valid JSON object with the required fields.'

		else:
			from openai import RateLimitError

			RATE_LIMIT_ERRORS = (
				RateLimitError,  # OpenAI
				# Add other rate limit errors as needed
			)

			if isinstance(error, RATE_LIMIT_ERRORS):
				logger.warning(f'{prefix}{error_msg}')
				await asyncio.sleep(self.settings.retry_delay)
			else:
				logger.error(f'{prefix}{error_msg}')

		return [ActionResult(error=error_msg, include_in_memory=True)]

	def _make_history_item(
		self,
		model_output: AgentOutput | None,
		state: AppStateHistory,
		result: list[ActionResult],
		metadata: StepMetadata | None = None,
	) -> None:
		"""Create and store history item"""
		history_item = AgentHistory(model_output=model_output, result=result, state=state, metadata=metadata)
		self.state.history.history.append(history_item)

	THINK_TAGS = re.compile(r'<think>.*?</think>', re.DOTALL)
	STRAY_CLOSE_TAG = re.compile(r'.*?</think>', re.DOTALL)

	def _remove_think_tags(self, text: str) -> str:
		"""Remove thinking tags from text.

		Args:
		    text: Text to process

		Returns:
		    Processed text with thinking tags removed
		"""
		# Step 1: Remove well-formed <think>...</think>
		text = re.sub(self.THINK_TAGS, '', text)
		# Step 2: If there's an unmatched closing tag </think>,
		#         remove everything up to and including that.
		text = re.sub(self.STRAY_CLOSE_TAG, '', text)
		return text.strip()

	async def get_next_action(self, input_messages: list[BaseMessage]) -> AgentOutput:
		"""Get next action from LLM based on current state"""
		# TODO: Implement input message conversion if needed
		# input_messages = self._convert_input_messages(input_messages)

		if self.tool_calling_method == 'raw':
			logger.debug(f'Using {self.tool_calling_method} for {self.chat_model_library}')
			try:
				output = self.llm.invoke(input_messages)
				response = {'raw': output, 'parsed': None}
			except Exception as e:
				logger.error(f'Failed to invoke model: {str(e)}')
				raise Exception('LLM API call failed') from e

			output.content = self._remove_think_tags(str(output.content))
			try:
				# Extract JSON from model output
				parsed_json = extract_json_from_model_output(output.content)
				parsed = self.AgentOutput(**parsed_json)
				response['parsed'] = parsed
			except (ValueError, ValidationError) as e:
				logger.warning(f'Failed to parse model output: {output} {str(e)}')
				raise ValueError('Could not parse response.')

		elif self.tool_calling_method is None:
			structured_llm = self.llm.with_structured_output(self.AgentOutput, include_raw=True)
			try:
				response: dict[str, Any] = await structured_llm.ainvoke(input_messages)  # type: ignore
				parsed: AgentOutput | None = response['parsed']

			except Exception as e:
				logger.error(f'Failed to invoke model: {str(e)}')
				raise Exception('LLM API call failed') from e

		else:
			logger.debug(f'Using {self.tool_calling_method} for {self.chat_model_library}')
			structured_llm = self.llm.with_structured_output(self.AgentOutput, include_raw=True, method=self.tool_calling_method)
			response: dict[str, Any] = await structured_llm.ainvoke(input_messages)  # type: ignore
		# Handle tool call responses
		if response.get('parsing_error') and 'raw' in response:
			raw_msg = response['raw']
			if hasattr(raw_msg, 'tool_calls') and raw_msg.tool_calls:
				# Convert tool calls to AgentOutput format
				tool_call = raw_msg.tool_calls[0]  # Take first tool call

				# Create current state
				tool_call_name = tool_call['name']
				tool_call_args = tool_call['args']

				current_state = AgentBrain(
					evaluation_previous_goal='Executing action',
					memory='Using tool call',
					next_goal=f'Execute {tool_call_name}',
				)

				# Create action from tool call
				action = {tool_call_name: tool_call_args}

				parsed = self.AgentOutput(current_state=current_state, action=[self.ActionModel(**action)])
			else:
				try:
					raw_output = response['raw'].content
					parsed_json = extract_json_from_model_output(raw_output)
					parsed = self.AgentOutput(**parsed_json)
				except Exception as e:
					logger.warning(f'Failed to parse model output: {response["raw"].content} {str(e)}')
					if 'raw' in response:
						logger.warning(f'Raw output: {response["raw"]}')
					raise ValueError('Could not parse response.')
		else:
			parsed = response['parsed']

		# Cut the number of actions to max_actions_per_step if needed
		if len(parsed.action) > self.settings.max_actions_per_step:
			parsed.action = parsed.action[: self.settings.max_actions_per_step]

		# Log the response
		log_response(parsed)

		return parsed

	@property
	def message_manager(self) -> MessageManager:
		"""Get the message manager instance"""
		return self._message_manager

	async def multi_act(self, actions: list[Any]) -> list[ActionResult]:
		"""Execute multiple actions"""
		results = []

		for i, action in enumerate(actions):
			try:
				await self._raise_if_stopped_or_paused()

				result = await self.controller.act(
					action,
					self.app,
					context=self.context,
				)

				results.append(result)

				logger.debug(f'Executed action {i + 1} / {len(actions)}')
				if results[-1].is_done or results[-1].error or i == len(actions) - 1:
					break

				await asyncio.sleep(0.5)  # Small delay between actions

			except asyncio.CancelledError:
				# Gracefully handle task cancellation
				logger.info(f'Action {i + 1} was cancelled due to Ctrl+C')
				if not results:
					# Add a result for the cancelled action
					results.append(
						ActionResult(
							error='The action was cancelled due to Ctrl+C',
							include_in_memory=True,
						)
					)
				raise InterruptedError('Action cancelled by user')

		return results

	def _log_agent_run(self) -> None:
		"""Log the agent run"""
		logger.info(f'🚀 Starting task: {self.task}')

	async def take_step(self) -> tuple[bool, bool]:
		"""Take a step

		Returns:
		    Tuple[bool, bool]: (is_done, is_valid)
		"""
		await self.step()

		if self.state.history.is_done():
			# TODO: Implement validation if needed
			# if self.settings.validate_output:
			#     if not await self._validate_output():
			#         return True, False

			await self.log_completion()
			return True, True

		return False, False

	async def run(
		self,
		max_steps: int = 100,
		on_step_start: AgentHookFunc | None = None,
		on_step_end: AgentHookFunc | None = None,
	) -> AgentHistoryList:
		"""Execute the task with maximum number of steps"""
		agent_run_error: str | None = None  # Initialize error tracking variable

		try:
			self._log_agent_run()

			# Execute initial actions if provided
			if self.initial_actions:
				result = await self.multi_act(self.initial_actions)
				self.state.last_result = result

			for step in range(max_steps):
				# Check if we should stop due to too many failures
				if self.state.consecutive_failures >= self.settings.max_failures:
					logger.error(f'❌ Stopping due to {self.settings.max_failures} consecutive failures')
					agent_run_error = f'Stopped due to {self.settings.max_failures} consecutive failures'
					break

				# Check control flags before each step
				if self.state.stopped:
					logger.info('Agent stopped')
					agent_run_error = 'Agent stopped programmatically'
					break

				while self.state.paused:
					await asyncio.sleep(0.2)  # Small delay to prevent CPU spinning
					if self.state.stopped:  # Allow stopping while paused
						agent_run_error = 'Agent stopped programmatically while paused'
						break

				if on_step_start is not None:
					await on_step_start(self)

				step_info = AgentStepInfo(step_number=step, max_steps=max_steps)
				await self.step(step_info)

				if on_step_end is not None:
					await on_step_end(self)

				if self.state.history.is_done():
					# TODO: Implement validation if needed
					# if self.settings.validate_output and step < max_steps - 1:
					#     if not await self._validate_output():
					#         continue

					await self.log_completion()
					break
			else:
				agent_run_error = 'Failed to complete task in maximum steps'
				logger.info(f'❌ {agent_run_error}')

			return self.state.history

		except KeyboardInterrupt:
			# Handle KeyboardInterrupt
			logger.info('Got KeyboardInterrupt during execution, returning current history')
			agent_run_error = 'KeyboardInterrupt'
			return self.state.history

		except Exception as e:
			logger.error(f'Agent run failed with exception: {e}', exc_info=True)
			agent_run_error = str(e)
			raise e

		finally:
			# Cleanup
			await self.close()
			if self.settings.generate_gif:
				output_path: str = 'agent_history.gif'
				if isinstance(self.settings.generate_gif, str):
					output_path = self.settings.generate_gif
				create_history_gif(task=self.task, history=self.state.history, output_path=output_path)

	async def log_completion(self) -> None:
		"""Log the completion of the task"""
		logger.info('✅ Task completed')
		if self.state.history.is_successful():
			logger.info('✅ Successfully')
		else:
			logger.info('❌ Unfinished')

		total_tokens = self.state.history.total_input_tokens()
		logger.info(f'📝 Total input tokens used (approximate): {total_tokens}')

	def _convert_initial_actions(self, actions: list[dict[str, dict[str, Any]]]) -> list[Any]:
		"""Convert dictionary-based actions to ActionModel instances"""
		converted_actions = []
		for action_dict in actions:
			# Each action_dict should have a single key-value pair
			action_name = next(iter(action_dict))
			params = action_dict[action_name]

			# Get the parameter model for this action from registry
			action_info = self.controller.registry.registry.actions[action_name]
			param_model = action_info.param_model

			# Create validated parameters using the appropriate param model
			validated_params = param_model(**params)

			# Create ActionModel instance with the validated parameters
			action_model = self.ActionModel(**{action_name: validated_params})
			converted_actions.append(action_model)

		return converted_actions

	def _verify_llm_connection(self) -> bool:
		"""
		Verify that the LLM API keys are setup and the LLM API is responding properly.
		Helps prevent errors due to running out of API credits, missing env vars, or network issues.

		Returns:
		    bool: True if connection is verified, False otherwise
		"""
		logger.debug(f'Verifying the {self.llm.__class__.__name__} LLM knows the capital of France...')

		if getattr(self.llm, '_verified_api_keys', None) is True or SKIP_LLM_API_KEY_VERIFICATION:
			# skip roundtrip connection test for speed in cloud environment
			# If the LLM API keys have already been verified during a previous run, skip the test
			self.llm._verified_api_keys = True
			return True

		# Show a warning if it looks like any required environment variables are missing
		required_keys = REQUIRED_LLM_API_ENV_VARS.get(self.llm.__class__.__name__, [])
		if required_keys and not self._check_env_variables(required_keys, any_or_all=all):
			error = f'Expected LLM API Key environment variables might be missing for {self.llm.__class__.__name__}: {" ".join(required_keys)}'
			logger.warning(f'❌ {error}')

		# Send a basic sanity-test question to the LLM and verify the response
		test_prompt = 'What is the capital of France? Respond with a single word.'
		test_answer = 'paris'
		try:
			# Don't convert this to async! it *should* block any subsequent llm calls from running
			response = self.llm.invoke([HumanMessage(content=test_prompt)])
			response_text = str(response.content).lower()

			if test_answer in response_text:
				logger.debug(
					f'🪪 LLM API keys {", ".join(required_keys)} work, {self.llm.__class__.__name__} model is connected & responding correctly.'
				)
				self.llm._verified_api_keys = True
				return True
			else:
				logger.warning(
					'❌  Got bad LLM response to basic sanity check question: \n\t  %s\n\t\tEXPECTING: %s\n\t\tGOT: %s',
					test_prompt,
					test_answer,
					response,
				)
				raise Exception('LLM responded to a simple test question incorrectly')
		except Exception as e:
			self.llm._verified_api_keys = False
			if required_keys:
				logger.error(
					f'\n\n❌  LLM {self.llm.__class__.__name__} connection test failed. Check that {", ".join(required_keys)} is set correctly in .env and that the LLM API account has sufficient funding.\n\n{e}\n'
				)
				return False
			else:
				return False

	def _check_env_variables(self, required_vars: list[str], any_or_all=any) -> bool:
		"""
		Check if required environment variables are set.
		Args:
		    required_vars: List of required environment variables
		    any_or_all: Function to use for checking (any or all)

		Returns:
		    bool: True if required variables are set according to any_or_all condition
		"""
		return any_or_all(var in os.environ and os.environ[var] for var in required_vars)

	def pause(self) -> None:
		"""Pause the agent before the next step"""
		print('\n\n⏸️  Got Ctrl+C, paused the agent.')
		self.state.paused = True

	def resume(self) -> None:
		"""Resume the agent"""
		print('----------------------------------------------------------------------')
		print('▶️  Got Enter, resuming agent execution where it left off...\n')
		self.state.paused = False

	def stop(self) -> None:
		"""Stop the agent"""
		logger.info('⏹️ Agent stopping')
		self.state.stopped = True

	async def close(self):
		"""Close all resources"""
		try:
			# Force garbage collection
			self.app.close()
			gc.collect()
		except Exception as e:
			logger.error(f'Error during cleanup: {e}')

	# ------------------------------------------------------------------
	# Planner integration
	# ------------------------------------------------------------------

	async def _run_planner(self, step_info: AgentStepInfo | None = None) -> None:
		"""Run the planner if conditions are met"""
		if not self.settings.planner_llm:
			return

		# Only run planner based on interval
		if self.state.n_steps % self.settings.planner_interval != 0:
			return

		logger.info(f'📋 Running planner (step {self.state.n_steps})')

		try:
			# Get current app state for planner context
			app_state = self.app.get_app_state()

			# Create planner messages
			messages = []

			# Add system message for planner
			system_prompt = PlannerPrompt(
				available_actions=self.unfiltered_actions,
				original_task=self.task,
				current_step=self.state.n_steps,
				is_reasoning=self.settings.is_planner_reasoning,
				extend_prompt=self.settings.extend_planner_system_prompt,
			).get_system_message()

			messages.append(SystemMessage(content=system_prompt))

			# Add current state context
			app_context = f'Current app state: {len(app_state.selector_map)} elements available'
			if hasattr(app_state, 'get_text_representation'):
				app_context += f'\n{app_state.get_text_representation()}'

			# Add recent history context
			if len(self.state.history.history) > 0:
				recent_actions = []
				for i, hist in enumerate(self.state.history.history[-3:]):  # Last 3 actions
					if hist.model_output:
						for action in hist.model_output.action:
							action_dict = action.model_dump(exclude_none=True)
							action_type = list(action_dict.keys())[0] if action_dict else 'unknown'
							recent_actions.append(f'Step {len(self.state.history.history) - 2 + i}: {action_type}')

				if recent_actions:
					app_context += f'\nRecent actions: {"; ".join(recent_actions)}'

			# Add task progress message
			progress_message = f"""
Task: {self.task}

Current Progress:
- Step: {self.state.n_steps}
- {app_context}

Please analyze the current situation and provide strategic guidance for the next steps.
Focus on high-level planning and identifying the most efficient path to complete the task.
"""

			messages.append(HumanMessage(content=progress_message))

			# Query the planner LLM
			if self.settings.is_planner_reasoning:
				# Use reasoning mode - just get text response
				response = await self.settings.planner_llm.ainvoke(messages)
				planner_output = response.content if hasattr(response, 'content') else str(response)
				logger.info(f'🧠 Planner guidance: {planner_output[:200]}...')

				# Add planner guidance to message manager
				guidance_message = HumanMessage(content=f'Strategic guidance from planner: {planner_output}')
				self._message_manager._add_message_with_tokens(guidance_message)
			else:
				# Simple planner mode - just log insights
				response = await self.settings.planner_llm.ainvoke(messages)
				planner_output = response.content if hasattr(response, 'content') else str(response)
				logger.info(f'🧠 Planner insights: {planner_output[:200]}...')

		except Exception as e:
			logger.warning(f'⚠️ Planner execution failed: {str(e)}')
