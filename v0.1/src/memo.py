from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QIntValidator, QFont
import sys

def change_font_size(text_edit: QTextEdit, size, font=''):
    text_edit.setFont(QFont(font, size))


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
        self.resize(600, 400)

        self.main_content = QTextEdit()
        self.setCentralWidget(self.main_content)
        change_font_size(self.main_content, 12)

        self.file_path = None

        self.menuber = self.menuBar()
        self.filemenu = self.menuber.addMenu('file')
        self.settingmenu = self.menuber.addMenu('setting')

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

        exitmenu = QAction('exit', self)
        exitmenu.setShortcut('Ctrl+Q')
        exitmenu.triggered.connect(self.exit_file)

        # ---

        # -- setting --

        font_sizemenu = QAction('font size', self)
        font_sizemenu.triggered.connect(self.font_size_setting)

        # ---

        self.filemenu.addAction(newmenu)
        self.filemenu.addAction(openmenu)
        self.filemenu.addAction(savemenu)
        self.filemenu.addAction(separ)
        self.filemenu.addAction(exitmenu)

        self.settingmenu.addAction(font_sizemenu)

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

    def exit_file(self):
        result = QMessageBox.question(self, 'save?', 'Are you going to save it?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if result == QMessageBox.Yes:
            self.save_file()
        QApplication.instance().quit()

    def font_size_setting(self):
        self.font_size = FontSzie(self.main_content)
        self.font_size.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainMemo()
    win.show()

    sys.exit(app.exec_())
