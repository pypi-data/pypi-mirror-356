from __future__ import annotations

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QWidget

from pyqgssim import __author__
from pyqgssim import __build_date__
from pyqgssim import __version__
from pyqgssim.config import config
from pyqgssim.gui.help.ui_AboutDialog import Ui_AboutDialog


class AboutDialog(QDialog, Ui_AboutDialog):
    """关于对话框."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)  # type: ignore
        self.setWindowTitle(
            f"关于 {config.get('app.name_cn')} {config.get('app.version')}",
        )
        self.label.setText(
            f"<p>版本: {__version__}</p>\
              <p>作者: {__author__}</p>\
              <p>构建日期: {__build_date__}</p>",
        )
