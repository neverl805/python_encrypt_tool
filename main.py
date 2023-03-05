import sys,os,threading
from PySide6 import QtWidgets
from untitled import *
from PySide6.QtWidgets import QApplication, QMainWindow,QFileDialog,QMessageBox
from PySide6 import QtCore
import PySide6
from subprocess import Popen, PIPE, STDOUT

class Ui_MainWindows(QMainWindow):
    def __init__(self):
        super(Ui_MainWindows, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.anim = None
        self.path = os.path.abspath(".")
        self.effect_shadow_style(self.ui.frame)
        self.bind_event()
        self.setWindowTitle('Python代码加密工具')
        self.setWindowIcon(QIcon('encrypt_logo.ico'))

    def bind_event(self):
        self.ui.pushButton.clicked.connect(self.file_choices)
        self.ui.pushButton_2.clicked.connect(self.encrypt_file)
        self.ui.pushButton_3.clicked.connect(self.open_files)


    def encrypt_file(self):
        enc_path = self.ui.lineEdit.text()
        process = Popen(["cmd"], shell=False, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        commands = (
                    f"pyarmor obfuscate {enc_path}\n"
                    )
        outs, errs = process.communicate(commands.encode('gbk'))
        content = [z.strip() for z in outs.decode('gb18030').split("\n") if z]
        # print(*content, sep="\n")
        QMessageBox.information(self,'提示',content[-4]+'\n'+content[-3])

    def file_choices(self):
        folder_path = QFileDialog.getOpenFileName(self,'请选择要加密文件的所在文件夹')
        self.ui.lineEdit.setText(folder_path[0])

    def open_files(self):
        def action():
            os.startfile(self.path)
        t = threading.Thread(target=action)
        t.setDaemon(True)
        t.start()

    # 鼠标点击
    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPosition().toPoint() - self.pos()
            event.accept()
            self.setCursor(PySide6.QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    # 鼠标点拖之后移动
    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(event.globalPosition().toPoint() - self.m_Position)
            event.accept()

    # 鼠标释放
    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.m_flag = False
        self.setCursor(PySide6.QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def effect_shadow_style(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 8)  # 偏移
        effect_shadow.setBlurRadius(48)  # 阴影半径
        effect_shadow.setColor(QColor(162, 129, 247))  # 阴影颜色
        widget.setGraphicsEffect(effect_shadow)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindows()
    window.show()
    sys.exit(app.exec())