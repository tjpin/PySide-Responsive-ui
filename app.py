import sys
from threading import Thread

from PySide6.QtCharts import *
from PySide6.QtCore import *
from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import pandas as pd
from dtview import ChartWidget, DonutWidget

ui, _ = loadUiType("dynamic_layout.ui")


class DynamicApp(QMainWindow, ui):
    def __init__(self):
        super(DynamicApp, self).__init__()
        self.setupUi(self)
        # Remove default frame
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.pos_ = self.pos()
        self.setWindowFlags(flags)
        self.activate_()

    def mousePressEvent(self, event):
        # globalPos seems deprecated
        self.pos_ = event.globalPos()

    def mouseMoveEvent(self, event):
        point = QPoint(event.globalPos() - self.pos_)
        self.move(self.x() + point.x(), self.y() + point.y())
        self.pos_ = event.globalPos()

    def activate_(self):
        self.toggleButton.clicked.connect(self.open_close_menu)
        self.closeButton.clicked.connect(self.close_win)
        self.miniButton.clicked.connect(self.minimize)
        self.maxiButton.clicked.connect(self.maxmize_minimize)
        self.load_data()
        self.draw_line_chart()

        # th = Thread(target=self.load_data)
        # th.start()

    def open_close_menu(self):
        width = self.leftMenu.maximumWidth()
        fr = QFrame()
        if width == 200:
            self.leftMenu.setMaximumWidth(43)
        else:
            self.leftMenu.setMaximumWidth(200)
        # return width

    def minimize(self):
        self.showMinimized()

    def close_win(self):
        self.close()

    def maxmize_minimize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def draw_line_chart(self):
        chart = QChart()

        wid = self.plotCard
        pi = self.pieCard

        cw = ChartWidget(wid)
        cd = DonutWidget(pi)

        cw.add_chart()
        cd.add_donut()

    def load_data(self):
        df = pd.read_excel("data.xlsx")
        # tbl = self.load_data(df)
        table = self.tableWidget
        table.setStyleSheet("background-color: rgb(25, 25, 25); color: rgb(157, 168, 168)")
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)
        table.setRowCount(len(df.index))

        header = table.horizontalHeader()
        header.setStyleSheet("background-color: rgb(25, 25, 25); color: rgb(157, 168, 168)")

        for rn, row in enumerate(df.index):
            for cn, col in enumerate(df.columns):
                item = QTableWidgetItem(str(df.loc[row, col]))
                table.setItem(rn, cn, item)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)


if __name__ == "__main__":
    app = QApplication()
    win = DynamicApp()
    win.show()
    sys.exit(app.exec())
