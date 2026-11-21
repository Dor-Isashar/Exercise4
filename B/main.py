import csv
import sys
from pathlib import Path

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.figure import Figure

from About import AboutWindow

class IceCreamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Sales Analysis")
        self.setMinimumSize(900, 650)
        self.resize(1100, 720)

        self.temperatures = []
        self.revenues = []

        self.build_ui()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(12)

        title = QLabel("Ice Cream Revenue vs. Temperature")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        file_group = QGroupBox("CSV File")
        file_layout = QHBoxLayout(file_group)
        self.status_label = QLabel("No file loaded")
        self.status_label.setObjectName("statusLabel")
        file_layout.addWidget(self.status_label, stretch=1)

        self.load_button = QPushButton("Open CSV File")
        self.load_button.clicked.connect(self.on_open_file)
        file_layout.addWidget(self.load_button)

        self.about_button = QPushButton("About")
        self.about_button.setObjectName("aboutButton")
        self.about_button.clicked.connect(self.on_about)
        file_layout.addWidget(self.about_button)
        root.addWidget(file_group)

        self.figure = Figure(figsize=(9, 6), dpi=100)
        self.figure.patch.set_facecolor("#181825")
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        root.addWidget(self.toolbar)
        root.addWidget(self.canvas, stretch=1)

    def on_open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Ice Cream CSV",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if not path:
            return

        self.temperatures.clear()
        self.revenues.clear()

        try:
            with open(path, newline="", encoding="utf-8-sig") as csv_file:
                reader = csv.reader(csv_file)
                next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        try:
                            self.temperatures.append(float(row[0].strip()))
                            self.revenues.append(float(row[1].strip()))
                        except ValueError:
                            continue
        except OSError as error:
            self.status_label.setText(f"Could not open file: {error}")
            return

        if not self.temperatures:
            self.status_label.setText("No valid numeric data found")
            return

        self.status_label.setText(
            f"Loaded: {Path(path).name} - {len(self.temperatures)} records"
        )
        self.draw_chart()

    def draw_chart(self):
        self.figure.clear()
        axes = self.figure.add_subplot(111)
        axes.set_facecolor("#181825")

        temperatures = np.array(self.temperatures)
        revenues = np.array(self.revenues)

        axes.scatter(
            temperatures,
            revenues,
            s=1,
            color="#89b4fa",
            alpha=0.75,
            label="Sales data",
        )

        if len(temperatures) >= 2:
            slope, intercept = np.polyfit(temperatures, revenues, 1)
            trend_x = np.linspace(temperatures.min(), temperatures.max(), 300)
            trend_y = slope * trend_x + intercept
            axes.plot(trend_x, trend_y, color="#f38ba8", linewidth=2, label="Trend line")

            sign = "+" if intercept >= 0 else "-"
            equation = f"y = {slope:.2f}x {sign} {abs(intercept):.2f}"
            axes.text(
                0.04,
                0.96,
                equation,
                transform=axes.transAxes,
                fontsize=12,
                fontweight="bold",
                color="#f9e2af",
                verticalalignment="top",
                bbox={"boxstyle": "round", "facecolor": "#313244", "alpha": 0.9},
            )

        axes.set_title("Ice Cream Revenue vs. Outside Temperature", color="#cdd6f4")
        axes.set_xlabel("Outside Temperature (°C)", color="#cdd6f4")
        axes.set_ylabel("Ice Cream Sales Revenue ($)", color="#cdd6f4")
        axes.tick_params(colors="#a6adc8")
        axes.spines["top"].set_visible(False)
        axes.spines["right"].set_visible(False)
        axes.spines["bottom"].set_color("#585b70")
        axes.spines["left"].set_color("#585b70")
        axes.grid(True, linestyle="--", alpha=0.18, color="#a6adc8")
        axes.legend(facecolor="#313244", edgecolor="#585b70", labelcolor="#cdd6f4")
        self.figure.tight_layout()
        self.canvas.draw()

    def on_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()

def main():
    app = QApplication(sys.argv)
    qss_path = Path(__file__).parent / "style.qss"
    app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    window = IceCreamWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
