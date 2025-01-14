from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox
from gui.recorder import Recorder
from gui.history_window import HistoryWindow


class MainWindow(QWidget):
    def __init__(self, data_service):
        super().__init__()

        self.data_service = data_service

        self.setWindowTitle('CPU, RAM, Disk Usage Monitor')
        self.setGeometry(100, 100, 400, 300)
        self.setFixedSize(400, 300)

        self.recorder = Recorder(self, self.data_service)

        self.layout = QVBoxLayout(self)
        self.cpu_label = QLabel('CPU: 0%', self)
        self.ram_label = QLabel('RAM: 0%', self)
        self.disk_label = QLabel('Disk: 0%', self)

        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)

        self.refresh_time_label = QLabel("Time Interval (sec):", self)
        self.layout.addWidget(self.refresh_time_label)

        self.refresh_time_input = QSpinBox(self)
        self.refresh_time_input.setMinimum(1)
        self.refresh_time_input.setValue(1)
        self.layout.addWidget(self.refresh_time_input)

        self.start_button = QPushButton('Start Recording', self)
        self.start_button.clicked.connect(self.recorder.start_recording)

        self.stop_button = QPushButton('Stop Recording', self)
        self.stop_button.clicked.connect(self.recorder.stop_recording)
        self.stop_button.setEnabled(False)

        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)

        self.history_button = QPushButton('View History', self)
        self.history_button.clicked.connect(self.open_history_window)
        self.layout.addWidget(self.history_button)

        self.record_timer = QTimer(self)
        self.record_timer.timeout.connect(self.update_record_time)
        self.record_time = QTime(0, 0)

        self.record_time_label = QLabel('Recording Time: 00:00', self)
        self.record_time_label.setVisible(False)
        self.layout.addWidget(self.record_time_label)

        self.history_window = HistoryWindow(self.data_service)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_usage)
        self.timer.start(1000)

        self.interval = 1

    def update_usage(self):
        cpu, ram, disk = self.recorder.get_usage()
        self.cpu_label.setText(f'CPU: {cpu}%')
        self.ram_label.setText(f'RAM: {ram}%')
        self.disk_label.setText(f'Disk: {disk}%')

        self.interval = self.refresh_time_input.value()
        self.timer.setInterval(self.interval * 1000)

    def start_recording_ui(self):
        self.start_button.setVisible(False)
        self.record_time_label.setVisible(True)

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.record_timer.start(1000)
        self.record_time = QTime(0, 0)

    def stop_recording_ui(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        self.record_timer.stop()
        self.record_time_label.setVisible(False)

        self.start_button.setVisible(True)

        self.record_time_label.setText('Recording Time: 00:00')

    def update_record_time(self):
        self.record_time = self.record_time.addSecs(1)
        self.record_time_label.setText(f'Recording Time: {self.record_time.toString("mm:ss")}')

    def open_history_window(self):
        self.history_window.refresh_history()
        self.history_window.show()

    def closeEvent(self, event):
        if self.data_service:
            self.data_service.close()
        event.accept()
