from textual.app import App, ComposeResult
from textual.widgets import Input, Label
from textual.widgets import Markdown
from textual.containers import Vertical, Container, Horizontal
from textual import events
import asyncio
import argparse
from chat_manager import ChatManager


class ClaudeCodeApp(App):
    CSS = """
    Screen {
        background: transparent;
        padding: 0;
        margin: 0;
    }
    
    #content_panel {
        height: 1fr;
        background: transparent;
        padding: 0;
        overflow: hidden;
    }
    
    #output {
        background: transparent;
        color: #ffffff;
        scrollbar-background: #333333;
        scrollbar-color: #666666;
        height: 100%;
        overflow-y: auto;
        scrollbar-size: 1 1;
    }
    
    #input_panel {
        height: auto;
        background: transparent;
        border: solid white;
        margin: 0;
        padding: 0 1;
    }
    
    #input_container {
        height: auto;
        background: transparent;
        align: left middle;
    }
    
    #user_input {
        margin: 0;
        background: transparent;
        border: none;
        color: #ffffff;
        height: 1;
        min-height: 1;
    }
    
    #user_input:focus {
        border: none;
        background: transparent;
    }
    
    #prompt {
        color: #ffffff;
        width: auto;
        content-align: center middle;
        text-style: bold;
    }
    
    .message {
        margin: 1 0;
        padding: 1;
    }
    
    .user-message {
        background: #2a2a2a;
        border-left: thick #d97706;
        color: #ffffff;
    }
    
    .assistant-message {
        background: #1a1a1a;
        border-left: thick #10b981;
        color: #ffffff;
    }
    """
    
    def __init__(self, model_name="qwen2.5:7b-instruct", num_ctx=None, host="192.168.170.76"):
        super().__init__()
        self.chat_manager = ChatManager(model_name=model_name, num_ctx=num_ctx, host=host)
        self.current_task = None

    def compose(self) -> ComposeResult:
        with Vertical():
            with Container(id="content_panel"):
                yield Markdown("", id="output")
            with Container(id="input_panel"):
                with Horizontal(id="input_container"):
                    yield Label("> ", id="prompt")
                    yield Input(placeholder="Type your message here...", id="user_input")
    
    def on_mount(self):
        """Initialize the display"""
        import os
        current_dir = os.getcwd()
        welcome_msg = f"Welcome to Claude Code!\ncwd: {current_dir}"
        output_widget = self.query_one("#output", Markdown)
        output_widget.update(welcome_msg)
        
        # Set up UI refresh callback for real-time tool updates
        self.chat_manager.ui_refresh_callback = self.update_conversation_display

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_text = event.value.strip()
        if not user_text:
            return
        
        if self.chat_manager.is_processing():
            return
        
            
        self.chat_manager.add_user_message(user_text)
        self.update_conversation_display()
        
        # Clear input
        event.input.value = ""
        
        # Process with ollama asynchronously
        self.run_worker(self.process_ollama_response(user_text), exclusive=True)


    async def process_ollama_response(self, user_text: str):
        assistant_response = await self.chat_manager.get_assistant_response(user_text)
        if assistant_response:  # Only add if there's actual content
            self.chat_manager.add_assistant_message(assistant_response)
        self.update_conversation_display()
        
        # Re-enable input to continue the loop
        input_widget = self.query_one("#user_input", Input)
        input_widget.disabled = False
        input_widget.focus()

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape" and self.chat_manager.is_processing():
            self.interrupt_processing()
            event.prevent_default()

    def interrupt_processing(self):
        if self.current_task:
            self.current_task.cancel()
        self.chat_manager.stop_processing()
        self.chat_manager.add_assistant_message("**Process interrupted by user**")
        self.update_conversation_display()

    def update_conversation_display(self):
        output_widget = self.query_one("#output", Markdown)
        conversation_text = self.chat_manager.get_conversation_text()
        output_widget.update(conversation_text)
        output_widget.scroll_end()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Claude Code - AI coding assistant")
    parser.add_argument("--model", default="qwen2.5:7b-instruct", help="Ollama model to use (default: qwen2.5:7b-instruct)")
    parser.add_argument("--num_ctx", type=int, help="Context length for the model")
    parser.add_argument("--host", default="192.168.170.76", help="Ollama host address (default: 192.168.170.76)")
    
    args = parser.parse_args()
    
    app = ClaudeCodeApp(model_name=args.model, num_ctx=args.num_ctx, host=args.host)
    app.run()
