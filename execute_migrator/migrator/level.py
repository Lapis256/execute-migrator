from pathlib import Path
from tempfile import TemporaryDirectory

from amulet.api.chunk import Chunk
from amulet_nbt._int import IntTag
from amulet_nbt._string import StringTag
from amulet.level.formats.leveldb_world.format import LevelDBFormat
from tqdm import tqdm

from .str import migrate_execute
from .zip_utils import unzip_all, zip_all


def iter_chunk(level: LevelDBFormat):
    for dimension in level.dimensions:
        chunk_pos_set = level.all_chunk_coords(dimension)
        for cx, cz in chunk_pos_set:
            data = level.get_raw_chunk_data(cx, cz, dimension)
            interface = level._get_interface(data)
            yield (
                *level._decode(interface, dimension, cx, cz, data),
                interface,
                dimension,
            )


def iter_old_command_block_entity(chunk: Chunk):
    for entity in chunk.block_entities.values():
        if entity.base_name != "CommandBlock":
            continue
        version = entity.nbt.compound.get_int("Version").py_int
        if version >= 25:
            continue
        yield entity


def migrate_level(path: Path):
    level = LevelDBFormat(str(path))
    level.open()

    print(f"{level.level_name} の変換を開始します")
    print("チャンクを検索しています...")
    chunks = list(iter_chunk(level))
    print(f"{len(chunks)} 個のチャンクがヒットしました")
    print("execute コマンドとコマンドブロックの更新を開始します")
    for chunk, palette, interface, dimension in tqdm(chunks, position=0):
        for entity in iter_old_command_block_entity(chunk):
            compound = entity.nbt.compound
            command = compound.get_string("Command").py_str
            new_command = migrate_execute(command)
            if new_command is None:
                continue

            compound["Version"] = IntTag(25)
            compound["Command"] = StringTag(new_command)

            chunk.block_entities[entity.location] = entity

        data = level._encode(interface, chunk, dimension, palette)
        level._put_raw_chunk_data(chunk.cx, chunk.cz, data, dimension)

    level.close()

    print(f"{level.level_name} の変換を完了しました")


def migrate_level_zip(file: Path):
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        unzip_all(file, temp_path)
        migrate_level(temp_path)
        zip_all(file, temp_path)
