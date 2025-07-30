import os
import asyncio
from typing import Any, Dict, Iterator, List, Optional, AsyncIterator
from google import genai
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
    AsyncCallbackManagerForLLMRun
)
from pydantic import Field, SecretStr
from langchain_core.utils import convert_to_secret_str

class GeminiChatModel(BaseChatModel):
    """Custom chat model using Google's genai client package directly with real streaming support.
    
    This implementation provides direct access to Google's genai features
    while being compatible with LangChain's BaseChatModel interface.
    
    Example:
        ```python
        model = GeminiChatModel(
            model_name="gemini-2.0-flash",
            google_api_key="your-api-key",
            temperature=0.7
        )
        
        # Basic usage
        response = model.invoke("Hello, how are you?")
        print(response.content)
        
        # Streaming usage
        for chunk in model.stream("Tell me a story"):
            print(chunk.content, end="")
            
        # Async usage
        async def test_async():
            response = await model.ainvoke("Hello!")
            print(response.content)
            
            async for chunk in model.astream("Tell me a story"):
                print(chunk.content, end="")
        ```
    """
    
    # Model configuration
    model_name: str = Field(default="gemini-2.0-flash", description="The Google model name to use")
    google_api_key: Optional[SecretStr] = Field(default=None, description="Google API key")
    temperature: Optional[float] = Field(default=0.7, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")
    top_p: Optional[float] = Field(default=None, description="Top-p sampling parameter")
    top_k: Optional[int] = Field(default=None, description="Top-k sampling parameter")
    
    # Internal client
    _client: Optional[genai.Client] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Get API key from environment if not provided
        if self.google_api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                self.google_api_key = convert_to_secret_str(api_key)
        
        # Initialize the Google GenAI client
        if self.google_api_key:
            self._client = genai.Client(
                api_key=self.google_api_key.get_secret_value()
            )
        else:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass google_api_key parameter.")
    
    @property
    def _llm_type(self) -> str:
        """Return identifier for the model type."""
        return "custom_google_genai"
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters for tracing."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "top_k": self.top_k,
        }
    
    def _convert_messages_to_genai_format(self, messages: List[BaseMessage]) -> str:
        """Convert LangChain messages to Google GenAI format.
        
        Google GenAI API doesn't support system messages, so we'll convert
        the conversation to a single prompt string with proper formatting.
        """
        prompt_parts = []
        
        for message in messages:
            if isinstance(message, SystemMessage):
                # Convert system message to instruction format
                prompt_parts.append(f"Instructions: {message.content}")
            elif isinstance(message, HumanMessage):
                prompt_parts.append(f"Human: {message.content}")
            elif isinstance(message, AIMessage):
                prompt_parts.append(f"Assistant: {message.content}")
            else:
                # Default to human format for unknown message types
                prompt_parts.append(f"Human: {str(message.content)}")
        
        # Add a final prompt for the assistant to respond
        if not prompt_parts or not prompt_parts[-1].startswith("Human:"):
            prompt_parts.append("Human: Please respond to the above.")
        
        prompt_parts.append("Assistant:")
        
        return "\n\n".join(prompt_parts)
    
    def _prepare_generation_config(self, stop: Optional[List[str]] = None) -> Dict[str, Any]:
        """Prepare generation configuration for Google GenAI."""
        generation_config = {}
        if self.temperature is not None:
            generation_config["temperature"] = self.temperature
        if self.max_tokens is not None:
            generation_config["max_output_tokens"] = self.max_tokens
        if self.top_p is not None:
            generation_config["top_p"] = self.top_p
        if self.top_k is not None:
            generation_config["top_k"] = self.top_k
        if stop:
            generation_config["stop_sequences"] = stop
        return generation_config
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a response using Google's genai client."""
        
        # Convert messages to a single prompt string
        prompt = self._convert_messages_to_genai_format(messages)
        
        # Prepare generation config
        generation_config = self._prepare_generation_config(stop)
        
        try:
            # Generate response using Google GenAI
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=generation_config if generation_config else None
            )
            
            # Extract the generated text
            generated_text = response.text if hasattr(response, 'text') else str(response)
            
            # Create AI message with response metadata
            message = AIMessage(
                content=generated_text,
                response_metadata={
                    "model_name": self.model_name,
                    "finish_reason": getattr(response, 'finish_reason', None),
                }
            )
            
            # Create and return ChatResult
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])
            
        except Exception as e:
            raise ValueError(f"Error generating content with Google GenAI: {str(e)}")
    
    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Async generate a response using Google's genai client."""
        
        # Convert messages to a single prompt string
        prompt = self._convert_messages_to_genai_format(messages)
        
        # Prepare generation config
        generation_config = self._prepare_generation_config(stop)
        
        try:
            # Generate response using Google GenAI (run in executor for async)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=generation_config if generation_config else None
                )
            )
            
            # Extract the generated text
            generated_text = response.text if hasattr(response, 'text') else str(response)
            
            # Create AI message with response metadata
            message = AIMessage(
                content=generated_text,
                response_metadata={
                    "model_name": self.model_name,
                    "finish_reason": getattr(response, 'finish_reason', None),
                }
            )
            
            # Create and return ChatResult
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])
            
        except Exception as e:
            raise ValueError(f"Error generating content with Google GenAI: {str(e)}")
    
    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """Stream the output using Google's genai client with real streaming."""
        
        # Convert messages to a single prompt string
        prompt = self._convert_messages_to_genai_format(messages)
        
        # Prepare generation config
        generation_config = self._prepare_generation_config(stop)
        
        try:
            # Use Google GenAI streaming
            stream = self._client.models.generate_content_stream(
                model=self.model_name,
                contents=prompt,
                config=generation_config if generation_config else None
            )
            
            for chunk_response in stream:
                if hasattr(chunk_response, 'text') and chunk_response.text:
                    content = chunk_response.text
                    
                    chunk = ChatGenerationChunk(
                        message=AIMessageChunk(
                            content=content,
                            response_metadata={
                                "model_name": self.model_name,
                                "finish_reason": getattr(chunk_response, 'finish_reason', None),
                            }
                        )
                    )
                    yield chunk
                    
                    # Trigger callback for new token
                    if run_manager:
                        run_manager.on_llm_new_token(content, chunk=chunk)
        
        except Exception as e:
            # Fallback to non-streaming if streaming fails
            try:
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=generation_config if generation_config else None
                )
                
                generated_text = response.text if hasattr(response, 'text') else str(response)
                
                # Simulate streaming by yielding words
                words = generated_text.split()
                for i, word in enumerate(words):
                    content = f" {word}" if i > 0 else word
                    
                    chunk = ChatGenerationChunk(
                        message=AIMessageChunk(content=content)
                    )
                    yield chunk
                    
                    if run_manager:
                        run_manager.on_llm_new_token(content, chunk=chunk)
                        
            except Exception as fallback_e:
                raise ValueError(f"Error streaming content with Google GenAI: {str(e)}. Fallback also failed: {str(fallback_e)}")
    
    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        """Async stream the output using Google's genai client."""
        
        # Convert messages to a single prompt string
        prompt = self._convert_messages_to_genai_format(messages)
        
        # Prepare generation config
        generation_config = self._prepare_generation_config(stop)
        
        try:
            # Use Google GenAI streaming in async context
            loop = asyncio.get_event_loop()
            
            # Run the streaming in executor
            def create_stream():
                return self._client.models.generate_content_stream(
                    model=self.model_name,
                    contents=prompt,
                    config=generation_config if generation_config else None
                )
            
            stream = await loop.run_in_executor(None, create_stream)
            
            for chunk_response in stream:
                if hasattr(chunk_response, 'text') and chunk_response.text:
                    content = chunk_response.text
                    
                    chunk = ChatGenerationChunk(
                        message=AIMessageChunk(
                            content=content,
                            response_metadata={
                                "model_name": self.model_name,
                                "finish_reason": getattr(chunk_response, 'finish_reason', None),
                            }
                        )
                    )
                    yield chunk
                    
                    # Trigger callback for new token
                    if run_manager:
                        await run_manager.on_llm_new_token(content, chunk=chunk)
        
        except Exception as e:
            # Fallback to async generate and simulate streaming
            try:
                result = await self._agenerate(messages, stop, run_manager, **kwargs)
                generated_text = result.generations[0].message.content
                
                # Simulate streaming by yielding words
                words = generated_text.split()
                for i, word in enumerate(words):
                    content = f" {word}" if i > 0 else word
                    
                    chunk = ChatGenerationChunk(
                        message=AIMessageChunk(content=content)
                    )
                    yield chunk
                    
                    if run_manager:
                        await run_manager.on_llm_new_token(content, chunk=chunk)
                        
            except Exception as fallback_e:
                raise ValueError(f"Error async streaming content with Google GenAI: {str(e)}. Fallback also failed: {str(fallback_e)}")