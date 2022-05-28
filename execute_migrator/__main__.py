from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction

from mcfunction import parse_command

from mcfunction.versions.mcbe_1_19.execute import ParsedExecuteCommand

EXECUTE_TEMPLATE_BASE = "execute as {0.target} at @s positioned {0.position} "
EXECUTE_TEMPLATE = EXECUTE_TEMPLATE_BASE + "run {run}"
EXECUTE_DETECT_TEMPLATE = (
    EXECUTE_TEMPLATE_BASE + "if block {0.detect_position} {0.block} {0.data} run {run}"
)


def migrate_execute(command_text: str) -> str:
    command: ParsedExecuteCommand = parse_command(command_text)

    run: str = command.run
    if run.startswith(("/execute", "execute")):
        run = migrate_execute(run.lstrip("/"))

    if command.detect is None:
        return EXECUTE_TEMPLATE.format(command, run=run)

    return EXECUTE_DETECT_TEMPLATE.format(command, run=run)


def default(parser: ArgumentParser, _):
    parser.print_help()


def migrate_text(parser: ArgumentParser, args: Namespace):
    print(migrate_execute(args.command))


def add_migrate_text(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser("text", help="指定した execute コマンドを移行する")
    parser.set_defaults(func=migrate_text)
    parser.add_argument("command", help="移行するコマンド")


def migrate_mcfunction(parser: ArgumentParser, args: Namespace):
    pass


def add_migrate_mcfunction(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser(
        "mcfunction", help=".mcfunction ファイル内の execute コマンドを移行する[WIP]"
    )
    parser.set_defaults(func=migrate_mcfunction)
    parser.add_argument("path", help=".mcfunction ファイル")


def main():
    parser = ArgumentParser(description="migrator")
    parser.set_defaults(func=default)

    subparser = parser.add_subparsers()
    add_migrate_text(subparser)
    add_migrate_mcfunction(subparser)

    args = parser.parse_args()
    args.func(parser, args)
