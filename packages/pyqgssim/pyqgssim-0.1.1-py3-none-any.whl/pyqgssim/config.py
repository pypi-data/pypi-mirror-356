from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from typing import TypeVar

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib

import tomli_w

__all__ = [
    "ASSETS_DIR",
    "CWD",
    "QSS_DIR",
    "config",
]

logger = logging.getLogger(__name__)

CWD = Path(__file__).parent
ASSETS_DIR = CWD / "assets"
QSS_DIR = ASSETS_DIR / "qss"


T = TypeVar("T")


class AppConfig:
    """应用配置.

    >>> config = AppConfig()
    >>> config.config["app"]["name"]
    'pyqgssim'
    >>> config.get("app.name")
    'pyqgssim'
    >>> config.get("app.name", "default")
    'pyqgssim'
    """

    def __init__(self) -> None:
        self.config: dict[str, Any] = {}
        self.config_file = ASSETS_DIR / "config.toml"

        self._load_config()

    @property
    def project_tree_path(self) -> Path:
        """项目树路径."""
        return Path(self.get("env.project_tree_path")).expanduser()

    def get(self, key: str, default: T = "") -> T:
        """获取配置项值.

        Args:
            key (str): 配置项键.
            default (T | None, optional): 默认值. Defaults to None.

        Returns:
            T | None: 配置项值.
        """
        keys = key.split(".")
        current = self.config

        for k in keys:
            if not isinstance(current, dict) or k not in current:
                return default

            current = current.get(k, default)

        return current  # type: ignore

    def _load_config(self) -> None:
        """加载配置.

        FileNotFoundError: 配置文件不存在.
        """
        try:
            with self.config_file.open("rb") as f:
                self.config = tomllib.load(f)
        except FileNotFoundError:
            logger.debug(f"配置文件 {self.config_file} 不存在.")
            self.config = {}
        else:
            logger.debug(f"从 {self.config_file} 读取配置成功.")

    def save_config(self) -> None:
        """保存配置."""
        with self.config_file.open("wb") as f:
            tomli_w.dump(self.config, f)


config = AppConfig()
