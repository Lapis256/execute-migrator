from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction
from pathlib import Path

from .migrator import (
    migrate_execute,
    migrate_mcfunction,
    migrate_mcfunctions,
    migrate_level,
    migrate_level_zip,
)


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


def migrate_function(_, args: Namespace):
    out_path = Path(args.output or args.path)
    migrate_mcfunction(Path(args.path), out_path)


def add_migrate_function(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser("function", help=".mcfunction 内の execute コマンドを移行する")
    parser.set_defaults(func=migrate_function)
    parser.add_argument("path", help=".mcfunction ファイル")
    parser.add_argument("-o", "--output", help="出力先ファイル")


def migrate_functions(_, args: Namespace):
    out_dir = Path(args.output or args.path)
    migrate_mcfunctions(Path(args.path), out_dir)


def add_migrate_functions(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser("functions", help="指定ディレクトリ内の .mcfunction を一括で変換します。")
    parser.set_defaults(func=migrate_functions)
    parser.add_argument("path", help="ディレクトリ")
    parser.add_argument("-o", "--output", help="出力先ディレクトリ")


def migrate_world(parser: ArgumentParser, args: Namespace):
    migrate_level(Path(args.path))


def add_migrate_world(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser("world", help="ワールドの内の execute コマンドを移行する")
    parser.set_defaults(func=migrate_world)
    parser.add_argument("path", help="ワールドのディレクトリ")
    # parser.add_argument("--ignore-npc", help="NPCを無視します。", action="store_true")
    # parser.add_argument(
    #     "--ignore-command-block", help="コマンドブロックを無視します。", action="store_true"
    # )
    # parser.add_argument(
    #     "--ignore-minecart", help="コマンドブロック付きトロッコを無視します。", action="store_true"
    # )


def migrate_mcworld(parser: ArgumentParser, args: Namespace):
    path = Path(args.path)
    migrate_level_zip(path)


def add_migrate_mcworld(subparser: _SubParsersAction[ArgumentParser]):
    parser = subparser.add_parser("mcworld", help=".mcworld ファイルの内の execute コマンドを移行する")
    parser.set_defaults(func=migrate_mcworld)
    parser.add_argument("path", help="ワールドのディレクトリ")
    # parser.add_argument("--ignore-npc", help="NPCを無視します。", action="store_true")
    # parser.add_argument(
    #     "--ignore-command-block", help="コマンドブロックを無視します。", action="store_true"
    # )
    # parser.add_argument(
    #     "--ignore-minecart", help="コマンドブロック付きトロッコを無視します。", action="store_true"
    # )


def main():
    parser = ArgumentParser(description="migrator")
    parser.set_defaults(func=default)

    subparser = parser.add_subparsers()
    add_migrate_text(subparser)
    add_migrate_function(subparser)
    add_migrate_functions(subparser)
    add_migrate_world(subparser)
    add_migrate_mcworld(subparser)

    args = parser.parse_args()
    args.func(parser, args)
