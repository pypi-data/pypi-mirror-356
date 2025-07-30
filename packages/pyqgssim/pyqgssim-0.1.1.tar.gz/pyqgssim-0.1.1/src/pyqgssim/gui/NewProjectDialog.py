from __future__ import annotations

import logging
from typing import ClassVar

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QTreeWidgetItem
from PySide2.QtWidgets import QWidget

from pyqgssim.config import config
from pyqgssim.gui.ui_NewProjectDialog import Ui_NewProjectDialog

logger = logging.getLogger(__name__)


class NewProjectDialog(QDialog, Ui_NewProjectDialog):
    """新建项目对话框."""

    ITEM_TYPE: ClassVar[dict[str, int]] = {
        "project": 0,
        "folder": 1,
        "file": 2,
    }

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self._init_ui()

        self.setWindowTitle("新建项目")
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)  # type: ignore

        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # type: ignore
        self.lineEdit_structTreePath.setText(str(config.project_tree_path))

    def _init_ui(self) -> None:
        """初始化界面."""
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["结构树"])
        self.treeWidget.setHeaderHidden(False)

        if not config.project_tree_path.exists():
            logger.warning(
                f"项目结构树目录不存在, 已自动创建: {config.project_tree_path}",
            )
            config.project_tree_path.mkdir(parents=True)

        folders = [
            f
            for f in config.project_tree_path.iterdir()
            if f.is_dir() and not f.name.startswith(".")
        ]
        for folder in folders:
            item = QTreeWidgetItem(self.treeWidget, [folder.name])
            item.setData(0, Qt.UserRole, self.ITEM_TYPE.get("project"))  # type: ignore
            item.setData(0, Qt.UserRole + 1, folder.name)  # type: ignore
