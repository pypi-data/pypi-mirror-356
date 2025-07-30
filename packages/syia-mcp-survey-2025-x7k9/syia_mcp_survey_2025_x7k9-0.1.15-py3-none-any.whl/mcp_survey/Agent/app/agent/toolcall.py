import json
from typing import Any, List, Optional, Union, Tuple

from pydantic import Field

from ...app.agent.react import ReActAgent
from ...app.logger import logger

from ...app.schema import TOOL_CHOICE_TYPE, AgentState, Message, ToolCall, ToolChoice
from ...app.tool import CreateChatCompletion, Terminate, ToolCollection
from ...markdown_logger import MarkdownLogger

# 🔧 ADD: Token counting and MongoDB imports
import tiktoken
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, UTC

TOOL_CALL_REQUIRED = "Tool calls required but none provided"

# 🔧 ADD: Token counting function
def token_count(input_text):
    """Count tokens in the input text using tiktoken"""
    input_text = str(input_text)
    encoding = tiktoken.encoding_for_model("gpt-4o")  # correct model name for GPT-4
    tokens = encoding.encode(input_text)
    return len(tokens)

# 🔧 ADD: MongoDB token tracking function
def write_updateMongodb(sessionId, token, response_token):
    """Update MongoDB with token usage information"""
    mongodb_url = "mongodb://etl:rSp6X49ScvkDpHE@db.syia.ai:27017/?authMechanism=DEFAULT&authSource=syia-etl&directConnection=true"
    db_name = "syia-etl"
    collection_name = "mailCasefile_tokenCounter_fixCasefile"

    try:
        client = MongoClient(mongodb_url)
        db = client[db_name]
        collection = db[collection_name]

        entry = collection.find_one({"_id": ObjectId(sessionId)})
        if entry:
            InputToken_list = entry.get("InputToken_list", [])
            responseToken_list = entry.get("responseToken_list", [])
            if not InputToken_list:
                InputToken_list = []
            InputToken_list.append(token)  # mutate the list in place    
            
            if not responseToken_list:
                responseToken_list = []
            responseToken_list.append(response_token)  # mutate the list in place 

            InputTokenSum = sum(InputToken_list)
            responseTokenSum = sum(responseToken_list)
            logger.info(f"InputTokenSum: {InputTokenSum}, responseTokenSum: {responseTokenSum}")
            collection.update_one(
                {"_id": ObjectId(sessionId)},
                {
                    "$set": {
                        "InputToken_list": InputToken_list,
                        "responseToken_list": responseToken_list,
                        "InputTokenSum": InputTokenSum,
                        "responseTokenSum": responseTokenSum,
                    }
                }
            )
        else:
            collection.insert_one({
                "_id": ObjectId(sessionId),
                "InputToken_list": [token],
                "responseToken_list": [response_token],
                "InputTokenSum": token,
                "responseTokenSum": response_token,
                "dateTime": datetime.now(UTC)
            })
        client.close()
    except Exception as e:
        logger.error(f"Failed to update MongoDB token tracking: {e}")

class ToolCallAgent(ReActAgent):
    """Base agent class for handling tool/function calls with enhanced abstraction"""

    name: str = "toolcall"
    description: str = "an agent that can execute tool calls."

    system_prompt: str = ""
    next_step_prompt: str = ""

    available_tools: ToolCollection = ToolCollection(
        CreateChatCompletion(), Terminate()
    )
    tool_choices: TOOL_CHOICE_TYPE = ToolChoice.AUTO  # type: ignore
    special_tool_names: List[str] = Field(default_factory=lambda: [Terminate().name])

    tool_calls: List[ToolCall] = Field(default_factory=list)
    markdown_logger: MarkdownLogger = Field(default_factory=MarkdownLogger)
    max_steps: int = 30
    max_observe: Optional[Union[int, bool]] = None
    
    # 🔧 ADD: Session ID for token tracking (optional)
    session_id: Optional[str] = None

    async def think(self) -> bool:
        """Process current state and decide next actions using tools"""
        if self.next_step_prompt:
            user_msg = Message.user_message(self.next_step_prompt) 
            self.messages += [user_msg]

        self.system_prompt = self.system_prompt + " Please use the generate_thought tool to explain your reasoning before using any other tools. If the user asks to write or save the content into a file, use the file_writer tool to do so."
        
        # 🔧 MODIFIED: Get response with token counting
        response_data = await self.llm.ask_tool(
            messages=self.messages,
            system_msgs=[Message.system_message(self.system_prompt)] if self.system_prompt else None,
            tools=self.available_tools.to_params(),
            tool_choice=self.tool_choices,
        )
        
        # 🔧 ADD: Handle token tracking if response includes token info
        if isinstance(response_data, tuple) and len(response_data) == 2:
            response, input_tokens = response_data
            response_tokens = token_count(response)
            
            # Save token usage to MongoDB if session_id is available
            if self.session_id:
                write_updateMongodb(self.session_id, input_tokens, response_tokens)
                logger.info(f"Token usage tracked - Input: {input_tokens}, Response: {response_tokens}")
        else:
            response = response_data

        self.tool_calls = response.tool_calls

        # Log response info
        logger.info(f"{self.name}'s content: {response.content}")
        if response.content:
            self.markdown_logger.write(f"{self.name}'s content", response.content)

        logger.info(
            f"🛠️ {self.name} selected {len(response.tool_calls) if response.tool_calls else 0} tools to use"
        )
        self.markdown_logger.write(f"🛠️ {self.name} selected {len(response.tool_calls) if response.tool_calls else 0} tools to use", response.tool_calls)
        if response.tool_calls:
            logger.info(
                 f"🧰 Tools being prepared: {[call.function.name for call in response.tool_calls]}"
            )
            self.markdown_logger.write(f"🧰 Tools being prepared: {[call.function.name for call in response.tool_calls]}", response.tool_calls)

        try:
            # Handle different tool_choices modes
            if self.tool_choices == ToolChoice.NONE:
                if response.tool_calls:
                    logger.warning(
                        f"🤔 Hmm, {self.name} tried to use tools when they weren't available!"
                    )
                    self.markdown_logger.write(f"🤔 Hmm, {self.name} tried to use tools when they weren't available!", response.tool_calls)
                if response.content:
                    self.memory.add_message(Message.assistant_message(response.content))
                    return True
                return False

            # Create and add assistant message
            assistant_msg = (
                Message.from_tool_calls(
                    content=response.content, tool_calls=self.tool_calls
                )
                if self.tool_calls
                else Message.assistant_message(response.content)
            )
            self.memory.add_message(assistant_msg)

            if self.tool_choices == ToolChoice.REQUIRED and not self.tool_calls:
                return True  # Will be handled in act()

            # For 'auto' mode, continue with content if no commands but content exists
            if self.tool_choices == ToolChoice.AUTO and not self.tool_calls:
                return bool(response.content)

            return bool(self.tool_calls)
        except Exception as e:
            logger.error(f"🚨 Oops! The {self.name}'s thinking process hit a snag: {e}")
            self.markdown_logger.write(f"🚨 Oops! The {self.name}'s thinking process hit a snag: {e}", e)
            self.memory.add_message(
                Message.assistant_message(
                    f"Error encountered while processing: {str(e)}"
                )
            )
            return False

    async def act(self) -> str:
        """Execute tool calls and handle their results"""
        if not self.tool_calls:
            if self.tool_choices == ToolChoice.REQUIRED:
                raise ValueError(TOOL_CALL_REQUIRED)

            # Return last message content if no tool calls
            return self.messages[-1].content or "No content or commands to execute"

        results = []
        for command in self.tool_calls:

            result , our_result= await self.execute_tool(command)

            
            logger.info(
                f"🎯 Tool '{command.function.name}' completed its mission! Result: {result}"
            )
            self.markdown_logger.write(f"🎯 Tool '{command.function.name}'  Response:", result)

            if self.max_observe:
                result = result[: self.max_observe]

            # Add tool response to memory
            tool_msg = Message.tool_message(
                content=result, tool_call_id=command.id, name=command.function.name
            )
            self.memory.add_message(tool_msg)
            results.append(result)

        return "\n\n".join(results)

    async def execute_tool(self, command: ToolCall) -> Tuple[str, Any]:
        """Execute a single tool call with robust error handling"""
        if not command or not command.function or not command.function.name:
            return "Error: Invalid command format"

        name = command.function.name
        if name not in self.available_tools.tool_map:
            return f"Error: Unknown tool '{name}'"

        try:
            # Parse arguments
            args = json.loads(command.function.arguments or "{}")
           

            logger.info(f"Arguments for the tool: {args}")
            self.markdown_logger.write(f"Arguments for the tool:", args)

 
            result = await self.available_tools.execute(name=name, tool_input=args)

            result_new = result
            # Format result for display
            observation = (
                f"Observed output of cmd `{name}` executed:\n{str(result_new)}"
                if result
                else f"Cmd `{name}` completed with no output"
            )


            # Handle special tools like `finish`
            await self._handle_special_tool(name=name, result=result_new)

            return observation,result_new
        except json.JSONDecodeError:
            error_msg = f"Error parsing arguments for {name}: Invalid JSON format"
            logger.error(
                f"📝 Oops! The arguments for '{name}' don't make sense - invalid JSON, arguments:{command.function.arguments}"
            )
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"⚠️ Tool '{name}' encountered a problem: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"

    async def _handle_special_tool(self, name: str, result: Any, **kwargs):
        """Handle special tool execution and state changes"""
        if not self._is_special_tool(name):
            return

        if self._should_finish_execution(name=name, result=result, **kwargs):
            # Set agent state to finished
            logger.info(f"🏁 Special tool '{name}' has completed the task!")
            self.state = AgentState.FINISHED

    
    @staticmethod
    def _should_finish_execution(**kwargs) -> bool:
        """Determine if tool execution should finish the agent"""
        return True

    def _is_special_tool(self, name: str) -> bool:
        """Check if tool name is in special tools list"""
        return name.lower() in [n.lower() for n in self.special_tool_names]
