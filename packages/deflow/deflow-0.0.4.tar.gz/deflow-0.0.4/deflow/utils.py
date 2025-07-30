import os
from pathlib import Path
from typing import Optional

from ddeutil.core import merge_list
from ddeutil.io import YamlEnvFl, is_ignored, read_ignore

from .__types import DictData


def get_data(name: str, path: Path):
    _dir: Path
    ignore: list[str] = read_ignore(path / ".confignore")
    target_dir: Optional[Path] = None
    for _dir in path.glob("*"):

        if _dir.is_file() and _dir.name == ".confignore":
            continue

        if is_ignored(_dir, ignore):
            continue

        for file in _dir.rglob("*"):

            if is_ignored(file, ignore):
                continue

            if file.is_file():
                continue

            if file.is_dir() and file.name == name:
                target_dir = file

    if target_dir is None:
        raise FileNotFoundError(f"Does not found dir name: {name!r}")

    sub_ignore: list[str] = read_ignore(target_dir / ".confignore")
    all_ignore: list[str] = list(set(merge_list(ignore, sub_ignore)))

    conf_data: Optional[DictData] = None
    child_paths: list[str] = []
    for file in target_dir.rglob("*"):

        if is_ignored(file, all_ignore):
            continue

        if file.stem == "config":
            conf_data = read_conf(file)
            continue

        if file.stem == "variables":
            continue

        if not file.is_file():
            continue

        relate_path_str = (
            str(file.relative_to(path)).split(name)[-1].lstrip(os.sep)
        )
        child_paths.append(relate_path_str)
        # print(file.relative_to(path))

    print(conf_data)

    if not conf_data:
        raise FileNotFoundError("Config file does not exists.")

    return {
        "conf": conf_data,
        "child": child_paths,
    }


def read_conf(path: Path) -> DictData:
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exists.")

    if path.suffix in (".yml", ".yaml"):
        data: DictData = YamlEnvFl(path).read()
        if not data:
            raise NotImplementedError("Config was empty")

        if len(data) > 1:
            return {"name": path.parent.name, **data}

        first_key: str = next(iter(data.keys()))
        return {"name": first_key, **data[first_key]}

    raise NotImplementedError(
        f"Config file format: {path.suffix!r} does not support yet."
    )
