from unittest.mock import MagicMock
from gui.recorder import Recorder


def test_get_usage():
    recorder = Recorder(None, None)
    cpu, ram, disk = recorder.get_usage()
    assert 0 <= cpu <= 100
    assert 0 <= ram <= 100
    assert 0 <= disk <= 100


def test_record_usage():
    mock_db_connector = MagicMock()
    mock_parent = MagicMock()

    recorder = Recorder(mock_parent, mock_db_connector)
    recorder.is_recording = True
    recorder.record_usage()

    mock_db_connector.insert_usage.assert_called_once()


def test_start_recording():
    mock_db_connector = MagicMock()
    mock_parent = MagicMock()

    recorder = Recorder(mock_parent, mock_db_connector)
    recorder.start_recording()

    mock_parent.start_recording_ui.assert_called_once()


def test_stop_recording():
    mock_db_connector = MagicMock()
    mock_parent = MagicMock()

    recorder = Recorder(mock_parent, mock_db_connector)
    recorder.stop_recording()

    mock_parent.stop_recording_ui.assert_called_once()
