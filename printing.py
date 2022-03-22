from rich import get_console
from rich.status import Status
from functools import wraps
from rich.progress import TimeElapsedColumn, Progress, SpinnerColumn

console = get_console()

print = console.print


def progress(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        prog = Progress(
            SpinnerColumn("clock", finished_text=":white_heavy_check_mark:"),
            f"[bold green]working on task {fn.__name__}[/bold green]",
            TimeElapsedColumn(),
        )
        with prog:
            task = prog.add_task(fn.__name__, total=1)
            result = fn(*args, **kwargs)
            prog.update(task, advance=1, finished="done")
        return result

    return wrapper
