from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Horizontal, Vertical
from textual.widgets import Input
from textual.events import Key
from rich.table import Table
from rich.text import Text
from rich.markup import escape

class KanbanTUI(App):
    def __init__(self, board):
        super().__init__()
        self.board = board  
        self.columns = ["TODO", "IN_PROGRESS", "DONE"]
        self.selected_column = 0
        self.selected_task_index = {col: 0 for col in self.columns}
        self.edit_mode = False
        self.input_field = None
        self.last_deleted_task = None

    def compose(self) -> ComposeResult:
        """Rebuild the UI dynamically each time a change occurs."""
        yield Header()
        self.layout = Horizontal(*self.render_columns())
        yield self.layout
        yield Footer()
    
    def render_columns(self):
        """Dynamically render columns using a better layout with a rich table."""
        table = Table(title="Kanban Board", expand=True)
        table.add_column("[bold cyan]TODO[/bold cyan]", justify="left", style="cyan", no_wrap=True)
        table.add_column("[bold yellow]IN PROGRESS[/bold yellow]", justify="left", style="yellow", no_wrap=True)
        table.add_column("[bold green]DONE[/bold green]", justify="left", style="green", no_wrap=True)

        max_rows = max(len(self.board.filter_tasks(col)) for col in self.columns)
        rows = [[] for _ in range(max_rows)]

        for col_index, status in enumerate(self.columns):
            tasks = self.board.filter_tasks(status)
            selected_index = self.selected_task_index[status]

            for row_index in range(max_rows):
                if row_index < len(tasks):
                    task_text = escape(f"[{tasks[row_index].id}] {tasks[row_index].title}")
                    if row_index == selected_index and col_index == self.selected_column:
                        task_text = f"[bold yellow]▶ {task_text}[/bold yellow]"
                else:
                    task_text = ""

                rows[row_index].append(task_text)

        for row in rows:
            table.add_row(*row)

        return [Static(table)]

    def move_selection(self, direction):
        """Move selection up/down within the current column."""
        current_status = self.columns[self.selected_column]
        tasks = self.board.filter_tasks(current_status)
        
        if not tasks:
            return
        
        if direction == "up":
            self.selected_task_index[current_status] = max(0, self.selected_task_index[current_status] - 1)
        elif direction == "down":
            self.selected_task_index[current_status] = min(len(tasks) - 1, self.selected_task_index[current_status] + 1)
        
        self.refresh_ui()

    def switch_column(self, direction):
        """Move selection left or right between columns."""
        if direction == "left" and self.selected_column > 0:
            self.selected_column -= 1
        elif direction == "right" and self.selected_column < len(self.columns) - 1:
            self.selected_column += 1

        self.refresh_ui()

    def move_task(self):
        """Move the selected task to the next column."""
        current_status = self.columns[self.selected_column]
        next_status_index = min(self.selected_column + 1, len(self.columns) - 1)
        next_status = self.columns[next_status_index]

        tasks = self.board.filter_tasks(current_status)
        
        if not tasks:
            return
        
        task = tasks[self.selected_task_index[current_status]]  
        task.status = next_status
        
        self.board.storage.save_tasks(self.board.tasks)  

        
        self.selected_task_index[next_status] = self.selected_task_index[current_status]
    
        
        if not self.board.filter_tasks(current_status):
            self.selected_task_index[current_status] = 0

        
        self.selected_column = next_status_index  

        self.refresh_ui() 

    def edit_task(self):
        current_status = self.columns[self.selected_column]
        tasks = self.board.filter_tasks(current_status)

        if not tasks:
            return
        
        task = tasks[self.selected_task_index[current_status]]
        
        self.edit_mode = True
        self.input_field = Input(placeholder="Edit Task Title...", value=task.title)
        self.mount(self.input_field)
        self.input_field.focus()

    
    def save_edited_task(self):
        if not self.edit_mode or not self.input_field:
            return

        current_status = self.columns[self.selected_column]
        tasks = self.board.filter_tasks(current_status)

        if not tasks:
            return

        task = tasks[self.selected_task_index[current_status]]
        task.title = self.input_field.value.strip()
    
        self.edit_mode = False
        self.input_field.remove()
        self.input_field = None
        self.board.storage.save_tasks(self.board.tasks) 
        self.refresh_ui() 

    def cancel_editing(self):
        if self.input_field:
            self.input_field.remove()
        self.edit_mode = False
        self.input_field = None
        self.refresh_ui()



    def delete_task(self):
        current_status = self.columns[self.selected_column]
        tasks = self.board.filter_tasks(current_status)

        if not tasks:
            return    
        task_to_delete = tasks[self.selected_task_index[current_status]]

        self.last_deleted_task = task_to_delete  

        self.board.tasks = [task for task in self.board.tasks if task.id != task_to_delete.id]

        self.board.storage.save_tasks(self.board.tasks)

        if self.selected_task_index[current_status] >= len(self.board.filter_tasks(current_status)):
            self.selected_task_index[current_status] = max(0, len(self.board.filter_tasks(current_status)) - 1)

        self.refresh_ui()
    def undo_delete(self):
        if not self.last_deleted_task:
            return     
        self.board.tasks.append(self.last_deleted_task)

        self.board.storage.save_tasks(self.board.tasks)

        self.last_deleted_task = None  

        self.refresh_ui()  

   
    def on_key(self, event):
        if self.edit_mode:
            if event.key == "enter":
                self.save_edited_task()
            elif event.key == "escape":
                self.cancel_editing()
            return 
    
        if event.key == "q":
            self.exit()
        elif event.key == "up":
            self.move_selection("up")
        elif event.key == "down":
            self.move_selection("down")
        elif event.key == "left":
            self.switch_column("left")
        elif event.key == "right":
            self.switch_column("right")
        elif event.key == "enter":
            self.move_task()
        elif event.key == "e":
            self.edit_task()
        elif event.key == "d":
            self.delete_task() 
        elif event.key == "ctrl+z":
            self.undo_delete()



    def refresh_ui(self):
        self.layout.remove_children() 
        self.layout.mount(*self.render_columns())

    def run(self):
        super().run()

