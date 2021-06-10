from zipfile import ZipFile
import pathlib
import shutil


def unzip_file(zipped_file: pathlib.Path):
    # unzip a gdb folder to a parent folder and return new path
    output_folder = zipped_file.parent
    # remove if folder exists
    shutil.rmtree(zipped_file.parent / zipped_file.stem, ignore_errors=True)
    with ZipFile(zipped_file, "r") as zip_ref:
        zip_ref.extractall(output_folder)
    return zipped_file.parent / zipped_file.stem