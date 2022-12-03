from typing import cast

from mcfunction import parse_command
from mcfunction.exceptions import ParserException
from mcfunction.versions.mcbe_1_19.execute import ParsedExecuteCommand


EXECUTE_TEMPLATE_BASE = "execute as {0.target} at @s positioned {0.position} "
EXECUTE_TEMPLATE = EXECUTE_TEMPLATE_BASE + "run {run}"
EXECUTE_DETECT_TEMPLATE = (
    EXECUTE_TEMPLATE_BASE + "if block {0.detect_position} {0.block} {0.data} run {run}"
)


def migrate_execute(command_text: str) -> str | None:
    pure_command_text = command_text.lstrip("/")
    try:
        command = cast(ParsedExecuteCommand, parse_command(pure_command_text))
    except ParserException:
        return

    run: str = str(command.run)
    if run.startswith(("/execute", "execute")):
        run = str(migrate_execute(run))

    if command.detect is None:
        return EXECUTE_TEMPLATE.format(command, run=run)

    return EXECUTE_DETECT_TEMPLATE.format(command, run=run)
