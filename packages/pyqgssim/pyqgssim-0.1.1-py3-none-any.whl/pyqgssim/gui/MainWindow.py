from __future__ import annotations

from typing import TYPE_CHECKING

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QWidget

from pyqgssim.config import ASSETS_DIR
from pyqgssim.config import QSS_DIR
from pyqgssim.gui.ui_MainWindow import Ui_MainWindow

if TYPE_CHECKING:
    from PySide2.QtGui import QCloseEvent


from pyqgssim.config import config
from pyqgssim.gui.help.AboutDialog import AboutDialog
from pyqgssim.gui.NewProjectDialog import NewProjectDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    """主窗口."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setupUi(self)

        icon = QIcon(str(ASSETS_DIR / config.get("app.icon")))
        self.setWindowTitle(config.get("app.name_cn") or "PyQGSSim")
        self.setWindowIcon(icon)

        self._init_style()
        self._init_ui()

    def _init_ui(self) -> None:
        self.newProjectDialog = NewProjectDialog(self)
        self.newProjectAction.triggered.connect(self.newProjectDialog.show)  # type: ignore

        self.action_about.triggered.connect(self.on_about)  # type: ignore
        self.action_exit.triggered.connect(self.close)  # type: ignore

    def _init_style(self) -> None:
        """初始化样式."""
        qss_file = QSS_DIR / "lightblue.css"
        with qss_file.open(encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def on_about(self) -> None:
        """显示关于窗口."""
        about_dialog = AboutDialog(self)
        about_dialog.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        """关闭事件."""
        return

        reply = QMessageBox.question(
            self,
            "提示",
            "确定要退出吗?",
            QMessageBox.Yes | QMessageBox.No,  # type: ignore
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
