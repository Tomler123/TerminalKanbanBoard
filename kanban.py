import argparse
from board import Board
from task import Task
from ui import display_board
from tui import KanbanTUI

def main():
    board = Board()

    parser = argparse.ArgumentParser(description="Kanban Board CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task")

    move_parser = subparsers.add_parser("move", help="Move a task to a different status")
    move_parser.add_argument("task_id", type=int, help="Task ID")
    move_parser.add_argument("status", type=str, choices=["TODO","IN_PROGRESS","DONE"], help="New status")

    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--filter", type=str, choices=["TODO","IN_PROGRESS","DONE"], help="Filter tasks by status")
    list_parser.add_argument("--sort", type=str, choices=["priority","title"], help="Sort tasks by a field")

    tui_parser = subparsers.add_parser("tui", help="Launch interactive Kanban UI")

    args = parser.parse_args()

    if args.command == "add":
        board.add_task(Task(len(board.tasks) + 1, args.title, "TODO"))
    elif args.command == "move":
        board.move_task(args.task_id, args.status)
    elif args.command == "list":
        # board.list_tasks()
        filtered_tasks = board.filter_tasks(args.filter) if args.filter else board.tasks
        sorted_tasks = board.sort_tasks(filtered_tasks, args.sort) if args.sort else filtered_tasks
        display_board(board.tasks)
    elif args.command == "tui":
        app = KanbanTUI(board)
        app.run()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()





