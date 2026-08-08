"""Diálogo de colaboración: actividad, permisos y uso compartido."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from rword.core.collaboration import CollaborationManager


class CollaborationDialog(QDialog):
    """Muestra actividad, gestiona permisos y comparte el documento."""

    def __init__(self, manager: CollaborationManager, parent=None) -> None:
        super().__init__(parent)
        self._manager = manager
        self.setWindowTitle("Colaboración")
        self.resize(520, 420)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        self._tabs = QTabWidget(self)

        activity_tab = QWidget(self)
        activity_layout = QVBoxLayout(activity_tab)
        self._activity_list = QListWidget(activity_tab)
        activity_layout.addWidget(self._activity_list)
        self._tabs.addTab(activity_tab, "Historial de actividad")

        permissions_tab = QWidget(self)
        perm_layout = QVBoxLayout(permissions_tab)
        self._perm_user_input = QComboBox(permissions_tab)
        self._perm_user_input.setEditable(True)
        perm_layout.addWidget(self._perm_user_input)
        self._mode_combo = QComboBox(permissions_tab)
        self._mode_combo.addItem("Edición", "write")
        self._mode_combo.addItem("Solo lectura", "read")
        perm_layout.addWidget(self._mode_combo)
        set_button = QPushButton("Aplicar permiso", permissions_tab)
        set_button.clicked.connect(self._apply_permission)
        perm_layout.addWidget(set_button)
        self._permissions_list = QListWidget(permissions_tab)
        perm_layout.addWidget(self._permissions_list)
        self._tabs.addTab(permissions_tab, "Permisos")

        layout.addWidget(self._tabs)

        share_row = QHBoxLayout()
        share_button = QPushButton("Copiar enlace para compartir", self)
        share_button.clicked.connect(self._copy_link)
        email_button = QPushButton("Compartir por correo...", self)
        email_button.clicked.connect(self._share_email)
        share_row.addWidget(share_button)
        share_row.addWidget(email_button)
        layout.addLayout(share_row)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        buttons.rejected.connect(self.accept)
        layout.addWidget(buttons)

        self._refresh()

    def _refresh(self) -> None:
        self._activity_list.clear()
        for entry in reversed(self._manager.activity()):
            self._activity_list.addItem(
                f"[{entry['time']}] {entry['user']}: {entry['event']}"
                f"{' — ' + entry['detail'] if entry['detail'] else ''}"
            )
        self._permissions_list.clear()
        permissions = self._permissions_data()
        for username, mode in permissions.items():
            label = "lectura" if mode == "read" else "edición"
            self._permissions_list.addItem(f"{username}: {label}")

    def _permissions_data(self) -> dict:
        return {
            username: self._manager.permission(username)
            for username in self._known_users()
        }

    def _known_users(self) -> list[str]:
        names = [self._manager.username]
        for entry in self._manager.activity():
            if entry["user"] not in names:
                names.append(entry["user"])
        return names

    def _apply_permission(self) -> None:
        username = self._perm_user_input.currentText().strip()
        if username:
            self._manager.set_permission(username, self._mode_combo.currentData())
            self._refresh()

    def _copy_link(self) -> None:
        from PySide6.QtWidgets import QApplication

        QApplication.clipboard().setText(self._manager.share_link())

    def _share_email(self) -> None:
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices

        link = self._manager.share_link()
        url = self._manager.share_mailto("Documento compartido", link)
        QDesktopServices.openUrl(QUrl(url))
