from rich.console import Console
from rich.table import Table

def display_board(tasks):
    console = Console()
    table = Table(title="Kanban Board")

    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="green")

    for task in tasks:
        table.add_row(str(task.id), task.title, task.status)

    console.print(table)
