import os
import sys
import threading
from typing import List, Dict, Any

from PySide6.QtCore import QObject, Slot, Signal, QUrl, QTimer
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtQml import QQmlApplicationEngine

from controllers.login_controller import RiotLoginController


class Backend(QObject):
    notification = Signal(str, str)
    accountsChanged = Signal(list)
    regionsChanged = Signal(list)
    savedAccount = Signal(str, str)

    def __init__(self, controller: RiotLoginController, parent: QObject = None) -> None:
        super().__init__(parent)
        self.controller = controller

    @Slot()
    def loadInitialData(self) -> None:
        try:
            accounts = self.controller.get_accounts()
            regions = self.controller.get_regions()
            self.accountsChanged.emit(accounts)
            self.regionsChanged.emit(regions)
        except Exception as exc:
            self.notification.emit(f"Error loading data: {exc}", "error")

    @Slot(str, str, str)
    def saveAccount(self, username: str, password: str, region: str) -> None:
        if not username or not password or not region:
            self.notification.emit("Please fill in all fields", "error")
            return
        try:
            result: Dict[str, Any] = self.controller.save_account(username, password, region)
            if result.get("success"):
                self.notification.emit("Account saved successfully", "success")
                self.loadInitialData()
                self.savedAccount.emit(username, region)
            else:
                self.notification.emit(f"Error saving account: {result.get('message')}", "error")
        except Exception as exc:
            self.notification.emit(f"Error saving account: {exc}", "error")

    @Slot(str)
    def deleteAccount(self, username: str) -> None:
        if not username:
            self.notification.emit("Please select an account to delete", "error")
            return
        try:
            result: Dict[str, Any] = self.controller.delete_account(username)
            if result.get("success"):
                self.notification.emit("Account deleted successfully", "success")
                self.loadInitialData()
            else:
                self.notification.emit(f"Error deleting account: {result.get('message')}", "error")
        except Exception as exc:
            self.notification.emit(f"Error deleting account: {exc}", "error")

    @Slot(str)
    def loginToClient(self, username: str) -> None:
        if not username:
            self.notification.emit("Please select an account to login", "error")
            return

        self.notification.emit("Logging in...", "info")

        def _run() -> None:
            try:
                result: Dict[str, Any] = self.controller.login_to_client(username)
                msg_type = "success" if result.get("success") else "error"
                self.notification.emit(result.get("message", ""), msg_type)
            except Exception as exc:
                self.notification.emit(f"Login error: {exc}", "error")

        threading.Thread(target=_run, daemon=True).start()


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main() -> None:
    app = QGuiApplication(sys.argv)

    # App title and icon
    app.setApplicationDisplayName("Riot Auto Login")
    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Ensure a non-native style so our custom backgrounds/contentItems are respected
    try:
        QQuickStyle.setStyle("Fusion")
    except Exception:
        pass

    engine = QQmlApplicationEngine()

    controller = RiotLoginController()
    backend = Backend(controller)

    # Expose context properties
    engine.rootContext().setContextProperty("backend", backend)
    bg_path = resource_path("background.jpg")
    engine.rootContext().setContextProperty("bgImageUrl", QUrl.fromLocalFile(bg_path) if os.path.exists(bg_path) else QUrl())

    # Load QML
    qml_path = resource_path(os.path.join("ui", "main.qml"))
    engine.load(QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        sys.exit(-1)

    # Center the window on the primary screen
    try:
        root = engine.rootObjects()[0]
        screen_geo = QGuiApplication.primaryScreen().availableGeometry()
        x = screen_geo.x() + (screen_geo.width() - root.width()) // 2
        y = screen_geo.y() + (screen_geo.height() - root.height()) // 2
        root.setX(x)
        root.setY(y)
    except Exception:
        pass

    # Kick off initial data load shortly after startup
    QTimer.singleShot(0, backend.loadInitialData)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()


