import argparse, subprocess

from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

from unrun.utils.console import console, error, warning
from unrun.utils.loader import load_scripts
from unrun.utils.parser import parse_extra, parse_command
from unrun.utils.selector import select
from unrun.utils.config import setup_config


def main():
    parser = argparse.ArgumentParser(
        description="Run commands from `.yaml` files using unrun.",
        epilog="Example: unrun my_command",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("key", nargs="?", default=None, help="The key of the command to run from `.yaml`")
    parser.add_argument("--include", "-i", nargs="*", default=None, help="Include specific keys from the `.yaml`")
    parser.add_argument("--exclude", "-e", nargs="*", default=None, help="Exclude specific keys from the `.yaml`")
    parser.add_argument("--file", "-f", default=None, help="Path to the `.yaml`")
    parser.add_argument("extra", nargs="*", help="Extra arguments to pass to the command")
    args, unknown = parser.parse_known_args()
    config = setup_config(args)

    key = args.key
    extra = parse_extra(args.extra, unknown)

    scripts = load_scripts(config["file"])
    if scripts is None:
        return

    commands = parse_command(key, scripts)
    if commands is None:
        return

    command = select(commands)
    if command is None:
        warning("No command selected. Exiting.")
        return

    if extra:
        command += f" {extra}"

    console.print(
        Panel(
            Syntax(command, "bash", word_wrap=True),
            title=Text(f"Running command for key '{args.key}'", style="bold blue"),
        )
    )

    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        error(
            f"An unexpected error occurred:\n{e}",
            title="Unexpected Error"
        )
