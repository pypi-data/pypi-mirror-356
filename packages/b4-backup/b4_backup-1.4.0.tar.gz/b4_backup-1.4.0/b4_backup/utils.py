"""A collection of Helper functions."""

import logging
import os
from pathlib import Path, PurePath

from omegaconf import OmegaConf, SCMode
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

from b4_backup.config_schema import DEFAULT, BaseConfig

log = logging.getLogger("b4_backup.utils")

DEFAULT_CONFIG = Path(os.getenv("B4_BACKUP_CONFIG", str(BaseConfig.config_path)))

DEFAULT_THEME = Theme(
    {
        "logging.level.debug": "blue",
        "logging.level.info": "green",
        "logging.level.warning": "yellow",
        "logging.level.error": "red",
        "logging.level.critical": "reverse red",
    }
)
CONSOLE = Console(theme=DEFAULT_THEME)


# Dynamically imported by logging.config.dictConfig
def rich_handler() -> RichHandler:
    """Used in the logging config to use a customized RichHandler."""
    return RichHandler(console=CONSOLE)


def resolve_parent_dir(path: str) -> str:
    """
    This resolver (parent_dir) can be used in OmegaConf configs to return the parent directory or the directory of a file.

    Args:
        path: Name of the file or directory

    Returns:
        Parent directory
    """
    return str(PurePath(path).parent)


def resolve_from_file(path: str) -> str:
    """
    This resolver (from_file) can be used in OmegaConf configs to use the raw content of a file as an input.

    Args:
        path: Input file path

    Returns:
        File content
    """
    return Path(path).read_text(encoding="utf8").strip()


def _copy_from_default_retention(config: BaseConfig):
    for target in config.backup_targets.values():
        for (
            retention_name,
            retention,
        ) in config.backup_targets[DEFAULT].src_retention.items():
            if retention_name not in target.src_retention:
                target.src_retention[retention_name] = retention

        for (
            retention_name,
            retention,
        ) in config.backup_targets[DEFAULT].dst_retention.items():
            if retention_name not in target.dst_retention:
                target.dst_retention[retention_name] = retention


def load_config(
    config_path: Path = DEFAULT_CONFIG, overrides: list[str] | None = None
) -> BaseConfig:
    """
    Reads the config file and returns a config dataclass.

    Args:
        config_path: Path of the config file
        overrides:
            A list of dot list entries, which can override the values in the config.
            Used for CLI.

    Returns:
        Config object
    """
    overrides = overrides or []

    config_path = config_path.expanduser()
    config_path.parent.mkdir(exist_ok=True, parents=True)
    _ = config_path.exists() or config_path.touch()

    if not OmegaConf.has_resolver("from_file"):
        OmegaConf.register_new_resolver("from_file", resolve_from_file)
        OmegaConf.register_new_resolver("parent_dir", resolve_parent_dir)

    base_conf = OmegaConf.merge(
        OmegaConf.structured(BaseConfig),
        OmegaConf.load(config_path),
        OmegaConf.from_dotlist(overrides),
    )

    # Templates shouldn't fail, if there is a value missing
    base_conf.backup_targets[DEFAULT].source = "NONE"

    # pylance doesn't understand here that it's actually a config_schema.BaseConfig type
    base_conf_instance: BaseConfig = OmegaConf.to_container(  # type: ignore
        base_conf, structured_config_mode=SCMode.INSTANTIATE, resolve=True
    )

    base_conf_instance.config_path = config_path

    # retention rulesets shouldn't do a nested merge
    # That's why I do a shallow update here manually
    _copy_from_default_retention(base_conf_instance)

    return base_conf_instance


def contains_path(path: PurePath, sub_path: PurePath) -> bool:
    """
    Check if a subpath is included in another path.

    Args:
        path: Path you want to check
        sub_path: Subpath that should be included in path.

    Returns:
        True if path contains subpath
    """
    return any(
        slice == sub_path.parts
        for slice in zip(*[path.parts[i:] for i in range(len(sub_path.parts))])
    )
