from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path


def unzip_all(file: Path, path: Path):
    with ZipFile(file) as zip:
        zip.extractall(path)


def zip_all(file: Path, path: Path):
    with ZipFile(file, "w", compression=ZIP_DEFLATED) as new_zip:
        for temp in path.glob("**/*"):
            relative = temp.relative_to(path)
            if temp.is_dir():
                new_zip.mkdir(str(relative))
                continue
            new_zip.write(temp, relative)
