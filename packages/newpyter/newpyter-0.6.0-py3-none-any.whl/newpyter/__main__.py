# CLI for newpyter
import sys
from pathlib import Path
from logging import getLogger
import nbformat
import io
from newpyter import parsing
from newpyter.config import get_storage_for_notebook


logger = getLogger(__file__)

usage = """
Usages:
python -m newpyter --to ipynb file1.newpy file2.newpy
python -m newpyter --to newpy file1.ipynb file2.ipynb
python -m newpyter debug   # shows used storage in cwd 

(if your env with newpyter is activated, you can skip 'python -m')
"""


def to_paths(files: list[str], expected_suffix: str) -> list[Path]:
    paths = [Path(f).absolute() for f in files]
    for f in paths:
        assert f.exists(), f"file {f} does not exist"
        assert f.suffix == expected_suffix, f"{expected_suffix=} not found in {f}"
    return paths


def convert_ipynb_to_newpy(ipynb_source: str, notebook_path: Path) -> str:
    storage = get_storage_for_notebook(notebook_path)
    notebook_node = nbformat.read(io.StringIO(ipynb_source), as_version=nbformat.current_nbformat)
    newpy_source = parsing.decompose_notebook(notebook_node, storage)
    return newpy_source


def convert_newpy_to_ipynb(newpy_source: str, notebook_path: Path) -> str:
    node = parsing.recompose_notebook(newpy_source, notebook_path=notebook_path)
    out = io.StringIO()
    nbformat.write(node, out)
    return out.getvalue()


def main():
    match list(sys.argv[1:]):
        case ["debug"]:
            from newpyter.config import get_storage_for_notebook

            storage = get_storage_for_notebook(notebook_filename=Path().joinpath("nonexistent.ipynb"))
            print(storage)
            return
        case ["stream-to-ipynb", newpy_file_path]:  # uses stdin/stdout
            ipynb_src = convert_newpy_to_ipynb(sys.stdin.read(), notebook_path=newpy_file_path)
            print(ipynb_src, end="")
            return

        case ["stream-to-newpy", newpy_file_path]:  # uses stdin/stdout
            newpy_src = convert_ipynb_to_newpy(sys.stdin.read(), notebook_path=newpy_file_path)
            print(newpy_src, end="")
            return
        case ["--to", output_format, *files]:
            input_suffix = {"ipynb": ".newpy", "newpy": ".ipynb"}[output_format]
            paths = to_paths(files, input_suffix)  # check all paths first

            for path in paths:
                logger.info(f"processing {path=}")
                if input_suffix == ".newpy":
                    output_content = convert_newpy_to_ipynb(path.read_text(), path)
                else:
                    assert input_suffix == ".ipynb"
                    output_content = convert_ipynb_to_newpy(path.read_text(), path.with_suffix(".newpy"))

                path.with_suffix(f".{output_format}").write_text(output_content)
                path.unlink()

            return
        case _:
            print(usage)
            exit(1)


if __name__ == "__main__":
    main()
