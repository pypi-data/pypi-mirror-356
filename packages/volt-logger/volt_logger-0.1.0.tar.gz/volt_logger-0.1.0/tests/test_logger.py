import io
import sys
import os
from voltlogger import Logger

def test_log_to_console(monkeypatch):
    captured = io.StringIO()
    monkeypatch.setattr(sys, "stdout", captured)

    Logger.screen_output_enabled = True
    Logger.report_mode_enabled = False
    Logger.log("Test message", level="info")
    
    output = captured.getvalue()
    assert "Test message" in output

def test_log_to_file(tmp_path):
    log_path = tmp_path / "test_log.txt"
    Logger.set_log_file(str(log_path))
    Logger.log("File log test", level="info")
    Logger.close()

    with open(log_path, "r", encoding="utf-8") as f:
        contents = f.read()
    
    assert "File log test" in contents

def test_logger_levels(monkeypatch):
    captured = io.StringIO()
    monkeypatch.setattr(sys, "stdout", captured)
    
    Logger.help("Help message test")
    output = captured.getvalue()
    assert "Help message test" in output
