from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QIntValidator, QFont
import sys

def change_font_size(text_edit: QTextEdit, size, font='나눔고딕'):
    text_edit.setFont(QFont(font, size))

class Font(QLineEdit):
    def __init__(self, main_content: QTextEdit, size):
        super().__init__()
        self.setWindowTitle('font setting')
        self.setFixedSize(200, 25)

        self.font_size = size

        self.main_content = main_content

        self.returnPressed.connect(self.on_return)

    def on_return(self):
        change_font_size(self.main_content, self.font_size, self.text(),)
        self.close()

class FontSzie(QLineEdit):
    def __init__(self, main_content: QTextEdit):
        super().__init__()
        self.setWindowTitle('font size setting')
        self.setFixedSize(200, 25)

        self.main_content = main_content

        self.setValidator(QIntValidator(1, 1000, self))

        self.returnPressed.connect(self.on_return)

    def on_return(self):
        change_font_size(self.main_content, int(self.text()))
        self.close()


class MainMemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('memo')
        self.resize(800, 500)

        self.main_content = QTextEdit()
        self.setCentralWidget(self.main_content)
        self.main_content.setUndoRedoEnabled(True)
        change_font_size(self.main_content, 13)

        self.file_path = None

        self.menuber = self.menuBar()
        self.filemenu = self.menuber.addMenu('file')
        self.settingmenu = self.menuber.addMenu('setting')
        self.viewmenu = self.menuber.addMenu('view')

        separ = QAction(self)
        separ.setSeparator(True)

        # -- filemenu --

        newmenu = QAction('new file', self)
        newmenu.setShortcut('Ctrl+N')
        newmenu.triggered.connect(self.new_file)

        openmenu = QAction('open', self)
        openmenu.setShortcut('Ctrl+O')
        openmenu.triggered.connect(self.open_file)

        savemenu = QAction('save', self)
        savemenu.setShortcut('Ctrl+S')
        savemenu.triggered.connect(self.save_file)

        save_asmenu = QAction('svae as', self)
        save_asmenu.setShortcut('Ctrl+Shift+S')
        save_asmenu.triggered.connect(self.save_as_file)

        exitmenu = QAction('exit', self)
        exitmenu.setShortcut('Ctrl+Q')
        exitmenu.triggered.connect(self.exit_file)

        # ---

        # -- setting --

        fontmenu = QAction('font', self)
        fontmenu.triggered.connect(self.font_setting)

        font_sizemenu = QAction('font size', self)
        font_sizemenu.triggered.connect(self.font_size_setting)

        # ---

        # -- View --

        self.auto_linemeun = QAction('auto line wrap')
        self.auto_linemeun.setCheckable(True)
        self.auto_linemeun.toggled.connect(self.auto_line_view)

        # ---

        self.filemenu.addAction(newmenu)
        self.filemenu.addAction(openmenu)
        self.filemenu.addAction(savemenu)
        self.filemenu.addAction(save_asmenu)
        self.filemenu.addAction(separ)
        self.filemenu.addAction(exitmenu)

        self.settingmenu.addAction(fontmenu)
        self.settingmenu.addAction(font_sizemenu)

        self.viewmenu.addAction(self.auto_linemeun)

    def new_file(self):
        result = QMessageBox.question(self, 'save?', 'Are you going to save it?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if result == QMessageBox.Yes:
            self.save_file()
            self.main_content.clear()
        elif result == QMessageBox.No:
            self.main_content.clear()
        else:
            return
        self.file_path = None

    def open_file(self):
        result = QMessageBox.question(self, 'save?', 'Are you going to save it?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if result == QMessageBox.Yes:
            self.save_file()
        elif result == QMessageBox.Cancel:
            return

        self.main_content.clear()

        self.file_path, _ = QFileDialog.getOpenFileName(None, "파일 선택", "", "모든 파일 (*);;텍스트 파일 (*.txt)")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.main_content.insertPlainText(f.read())

    def save_file(self):
        if self.file_path:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(self.main_content.toPlainText())
            return

        self.file_path, _ = QFileDialog.getSaveFileName(self, 'save file', '', 'Text Files (*.txt)')

        if self.file_path:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(self.main_content.toPlainText())

    def save_as_file(self):
        self.file_path, _ = QFileDialog.getSaveFileName(self, 'save as file', '', 'Text Files (*.txt)')

        if self.file_path:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(self.main_content.toPlainText())

    def exit_file(self):
        result = QMessageBox.question(self, 'save?', 'Are you going to save it?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if result == QMessageBox.Yes:
            self.save_file()
        elif result == QMessageBox.Cancel:
            return
        QApplication.instance().quit()

    def font_setting(self):
        self.font_win = Font(self.main_content, self.main_content.font().pointSize())
        self.font_win.show()

    def font_size_setting(self):
        self.font_size = FontSzie(self.main_content)
        self.font_size.show()

    def auto_line_view(self):
        if self.auto_linemeun.isChecked():
            self.main_content.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.main_content.setLineWrapMode(QTextEdit.NoWrap)

    def closeEvent(self, event):
        result = QMessageBox.question(self, 'save?', 'Are you going to save it?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if result == QMessageBox.Yes:
            self.save_file()
        elif result == QMessageBox.Cancel:
            event.ignore()
            return
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainMemo()
    win.show()
    sys.exit(app.exec_())