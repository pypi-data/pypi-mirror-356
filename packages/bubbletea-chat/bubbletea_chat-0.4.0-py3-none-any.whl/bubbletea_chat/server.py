"""
FastAPI server implementation for BubbleTea chatbots
"""

import json
import asyncio
from typing import Optional, AsyncGenerator
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

from .decorators import ChatbotFunction
from . import decorators
from .schemas import ComponentChatRequest, ComponentChatResponse, BotConfig
from .components import Done


class BubbleTeaServer:
    """FastAPI server for hosting BubbleTea chatbots"""
    
    def __init__(self, chatbot: ChatbotFunction, port: int = 8000):
        self.app = FastAPI(title=f"BubbleTea Bot: {chatbot.name}")
        self.chatbot = chatbot
        self.port = port
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup the chat endpoint"""
        
        @self.app.post("/chat")
        async def chat_endpoint(request: ComponentChatRequest):
            """Handle chat requests"""
            response = await self.chatbot.handle_request(request)
            
            if self.chatbot.stream:
                # Streaming response
                async def stream_generator():
                    async for component in response:
                        # Convert component to JSON and wrap in SSE format
                        data = component.model_dump_json()
                        yield f"data: {data}\n\n"
                    # Send done signal
                    done = Done()
                    yield f"data: {done.model_dump_json()}\n\n"
                
                return StreamingResponse(
                    stream_generator(),
                    media_type="text/event-stream"
                )
            else:
                # Non-streaming response
                return response
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "bot_name": self.chatbot.name,
                "streaming": self.chatbot.stream
            }
        
        # Register config endpoint if decorator was used
        if decorators._config_function:
            config_func, config_path = decorators._config_function
            
            @self.app.get(config_path, response_model=BotConfig)
            async def config_endpoint():
                """Get bot configuration"""
                # Check if config function is async
                if asyncio.iscoroutinefunction(config_func):
                    result = await config_func()
                else:
                    result = config_func()
                
                # Ensure result is a BotConfig instance
                if isinstance(result, BotConfig):
                    return result
                elif isinstance(result, dict):
                    return BotConfig(**result)
                else:
                    # Try to convert to BotConfig
                    return result
    
    def run(self, host: str = "0.0.0.0"):
        """Run the server"""
        uvicorn.run(self.app, host=host, port=self.port)


def run_server(chatbot: ChatbotFunction, port: int = 8000, host: str = "0.0.0.0"):
    """
    Run a FastAPI server for the given chatbot
    
    Args:
        chatbot: The chatbot function decorated with @chatbot
        port: Port to run the server on
        host: Host to bind the server to
    """
    server = BubbleTeaServer(chatbot, port)
    server.run(host)