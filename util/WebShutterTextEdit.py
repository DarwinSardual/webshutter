from PyQt5.QtWidgets import QTextEdit, QApplication
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

class WebShutterTextEdit(QTextEdit):

    def __init__(self):
        self.super = super(WebShutterTextEdit, self)
        self.super.__init__()

        self.callback = None

    def keyPressEvent(self, keyEvent):
        key = keyEvent.key()
        if (key == Qt.Key_Enter or key == Qt.Key_Return) and not QApplication.queryKeyboardModifiers() == Qt.ShiftModifier:
            self.callback and self.callback()
        else:
            self.super.keyPressEvent(keyEvent)

    def setCallback(self, callback):
        self.callback = callback
