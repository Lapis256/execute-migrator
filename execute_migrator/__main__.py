from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction
from pathlib import Path
from typing import cast
import os

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


def default(parser: ArgumentParser, _):
    parser.print_help()


def migrate_text(parser: ArgumentParser, args: Namespace):
    migrated = migrate_execute(args.command)
    if migrated is None:
        print("コマンドを解析できませんでした。")
        return

    print(migrated)


def add_migrate_text(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser("text", help="指定した execute コマンドを移行する")
    parser.set_defaults(func=migrate_text)
    parser.add_argument("command", help="移行するコマンド")


def migrate_mcfunction(path: str | Path, out_path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    def migrate(cmd: str):
        if not cmd.startswith("execute"):
            return cmd

        migrated = migrate_execute(cmd)
        if migrated is None:
            return f"# 変換できませんでした。\n# {cmd}"
        return migrated

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(map(migrate, lines))


def migrate_function(parser: ArgumentParser, args: Namespace):
    path: str = args.path
    out_path: str | Path = args.output or path
    migrate_mcfunction(args.path, out_path)


def add_migrate_function(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser("function", help=".mcfunction 内の execute コマンドを移行する")
    parser.set_defaults(func=migrate_function)
    parser.add_argument("path", help=".mcfunction ファイル")
    parser.add_argument("-o", "--output", help="出力先ファイル")


def migrate_functions(parser: ArgumentParser, args: Namespace):
    path = Path(args.path)
    out_dir = Path(args.output or path)
    for file in path.glob("**/*.mcfunction"):
        if file.is_dir():
            continue
        relative_path = file.relative_to(path)
        out_path = out_dir.joinpath(relative_path)
        os.makedirs(out_path.parent, exist_ok=True)
        migrate_mcfunction(file, out_path)


def add_migrate_functions(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser("functions", help="指定ディレクトリ内の .mcfunction を一括で変換します。")
    parser.set_defaults(func=migrate_functions)
    parser.add_argument("path", help="ディレクトリ")
    parser.add_argument("-o", "--output", help="出力先ディレクトリ")


def migrate_world(parser: ArgumentParser, args: Namespace):
    pass


def add_migrate_world(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser("world", help="ワールドの内の execute コマンドを移行する[WIP]")
    parser.set_defaults(func=migrate_world)
    parser.add_argument("path", help="ワールドのディレクトリ")
    parser.add_argument("--ignore-npc", help="NPCを無視します。", action="store_true")
    parser.add_argument(
        "--ignore-command-block", help="コマンドブロックを無視します。", action="store_true"
    )
    parser.add_argument(
        "--ignore-minecart", help="コマンドブロック付きトロッコを無視します。", action="store_true"
    )


def main():
    parser = ArgumentParser(description="migrator")
    parser.set_defaults(func=default)

    subparser = parser.add_subparsers()
    add_migrate_text(subparser)
    add_migrate_function(subparser)
    add_migrate_functions(subparser)
    add_migrate_world(subparser)

    args = parser.parse_args()
    args.func(parser, args)
