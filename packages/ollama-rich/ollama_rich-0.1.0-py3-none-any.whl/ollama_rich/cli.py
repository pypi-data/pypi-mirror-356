import argparse
from rich.console import Console
from rich.table import Table
from ollama_rich.ollama_rich import OllamaRichClient
from ollama_rich.utils import to_gb

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Ollama Client CLI with Rich UI")
    parser.add_argument('--host', default='http://127.0.0.1:11343', help='Ollama server host URL')
    subparsers = parser.add_subparsers(dest="command")

    # List models
    subparsers.add_parser("models", help="List all available models")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with a model")
    chat_parser.add_argument("model", help="Model name")
    chat_parser.add_argument("message", help="Message to send to the model")
    chat_parser.add_argument("--stream", action="store_true", help="Stream the response live")

    args = parser.parse_args()
    client = OllamaRichClient(host=args.host)

    if args.command == "models":
        models = client.models()
        if 'models' in models:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Model", style="red")
            table.add_column("Size (GB)", style="blue")
            table.add_column("Parameters", style="green")
            for model in models['models']:
                table.add_row(
                    model.get('model', ''),
                    f"{to_gb(model.get('size', 0))}",
                    str(model.get('details', {}).get('parameter_size', ''))
                )
            console.print(table)
        else:
            console.print("[red]No models found.[/red]")
    elif args.command == "chat":
        messages = [{"role": "user", "content": args.message}]
        if args.stream:
            client.chat_and_display(args.model, messages)
        else:
            md = client.chat(args.model, messages)
            console.print(md)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
