import pytest
from unittest.mock import MagicMock, patch
from io import StringIO
from tars_mazenav.adapters.mms_adapter import MMSAdapter
from tars_mazenav.adapters.hardware_serial_adapter import HardwareSerialAdapter


def test_mms_adapter_io():
    with patch("sys.stdout", new=StringIO()) as fake_out, \
         patch("sys.stdin", StringIO("16\n16\ntrue\nfalse\nack\n")):

        w, h = MMSAdapter.get_maze_dimensions()
        assert (w, h) == (16, 16)

        assert MMSAdapter.wall_front() is True
        assert MMSAdapter.wall_left() is False

        MMSAdapter.turn_right()
        MMSAdapter.turn_left()
        MMSAdapter.set_wall(0, 0, "n")
        MMSAdapter.set_text(0, 0, "S")
        MMSAdapter.set_color(0, 0, "g")

    with patch("sys.stderr", new=StringIO()) as fake_err:
        MMSAdapter.log("Test log")
        assert "[TARS-MMS] Test log\n" in fake_err.getvalue()


def test_hardware_serial_adapter_disconnected():
    adapter = HardwareSerialAdapter(port="COM_NON_EXISTENT")
    # Should safely fail connection without crashing
    assert adapter.connect() is False
    # When disconnected, should safely return defaults
    assert adapter.read_sensors() == (False, False, False)
    assert adapter.send_motion("FORWARD 1") is False


def test_hardware_serial_adapter_mocked():
    adapter = HardwareSerialAdapter(wall_threshold_cm=10.0)
    mock_serial = MagicMock()
    # Mock telemetry response: front=8cm (<10 => True), left=15cm (>10 => False), right=5cm (<10 => True)
    mock_serial.readline.return_value = b"TELEM:8.0,15.0,5.0\n"
    adapter.serial_conn = mock_serial

    wf, wl, wr = adapter.read_sensors()
    assert wf is True
    assert wl is False
    assert wr is True

    assert adapter.send_motion("STEP_1") is True
    mock_serial.write.assert_called_with(b"STEP_1\n")
