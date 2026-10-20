import shutil
import tomllib
from importlib.util import find_spec
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    with (root / "zensical.toml").open("rb") as file:
        config = tomllib.load(file)

    for module in config["project"]["plugins"]["api-autonav"]["modules"]:
        destination = root / module
        spec = find_spec(destination.name)
        if spec is None or spec.origin is None:
            raise ModuleNotFoundError(
                f"{destination.name} is not installed; run uv sync first"
            )

        source = Path(spec.origin).parent.resolve()
        if destination.is_symlink():
            destination.unlink()
        elif destination.exists():
            shutil.rmtree(destination)
        # Zensical excludes sources under .venv, including symlink targets.
        shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__"))
        print(f"{destination.name}: {source}")


if __name__ == "__main__":
    main()
