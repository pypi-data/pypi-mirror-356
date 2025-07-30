"""Tab completion functionality for freetracker."""

import readline
from typing import List, Optional, Callable
from rich.prompt import Prompt
from rich.console import Console

console = Console()


class TabCompleter:
    """A generic tab completer for names."""
    
    def __init__(self, choices: List[str]):
        """Initialize with a list of choices for completion."""
        self.choices = [choice.lower() for choice in choices]
        self.original_choices = choices  # Keep original case
        self.matches = []
    
    def complete(self, text: str, state: int) -> Optional[str]:
        """Complete function for readline."""
        if state == 0:
            # Generate matches
            if text:
                self.matches = [
                    original for choice, original in zip(self.choices, self.original_choices)
                    if choice.startswith(text.lower())
                ]
            else:
                self.matches = self.original_choices[:]
        
        try:
            return self.matches[state]
        except IndexError:
            return None


def prompt_with_completion(prompt_text: str, choices: List[str], default: str = "") -> str:
    """Prompt for input with tab completion."""
    if not choices:
        # Fall back to regular prompt if no choices
        return Prompt.ask(prompt_text, default=default)
    
    # Set up tab completion
    completer = TabCompleter(choices)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    
    # Display available choices
    if len(choices) <= 10:  # Only show if not too many
        choices_str = ", ".join(f"[cyan]{choice}[/cyan]" for choice in choices)
        console.print(f"[dim]Available: {choices_str}[/dim]")
    else:
        console.print(f"[dim]Available choices: {len(choices)} items (use tab to complete)[/dim]")
    
    try:
        # Get input with readline (enables tab completion)
        if default:
            result = input(f"{prompt_text} [{default}]: ").strip()
            return result if result else default
        else:
            result = input(f"{prompt_text}: ").strip()
            return result
    except (EOFError, KeyboardInterrupt):
        console.print("\n[red]Cancelled[/red]")
        raise
    finally:
        # Clean up readline
        readline.set_completer(None)


def prompt_client_name(clients: List[str], prompt_text: str = "Client name") -> str:
    """Prompt for client name with tab completion."""
    return prompt_with_completion(prompt_text, clients)


def prompt_project_name(projects: List[str], prompt_text: str = "Project name") -> str:
    """Prompt for project name with tab completion."""
    return prompt_with_completion(prompt_text, projects)