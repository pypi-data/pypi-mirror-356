from ollama import Client
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

console = Console()

class OllamaRichClient:
    def __init__(self, host=''):
        self.client = Client(host=host)

    def chat_and_display(self, model, messages):
        response = self.client.chat(
            model=model,
            stream=True,
            messages=messages,
        )

        full_content = ""
        with Live(Markdown(full_content), console=console, refresh_per_second=2) as live:
            for chunk in response:
                full_content += chunk['message']['content']
                live.update(Markdown(full_content))


    def chat(self, model, messages):
        with console.status("[bold green]Thinking...", spinner="dots"):
            response = self.client.chat(
                model=model,
                stream=False,
                messages=messages,
            )
        return Markdown(response['message']['content'])
    
    def models(self):
        return self.client.list()





