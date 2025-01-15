from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


class HistoryWindow(QDialog):
    def __init__(self, data_service):
        super().__init__()
        self.setWindowTitle('History of CPU, RAM, Disk Usage')
        self.setFixedSize(1000, 550)

        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.data_service = data_service

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'CPU', 'RAM', 'Disk', 'Created At'])
        self.refresh_history()
        self.table.setColumnWidth(4, 300)

    def refresh_history(self):
        data = self.data_service.get_all_usage()
        self.table.setRowCount(len(data))

        for i, row in enumerate(data):
            self._set_readonly_item(i, 0, str(row.id))
            self._set_readonly_item(i, 1, str(row.cpu))
            self._set_readonly_item(i, 2, str(row.ram))
            self._set_readonly_item(i, 3, str(row.disk))
            self._set_readonly_item(i, 4, str(row.created_at))

    def _set_readonly_item(self, row, column, text):
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Убираем возможность редактирования
        self.table.setItem(row, column, item)
