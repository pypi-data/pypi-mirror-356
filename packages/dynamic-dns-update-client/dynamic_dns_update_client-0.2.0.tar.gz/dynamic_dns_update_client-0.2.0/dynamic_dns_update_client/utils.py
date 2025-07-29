"""Utilities."""

from subprocess import CalledProcessError, CompletedProcess, run


def execute_cli_command(arguments: list[str]) -> str:
    """Execute a command.

    :param arguments:
    :return:
    """
    result: CompletedProcess = run(
        arguments, capture_output=True, text=True, check=True
    )
    return result.stdout


def cli_command_exists(command: str) -> bool:
    """Get IP address for a network.

    :param command:
    :return:
    """
    try:
        execute_cli_command(["command", "-v", command])
        return True
    except CalledProcessError:
        return False
