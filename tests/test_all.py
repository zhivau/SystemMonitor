import pytest
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QTime
from gui import MainWindow, HistoryWindow
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data import DataService, Base


DATABASE_URL = "postgresql://test_user:test_password@localhost/test_db"


@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def data_service(db_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()

    service = DataService(session)
    yield service
    service.close()


def test_refresh_history(qtbot, data_service):
    window = HistoryWindow(data_service)
    qtbot.addWidget(window)

    data_service.insert_usage(50.0, 30.0, 40.0)
    window.refresh_history()
    last_row_index = window.table.rowCount() - 1
    assert window.table.item(last_row_index, 1).text() == '50.0'
    assert window.table.item(last_row_index, 2).text() == '30.0'
    assert window.table.item(last_row_index, 3).text() == '40.0'


def test_start_stop_recording(qtbot, data_service):
    window = MainWindow(data_service)
    qtbot.addWidget(window)

    window.update_usage()
    assert window.start_button.isEnabled()
    assert not window.stop_button.isEnabled()

    QTest.mouseClick(window.start_button, Qt.LeftButton)
    assert not window.start_button.isEnabled()
    assert window.stop_button.isEnabled()

    QTest.mouseClick(window.stop_button, Qt.LeftButton)
    assert window.start_button.isEnabled()
    assert not window.stop_button.isEnabled()


def test_update_record_time(qtbot, data_service):
    window = MainWindow(data_service)
    qtbot.addWidget(window)
    window.update_time()
    assert QTime(0, 0, 1) == window.gui_time


def test_open_history_window(qtbot, data_service):
    window = MainWindow(data_service)
    qtbot.addWidget(window)
    QTest.mouseClick(window.history_button, Qt.LeftButton)
    assert window.history_window.isVisible()
    window.history_window.close()
    assert not window.history_window.isVisible()


def test_insert_usage(qtbot, data_service):
    window = MainWindow(data_service)
    qtbot.addWidget(window)

    window.insert_usage()
    window.history_window.refresh_history()
    last_row_index = window.history_window.table.rowCount() - 1
    assert 0.0 <= float(window.history_window.table.item(last_row_index, 1).text()) <= 100.0
    assert 0.0 <= float(window.history_window.table.item(last_row_index, 2).text()) <= 100.0
    assert 0.0 <= float(window.history_window.table.item(last_row_index, 3).text()) <= 100.0
    window.close()