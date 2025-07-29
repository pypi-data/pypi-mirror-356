"""Command-line interface for the Pomodoro timer."""

import typer
from typing import Optional
from pathlib import Path
from .timer import PomodoroTimer


def version_callback(value: bool):
    if value:
        from . import __version__
        typer.echo(f"tpom version {__version__}")
        raise typer.Exit()


def timer_main(
    minutes: Optional[int] = typer.Option(
        None,
        "--minutes",
        "-m",
        help="Duration of the Pomodoro session in minutes"
    ),
    sound_file: Optional[Path] = typer.Option(
        None,
        "--sound-file",
        "-s",
        help="Path to custom sound file",
        exists=True,
        file_okay=True,
        dir_okay=False
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    )
) -> None:
    """🍅 A simple and elegant Pomodoro timer for the command line.

    Start a Pomodoro session with the specified duration in minutes.
    The timer will count down and play a gentle alarm when finished.
    """
    # Prompt for minutes if not provided
    if minutes is None:
        minutes = typer.prompt("Enter time in minutes", type=int)

    try:
        timer = PomodoroTimer(sound_file=str(sound_file)
                              if sound_file else None)
        timer.start(minutes)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Abort()
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Abort()


def main():
    """Entry point for the CLI."""
    typer.run(timer_main)


if __name__ == "__main__":
    main()
