#
# MIT License
#
# Copyright (c) 2024-2025 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
Testing Against Learned Reference Data.

# Concept

A unit test creates files in a temporary folder `tmp_path`.
:any:`assert_refdata()` is called at the end of the test.

There are two modes:

* **Testing**: Test result in `tmp_path` is compared against a known reference.
  Any deviation in the files, causes a fail.
* **Learning**: The test result in `tmp_path` is taken as reference and is copied
  to the reference folder, which should be committed to version control and kept as
  reference.

The file `.test2ref` in the project root directory selects the operation mode.
If the file exists, **Learning Mode** is selected.
If the files does **not** exists, the **Testing Mode** is selected.

Next to that, stdout, stderr and logging can be included in the reference automatically.

# Minimal Example

!!! example

    ```python
    >>> def test_something(tmp_path, capsys):
    ...     (tmp_path / "file.txt").write_text("Hello Mars")
    ...     print("Hello World")
    ...     assert_refdata(test_something, tmp_path, capsys=capsys)

    ```

# API
"""

import os
import re
import site
import subprocess
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from shutil import copytree, ignore_patterns, rmtree
from tempfile import TemporaryDirectory
from typing import Any, TypeAlias

from binaryornot.check import is_binary

PRJ_PATH = Path.cwd()

Search: TypeAlias = Path | str | re.Pattern
"""
Possible Search Pattern.

File System Path, string or regular expression.
"""

Replacements: TypeAlias = Iterable[tuple[Search, str]]
"""
Replacements - Pairs of Search Pattern and Things to be Replaced.
"""

StrReplacements: TypeAlias = Iterable[tuple[str, str]]
Excludes: TypeAlias = tuple[str, ...]


DEFAULT_REF_PATH: Path = PRJ_PATH / "tests" / "refdata"
DEFAULT_REF_UPDATE: bool = (PRJ_PATH / ".test2ref").exists()
DEFAULT_EXCLUDES: Excludes = ("__pycache__", ".tool_cache", ".cache")
DEFAULT_IGNORE_SPACES: bool = False
CONFIG = {
    "ref_path": DEFAULT_REF_PATH,
    "ref_update": DEFAULT_REF_UPDATE,
    "excludes": DEFAULT_EXCLUDES,
    "ignore_spaces": DEFAULT_IGNORE_SPACES,
}
ENCODING = "utf-8"
ENCODING_ERRORS = "surrogateescape"


def configure(
    ref_path: Path | None = None,
    ref_update: bool | None = None,
    excludes: Excludes | None = None,
    add_excludes: Excludes | None = None,
    rm_excludes: Excludes | None = None,
    ignore_spaces: bool | None = False,
) -> None:
    """
    Configure.

    Keyword Args:
        ref_path: Path for reference files. "tests/refdata" by default
        ref_update: Update reference files. True by default if `.test2ref` file exists.
        excludes: Paths to be excluded in all runs.
        add_excludes: Additionally Excluded Files
        rm_excludes: Not Excluded Files
        ignore_spaces: Ignore Space Changes - `False` by default
    """
    if ref_path is not None:
        CONFIG["ref_path"] = ref_path
    if ref_update is not None:
        CONFIG["ref_update"] = ref_update
    if excludes:
        CONFIG["excludes"] = excludes
    if add_excludes:
        CONFIG["excludes"] = (*CONFIG["excludes"], *add_excludes)
    if rm_excludes:
        CONFIG["excludes"] = tuple(exclude for exclude in CONFIG["excludes"] if exclude not in rm_excludes)  # type: ignore[attr-defined]
    if ignore_spaces is not None:
        CONFIG["ignore_spaces"] = ignore_spaces


def assert_refdata(
    arg: Callable | Path,
    path: Path,
    capsys: Any = None,
    caplog: Any = None,
    replacements: Replacements | None = None,
    excludes: Iterable[str] | None = None,
    flavor: str = "",
) -> None:
    """
    Compare Output of `arg` generated at `path` with reference.

    Use `replacements` to mention things which vary from test to test.
    `path` and the project location are already replaced by default.

    Args:
        arg: Test Function or Path to reference data
        path: Path with generated files to be compared.

    Keyword Args:
        capsys: pytest `capsys` fixture. Include `stdout`/`stderr` too.
        caplog: pytest `caplog` fixture. Include logging output too.
        replacements: pairs of things to be replaced.
        excludes: Files and directories to be excluded.
        flavor: Flavor for different variants.

    !!! example "Minimal Example"

        ```python
        def test_example(tmp_path):
            (tmp_path / "file.txt").write_text("Content")
            assert_refdata(test_example, tmp_path)
        ```

    !!! example "Full Example"

        ```python
        import logging

        def test_example(tmp_path, capsys, caplog):
            (tmp_path / "file.txt").write_text("Content")

            # print on standard-output - captured by capsys
            print("Hello World")

            # logging - captured by caplog
            logging.getLogger().warning("test")

            assert_refdata(test_example, tmp_path, capsys=capsys, caplog=caplog)
        ```

    """
    ref_basepath: Path = CONFIG["ref_path"]  # type: ignore[assignment]
    if isinstance(arg, Path):
        ref_path = ref_basepath / arg
    else:
        ref_path = ref_basepath / arg.__module__ / arg.__name__
    if flavor:
        ref_path = ref_path / flavor
    ref_path.mkdir(parents=True, exist_ok=True)
    rplcs: Replacements = replacements or ()  # type: ignore[assignment]
    path_rplcs: StrReplacements = [(srch, rplc) for srch, rplc in rplcs if isinstance(srch, str)]
    sitepaths = (*site.getsitepackages(), site.getusersitepackages())

    gen_rplcs: Replacements = [
        *((Path(path) / "Lib" / "site-packages", "$SITE") for path in sitepaths),  # dirty hack for win
        *((Path(path), "$SITE") for path in sitepaths),
        (PRJ_PATH, "$PRJ"),
        (path, "$GEN"),
        *rplcs,
        (Path.home(), "$HOME"),
    ]
    gen_excludes: Excludes = (*CONFIG["excludes"], *(excludes or []))

    with TemporaryDirectory() as temp_dir:
        gen_path = Path(temp_dir)

        ignore = ignore_patterns(*gen_excludes)
        copytree(path, gen_path, dirs_exist_ok=True, ignore=ignore)

        _replace_path(gen_path, path_rplcs)

        if capsys:
            captured = capsys.readouterr()
            (gen_path / "stdout.txt").write_text(captured.out, encoding=ENCODING, errors=ENCODING_ERRORS)
            (gen_path / "stderr.txt").write_text(captured.err, encoding=ENCODING, errors=ENCODING_ERRORS)

        if caplog:
            logpath = gen_path / "logging.txt"
            with logpath.open("w", encoding=ENCODING, errors=ENCODING_ERRORS) as file:
                for record in caplog.records:
                    file.write(f"{record.levelname:7s}  {record.name}  {record.message}\n")
            caplog.clear()

        _remove_empty_dirs(gen_path)

        _replace_content(gen_path, gen_rplcs)

        if CONFIG["ref_update"]:
            rmtree(ref_path, ignore_errors=True)
            copytree(gen_path, ref_path)

        assert_paths(ref_path, gen_path, excludes=excludes)


def assert_paths(ref_path: Path, gen_path: Path, excludes: Iterable[str] | None = None) -> None:
    """
    Compare Output of `ref_path` with `gen_path`.

    Args:
        ref_path: Path with reference files to be compared.
        gen_path: Path with generated files to be compared.

    Keyword Args:
        excludes: Files and directories to be excluded.
    """
    diff_excludes: Excludes = (*CONFIG["excludes"], *(excludes or []))
    try:
        cmd = ["diff", "-ru", "--strip-trailing-cr", str(ref_path), str(gen_path)]
        for exclude in diff_excludes:
            cmd.extend(("--exclude", exclude))
        if CONFIG["ignore_spaces"]:
            cmd.append("-b")
        subprocess.run(cmd, check=True, capture_output=True)  # noqa: S603
    except subprocess.CalledProcessError as error:
        raise AssertionError(error.stdout.decode("utf-8")) from None


def _remove_empty_dirs(path: Path) -> None:
    """Remove Empty Directories within ``path``."""
    for sub_path in tuple(path.glob("**/*")):
        if not sub_path.exists() or not sub_path.is_dir():
            continue
        sub_dir = sub_path
        while sub_dir != path:
            is_empty = not any(sub_dir.iterdir())
            if is_empty:
                sub_dir.rmdir()
                sub_dir = sub_dir.parent
            else:
                break


def _replace_path(path: Path, replacements: StrReplacements) -> None:
    paths = [path]
    while paths:
        path = paths.pop()
        orig = name = path.name
        for srch, rplc in replacements:
            name = name.replace(srch, rplc)
        if orig != name:
            path = path.replace(path.with_name(name))
        if path.is_dir():
            paths.extend(path.iterdir())


def _replace_content(path: Path, replacements: Replacements) -> None:
    """Replace ``replacements`` for text files in ``path``."""
    # pre-compile regexs and create substitution functions
    regex_funcs = tuple(_create_regex_funcs(replacements))
    # search files and replace
    for sub_path in tuple(path.glob("**/*")):
        if not sub_path.is_file() or is_binary(str(sub_path)):
            continue
        content = sub_path.read_text(encoding=ENCODING, errors=ENCODING_ERRORS)
        total = 0
        for regex, func in regex_funcs:
            content, counts = regex.subn(func, content)
            total += counts
        if total:
            sub_path.write_text(content, encoding=ENCODING, errors=ENCODING_ERRORS)


def _create_regex_funcs(replacements: Replacements) -> Iterator[tuple[re.Pattern, Callable]]:
    """Create Regular Expression for `search`."""
    for search, replace in replacements:
        # already regex
        if isinstance(search, re.Pattern):
            yield search, _substitute_str(replace)

        # Path
        elif isinstance(search, Path):
            search_str = str(search)
            sep_esc = re.escape(os.sep)

            if os.altsep:
                doublesep = f"{os.sep}{os.sep}"

                search_repr = search_str.replace(os.sep, doublesep)
                doubleregex = rf"(?i){re.escape(search_repr)}([A-Za-z0-9\-_{sep_esc}{re.escape(os.altsep)}]*)\b"
                yield re.compile(f"{doubleregex}"), _substitute_path(replace, (doublesep, os.sep, os.altsep))

                altregex = rf"(?i){re.escape(search.as_posix())}([A-Za-z0-9\-_{sep_esc}{re.escape(os.altsep)}]*)\b"
                yield re.compile(f"{altregex}"), _substitute_path(replace, (os.sep, os.altsep))
                regex = rf"(?i){re.escape(search_str)}([A-Za-z0-9_{sep_esc}]*)\b"
            else:
                regex = rf"{re.escape(search_str)}([A-Za-z0-9_{sep_esc}]*)\b"
            yield re.compile(f"{regex}"), _substitute_path(replace, (os.sep,))

        # str
        else:
            yield re.compile(re.escape(search)), _substitute_str(replace)


def _substitute_path(replace: str, seps: tuple[str, ...] = ()):
    """Factory for Substitution Function."""

    def func(mat: re.Match) -> str:
        sub = mat.group(1)
        for sep in seps:
            sub = sub.replace(sep, "/")
        return f"{replace}{sub}"

    return func


def _substitute_str(replace: str):
    def func(mat: re.Match) -> str:
        return replace

    return func
