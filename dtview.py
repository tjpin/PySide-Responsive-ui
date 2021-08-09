from functools import partial
from random import randrange

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtCharts import *
from PySide6.QtWidgets import QGridLayout


class ChartWidget:
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.chart = QChart()
        self._chart_view = QChartView(self.chart)
        self.chart.ChartTheme(QChart.ChartThemeDark)
        self._axis_y = QValueAxis()
        self._axis_x = QBarCategoryAxis()
        self.categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        self._line_series = QLineSeries()
        self._bar_series = QBarSeries()
        self.set4 = QBarSet("Smartphones")
        self.set3 = QBarSet("iPhones")
        self.set2 = QBarSet("AirPods")
        self.set1 = QBarSet("Tablets")
        self.set0 = QBarSet("iMac")

    def add_chart(self):
        self.set0.append([1, 2, 3, 4, 5, 6])
        self.set1.append([5, 0, 0, 4, 0, 7])
        self.set2.append([3, 5, 8, 13, 8, 5])
        self.set3.append([5, 6, 7, 3, 4, 5])
        self.set4.append([9, 7, 5, 3, 1, 2])

        self._bar_series.append(self.set0)
        self._bar_series.append(self.set1)
        self._bar_series.append(self.set2)
        self._bar_series.append(self.set3)
        self._bar_series.append(self.set4)

        self._line_series.setName("Treds")
        self._line_series.append(QPoint(0, 4))
        self._line_series.append(QPoint(1, 15))
        self._line_series.append(QPoint(2, 20))
        self._line_series.append(QPoint(3, 4))
        self._line_series.append(QPoint(4, 12))
        self._line_series.append(QPoint(5, 17))

        self.chart.addSeries(self._bar_series)
        self.chart.addSeries(self._line_series)
        self.chart.setTitle("Line and barchart example")

        self._axis_x.append(self.categories)
        self.chart.setAxisX(self._axis_x, self._line_series)
        self.chart.setAxisX(self._axis_x, self._bar_series)
        self._axis_x.setRange("Jan", "Jun")

        self.chart.setAxisY(self._axis_y, self._line_series)
        self.chart.setAxisY(self._axis_y, self._bar_series)
        self._axis_y.setRange(0, 20)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.widget.addWidget(self._chart_view)


class DonutWidget:
    def __init__(self, pie):
        self.pie = pie
        self.donuts = []
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart = self.chart_view.chart()
        self.chart.legend().setVisible(False)
        self.chart.setTitle("Nested donuts")
        self.chart.setAnimationOptions(QChart.AllAnimations)

        self.min_size = 0.1
        self.max_size = 0.9
        self.donut_count = 5

        self.add_donut()

        # create main layout
        self.main_layout = self.pie
        self.main_layout.addWidget(self.chart_view, 1)
        # self.setLayout(self.main_layout)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_rotation)
        self.update_timer.start(1250)

    def add_donut(self):
        for i in range(self.donut_count):
            donut = QPieSeries()
            slccount = randrange(3, 6)
            for j in range(slccount):
                value = randrange(100, 200)

                slc = QPieSlice(str(value), value)
                slc.setLabelVisible(True)
                slc.setLabelColor(Qt.white)
                slc.setLabelPosition(QPieSlice.LabelInsideTangential)

                # Connection using an extra parameter for the slot
                slc.hovered[bool].connect(partial(self.explode_slice, slc=slc))

                donut.append(slc)
                size = (self.max_size - self.min_size) / self.donut_count
                donut.setHoleSize(self.min_size + i * size)
                donut.setPieSize(self.min_size + (i + 1) * size)

            self.donuts.append(donut)
            self.chart_view.chart().addSeries(donut)

    def update_rotation(self):
        for donut in self.donuts:
            phase_shift = randrange(-50, 100)
            donut.setPieStartAngle(donut.pieStartAngle() + phase_shift)
            donut.setPieEndAngle(donut.pieEndAngle() + phase_shift)

    def explode_slice(self, exploded, slc):
        if exploded:
            self.update_timer.stop()
            slice_startangle = slc.startAngle()
            slice_endangle = slc.startAngle() + slc.angleSpan()

            donut = slc.series()
            idx = self.donuts.index(donut)
            for i in range(idx + 1, len(self.donuts)):
                self.donuts[i].setPieStartAngle(slice_endangle)
                self.donuts[i].setPieEndAngle(360 + slice_startangle)
        else:
            for donut in self.donuts:
                donut.setPieStartAngle(0)
                donut.setPieEndAngle(360)

            self.update_timer.start()

        slc.setExploded(exploded)
