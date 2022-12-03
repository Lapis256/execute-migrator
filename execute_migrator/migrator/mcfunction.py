from pathlib import Path
import os

from tqdm import tqdm

from .str import migrate_execute


def migrate_mcfunction(path: Path, out_path: Path):
    print(f"{path} の変換を開始します")
    failed = _migrate_mcfunction(path, out_path)
    if len(failed) > 0:
        print("以下のコマンドを変換できませんでした")
    for line, command in failed.items():
        print(f"  - {line}行目 {command}".rstrip())
    print(f"{path} の変換を完了しました")


def _migrate_mcfunction(path: Path, out_path: Path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines: list[str] = []
    failed_lines: dict[int, str] = {}
    for index, line in enumerate(lines):
        if not line.startswith("execute"):
            new_lines.append(line)
            continue

        command = migrate_execute(line)
        if command is None:
            failed_lines[index + 1] = line
            command = line

        new_lines.append(command)

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return failed_lines


def migrate_mcfunctions(base_path: Path, output: Path):
    if base_path.is_file():
        print("ディレクトリを指定する必要があります")
        return

    print(f"{base_path} の変換を開始します\r")
    print(".mcfunction ファイルを探しています...")
    paths = list(base_path.glob("**/*.mcfunction"))
    if len(paths) <= 0:
        print("ヒットしませんでした。")
        return

    print(f"{len(paths)} 個の .mcfunction がヒットしました")
    print("execute コマンドを更新します...")
    for path in tqdm(paths):
        if path.is_dir():
            continue
        relative_path = path.relative_to(base_path)
        out_path = output.joinpath(relative_path)
        os.makedirs(out_path.parent, exist_ok=True)
        _migrate_mcfunction(path, out_path)

    print(f"{base_path} の変換を完了しました")
