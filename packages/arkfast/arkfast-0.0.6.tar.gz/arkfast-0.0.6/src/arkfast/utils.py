import os
import runpy
import zipfile
import shutil
import logging
import logging.config
import sys
from pathlib import Path
import toml


def handler(signal_code, _) -> None:
    """Signal handler."""
    logging.debug(f"Shutting down because signal {signal_code} was received.")
    sys.exit(1)


def read_toml(file_path: Path) -> dict:
    """Return the contents of a toml file as a dictionary."""
    if not file_path.exists():
        logging.critical(f"{file_path} does not exist!")
        sys.exit(1)
    try:
        return dict(toml.loads(file_path.read_text()))
    except (toml.TomlDecodeError, TypeError) as error:
        logging.critical(f"Toml format error: {error}.")
        sys.exit(1)


class TemporaryTemplatedPath:
    def __init__(self, template_file_path: Path | str | None, extraction_path: Path | str, remove_after_completion: bool = True):
        self.template_file_path = Path(template_file_path) if isinstance(template_file_path, str) else template_file_path
        self.extraction_path = extraction_path if isinstance(extraction_path, Path) else Path(extraction_path)
        self.remove_after_completion = remove_after_completion

    def __enter__(self):
        if not self.template_file_path:
            return self.extraction_path
        elif self.template_file_path.suffix == ".git":
            shutil.copytree(self.template_file_path, self.extraction_path)
        elif self.template_file_path.suffix == ".zip":
            with zipfile.ZipFile(self.template_file_path) as zip_file:
                zip_file.extractall(self.extraction_path)
        elif self.template_file_path.is_dir():
            shutil.copytree(self.template_file_path, self.extraction_path)
        elif self.template_file_path.is_file():
            self.extraction_path.parent.mkdir(parents=True, exist_ok=True) # This will cause the made directories to be left after cleanup.
            shutil.copyfile(self.template_file_path, self.extraction_path)
        else:
            raise ValueError(f"Unexpected extension '{self.template_file_path.suffix}'.")
        return self.extraction_path

    def __exit__(self, exc_type, exc_value, traceback):
        if self.remove_after_completion:
            try:
                if self.extraction_path.is_dir():
                    shutil.rmtree(self.extraction_path)
                elif self.extraction_path.is_file():
                    os.remove(self.extraction_path)
            except FileNotFoundError:
                pass

class TemporaryPath(TemporaryTemplatedPath):
    def __init__(self, path: Path | str, remove_after_completion: bool = True):
        super().__init__(None, path if isinstance(path, Path) else Path(path), remove_after_completion)

def run_module(path_to_script: Path):
    original_cwd = Path.cwd()
    try:
        os.chdir(path_to_script)
        runpy.run_path(str(path_to_script))
    finally:
        os.chdir(original_cwd)
