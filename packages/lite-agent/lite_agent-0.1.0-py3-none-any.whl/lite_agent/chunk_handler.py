from collections.abc import AsyncGenerator
from typing import Literal, TypedDict

import litellm
from funcall import Funcall

from open_agents.loggers import logger
from open_agents.processors import StreamChunkProcessor
from open_agents.processors.stream_chunk_processor import AssistantMessage


class LiteLLMRawChunk(TypedDict):
    """
    Define the type of chunk
    """

    type: Literal["litellm_raw"]
    raw: litellm.ModelResponseStream


class UsageChunk(TypedDict):
    """
    Define the type of usage info chunk
    """

    type: Literal["usage"]
    usage: litellm.Usage


class FinalMessageChunk(TypedDict):
    """
    Define the type of final message chunk
    """

    type: Literal["final_message"]
    message: AssistantMessage
    finish_reason: Literal["stop", "tool_calls"]


class ToolCallChunk(TypedDict):
    """
    Define the type of tool call chunk
    """

    type: Literal["tool_call"]
    name: str
    arguments: str


class ToolCallResultChunk(TypedDict):
    """
    Define the type of tool call result chunk
    """

    type: Literal["tool_call_result"]
    tool_call_id: str
    name: str
    content: str


class ContentDeltaChunk(TypedDict):
    """
    Define the type of message chunk
    """

    type: Literal["content_delta"]
    delta: str


class ToolCallDeltaChunk(TypedDict):
    """
    Define the type of tool call delta chunk
    """

    type: Literal["tool_call_delta"]
    tool_call_id: str
    name: str
    arguments_delta: str


AgentChunk = LiteLLMRawChunk | UsageChunk | FinalMessageChunk | ToolCallChunk | ToolCallResultChunk | ContentDeltaChunk


async def chunk_handler(
    resp: litellm.CustomStreamWrapper,
    fc: Funcall,
) -> AsyncGenerator[AgentChunk, None]:
    """
    Optimized chunk handler

    Args:
        resp: LiteLLM streaming response wrapper
        fc: function call handler

    Yields:
        litellm.ModelResponseStream: processed response chunk

    Raises:
        Exception: various exceptions during processing
    """
    processor = StreamChunkProcessor(fc)
    async for chunk in resp:
        if not isinstance(chunk, litellm.ModelResponseStream):
            logger.debug("unexpected chunk type: %s", type(chunk))
            logger.debug("chunk content: %s", chunk)
            continue

        # Handle usage info
        if usage := processor.handle_usage_info(chunk):
            yield UsageChunk(type="usage", usage=usage)
            continue

        # Get choice and delta data
        if not chunk.choices:
            yield LiteLLMRawChunk(type="litellm_raw", raw=chunk)
            continue

        choice = chunk.choices[0]
        delta = choice.delta
        if not processor.current_message:
            processor.initialize_message(chunk, choice)
        if delta.content:
            yield ContentDeltaChunk(type="content_delta", delta=delta.content)
        processor.update_content(delta.content)
        processor.update_tool_calls(delta.tool_calls)
        if delta.tool_calls:
            for tool_call in delta.tool_calls:
                if tool_call.function.arguments:
                    yield ToolCallDeltaChunk(
                        type="tool_call_delta",
                        tool_call_id=processor.current_message.tool_calls[-1].id,
                        name=processor.current_message.tool_calls[-1].function.name,
                        arguments_delta=tool_call.function.arguments,
                    )
        # Check if finished
        if choice.finish_reason and processor.current_message:
            current_message = processor.finalize_message()
            yield FinalMessageChunk(type="final_message", message=current_message, finish_reason=choice.finish_reason)
            # New: check tool_calls and handle
            tool_calls = current_message.tool_calls
            if tool_calls:
                # Execute each tool_call and yield result
                for tool_call in tool_calls:
                    try:
                        yield ToolCallChunk(
                            type="tool_call",
                            name=tool_call.function.name,
                            arguments=tool_call.function.arguments,
                        )
                        content = await fc.call_function_async(tool_call.function.name, tool_call.function.arguments)
                        yield ToolCallResultChunk(
                            type="tool_call_result",
                            tool_call_id=tool_call.id,
                            name=tool_call.function.name,
                            content=str(content),
                        )
                    except Exception as e:  # noqa: PERF203
                        logger.exception("Tool call %s failed", tool_call.id)
                        yield ToolCallResultChunk(
                            type="tool_call_result",
                            tool_call_id=tool_call.id,
                            name=tool_call.function.name,
                            content=str(e),
                        )
            continue
        yield LiteLLMRawChunk(type="litellm_raw", raw=chunk)
