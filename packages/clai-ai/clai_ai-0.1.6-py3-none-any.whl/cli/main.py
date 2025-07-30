


import typer

from rich.console import Console
from typing import Optional
from cli.git_handler import GitHandler
from rich.panel import Panel
from rich.text import Text
from cli.explainer import CodeExplainer
from cli.config import ConfigManager

app = typer.Typer(
    name="clay",
    help="Clay: CLI + AI - Smart Git automation and code explanation tool",
    add_completion=True,
    rich_markup_mode="rich",  
)


console = Console()

def version_callback(value: bool):
    if value:
        console.print("Clay CLI v0.1.0", style="bold green")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, help="Show version"
    ),
):
    """Clay: CLI + AI - Smart Git automation and code explanation tool"""
    if version:
        return  # version_callback will handle this
    
    # This will be shown when no command is provided
    console.print(Panel(
        "[bold green]Clay: CLI + AI[/bold green] - Smart Git automation and code explanation tool\n\n"
        "[bold]Usage:[/bold]\n"
        "  clay [command] [options]\n\n"
        "[bold]Available Commands:[/bold]\n"
        "  • [bold]commit[/bold] - Generate AI-powered commit messages\n"
        "  • [bold]config[/bold] - Configure API keys and settings\n\n"
        "Run [bold]clay --help[/bold] for more information about available commands.",
        title="Welcome to Clay",
        border_style="blue"
    ))


@app.command(rich_help_panel="Configuration")
def config(api_key:Optional[str]=typer.Option(None,"--api-key",help="set Gemini API key"),show:Optional[bool]=typer.Option(None,"--show",help="show Current Configuration")):
    
    config_manager = ConfigManager()
    if show:
        config_data= config_manager.get_config()
        if config_data.get('api_key'):
            masked_key = config_data['api_key'][:8] + "..." + config_data['api_key'][-4:]
            console.print(f"✅ API Key: {masked_key}", style="green")
        else:
            console.print("❌ No API key configured", style="red")
        return


    if api_key:
        config_manager.set_api_key(api_key)
    else:
        # Interactive prompt for API key
        api_key = typer.prompt("Enter your Gemini API key", hide_input=True)
        config_manager.set_api_key(api_key)
        console.print("✅ API key saved successfully!", style="green")

    

@app.command(rich_help_panel="Git Operations")  # Group commands in panels
def commit(message:Optional[str]=typer.Option(None,"--message",'-m',help="custom commit message"),no_push : Optional[bool] = typer.Option(False,"--no-push",help="don't push after commit"),auto_push:Optional[bool]=typer.Option(False,"--auto-push",help="auto push after commit")):
    config_manger =ConfigManager()
    if not config_manger.get_api_key():
        console.print("❌ No API key configured. Run 'clay config --api-key YOUR_KEY' first.", style="red")
        raise typer.Exit(1)
    try:
        git_handler = GitHandler()
        if not git_handler.is_git_repo():
            console.print("❌ Current directory is not a Git repository.", style="red")
            raise typer.Exit(1)
        
                
        # Check for staged changes
        if not git_handler.has_staged_changes():
            console.print("❌ No staged changes to commit!", style="yellow")
            console.print("💡 Stage your changes with 'git add' first.", style="blue")
            raise typer.Exit(1)
        
        console.print("🔍 Analyzing staged changes...", style="blue")

        if message:
            commit_msg = message
        else:
            # Generate AI commit message
            explainer = CodeExplainer()
            commit_msg = explainer.generate_commit_message()
        
        # Show commit message and confirm
        console.print(Panel(
            Text(commit_msg, style="white"),
            title="📝 Proposed Commit Message",
            border_style="blue"
        ))

        if not typer.confirm("Proceed with this commit?"):
            console.print("❌ Commit cancelled.", style="yellow")
            raise typer.Exit()
        
        # Perform commit
        console.print("💾 Committing changes...", style="blue")
        git_handler.commit(commit_msg)
        console.print("✅ Changes committed successfully!", style="green")
        
        # Handle push
        current_branch = git_handler.get_current_branch()
        if not no_push:
            should_push = auto_push or typer.confirm(f"Push to '{current_branch}' branch?")
            if should_push:
                console.print(f"🚀 Pushing to {current_branch}...", style="blue")
                git_handler.push()
                console.print("✅ Changes pushed successfully!", style="green")

    except Exception as e:
        console.print(f"❌ Error: {str(e)}", style="red")
        raise typer.Exit(1)

      

    pass

if __name__ == "__main__":
    app()