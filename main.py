import sys
import csv
import os
import subprocess
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
    QSpinBox, QLabel, QGroupBox, QHeaderView, QMessageBox,
)
from PySide6.QtCore import Qt

from About import AboutWindow

HEADERS = ["ID", "Grades Original", "Corrected Grades"]


class GradeWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Correction Tool")
        self.setMinimumSize(720, 680)
        self.resize(800, 720)


        self.build_ui()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''


    def build_ui(self) :
        central = QWidget()
        
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(20, 16, 20, 16)
        root_layout.setSpacing(14)
        
        title = QLabel("Grade Correction Tool")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(title)

        file_group = QGroupBox("File")
        file_layout = QHBoxLayout(file_group)

        self.status_label = QLabel("No file loaded")
        self.status_label.setObjectName("statusLabel")
        file_layout.addWidget(self.status_label, stretch=1)

        self.load_btn = QPushButton("Open CSV File…")
        self.load_btn.clicked.connect(self.on_open_file)
        file_layout.addWidget(self.load_btn)

        root_layout.addWidget(file_group)

        self.table = QTableWidget(50,3)
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        header = self.table.horizontalHeader()
        for col in range(3):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        root_layout.addWidget(self.table, stretch=1)

        bonus_group = QGroupBox("Bonus Points")
        bonus_layout = QHBoxLayout(bonus_group)

        bonus_layout.addWidget(QLabel("Correction points:"))

        self.spin = QSpinBox()
        self.spin.setRange(-100, 100)
        self.spin.setValue(0)
        self.spin.setFixedWidth(120)
        
        self.spin.editingFinished.connect(self.on_bonus_applied)
        bonus_layout.addWidget(self.spin)

        bonus_layout.addStretch()

        root_layout.addWidget(bonus_group)

        self.update_btn = QPushButton("Update File")
        self.update_btn.setObjectName("updateButton")
        self.update_btn.setEnabled(False)
        self.update_btn.clicked.connect(self.on_update_file)
        root_layout.addWidget(self.update_btn)

        self.about_btn = QPushButton("About")
        self.about_btn.setObjectName("aboutButton")
        self.about_btn.clicked.connect(self.on_about)
        root_layout.addWidget(self.about_btn)

    def on_open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Grades CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not path:
            return

        self.selected_file = path
        self.student_ids.clear()
        self.original_grades.clear()
        self.corrected_grades.clear()

        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    self.student_ids.append(row[0].strip())
                    grade = int(row[1].strip())
                    self.original_grades.append(grade)
                    self.corrected_grades.append(grade)

        self.spin.setValue(0)
        self.populate_table()
        self.status_label.setText(
            f"Loaded: {os.path.basename(path)}  —  {len(self.student_ids)} students"
        )
        self.update_btn.setEnabled(True)

    def on_bonus_applied(self):
        if not self.original_grades:
            return
        bonus = self.spin.value()
        for i in range(len(self.original_grades)):
            self.corrected_grades[i] = min(self.original_grades[i] + bonus, 100)
        self.populate_table()

    def on_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    def on_update_file(self) -> None:
        if not self.selected_file or not self.corrected_grades:
            return

        with open(self.selected_file, "r", newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = next(reader, None)
            rows = list(reader)

        if header is None:
            return

        with open(self.selected_file, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(header)
            for row, corrected_grade in zip(rows, self.corrected_grades):
                if len(row) >= 2:
                    row[1] = str(corrected_grade)
                writer.writerow(row)

        try:
            if sys.platform == "win32":
                os.startfile(self.selected_file)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", self.selected_file])
            else:
                subprocess.Popen(["xdg-open", self.selected_file])
        except OSError:
            QMessageBox.warning(
                self,
                "Warning",
                "The file was updated, but it could not be opened automatically.",
            )
            return

        QMessageBox.information(
            self,
            "Success",
            "The file was updated and opened.",
        )

    def populate_table(self):
        self.table.clearContents()
        self.table.setRowCount(50)
        for row_idx, (sid, orig, corrected) in enumerate(
            zip(self.student_ids, self.original_grades, self.corrected_grades)
        ):
            id_item = QTableWidgetItem(sid)
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 0, id_item)

            orig_item = QTableWidgetItem(str(orig))
            orig_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 1, orig_item)

            corr_item = QTableWidgetItem(str(corrected))
            corr_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 2, corr_item)


def main():
    app = QApplication(sys.argv)
    qss_path = Path(__file__).parent / "style.qss"
    app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    window = GradeWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
