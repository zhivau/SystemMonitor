from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem


class HistoryWindow(QDialog):
    def __init__(self, data_service):
        super().__init__()
        self.setWindowTitle('History of CPU, RAM, Disk Usage')
        self.setFixedSize(680, 550)

        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.data_service = data_service

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'CPU', 'RAM', 'Disk'])
        self.refresh_history()

    def refresh_history(self):
        data = self.data_service.get_all_usage()
        self.table.setRowCount(len(data))

        for i, row in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(row.id)))
            self.table.setItem(i, 1, QTableWidgetItem(str(row.cpu)))
            self.table.setItem(i, 2, QTableWidgetItem(str(row.ram)))
            self.table.setItem(i, 3, QTableWidgetItem(str(row.disk)))
