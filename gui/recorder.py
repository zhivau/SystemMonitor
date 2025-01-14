import psutil
from PyQt5.QtCore import QTimer


class Recorder:
    def __init__(self, parent, data_service):
        self.data_service = data_service
        self.is_recording = False
        self.parent = parent

    def get_usage(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        return cpu, ram, disk

    def start_recording(self):
        self.parent.start_recording_ui()
        self.is_recording = True
        self.record_usage()

    def record_usage(self):
        if self.is_recording:
            cpu, ram, disk = self.get_usage()
            self.data_service.insert_usage(cpu, ram, disk)
            QTimer.singleShot(self.parent.interval * 1000, self.record_usage)

    def stop_recording(self):
        self.parent.stop_recording_ui()
        self.is_recording = False
