# logger.py
# 05/18/2025 - Voltur
#
# A logging utility that lets you print to stderr.
# 


from datetime import datetime

class _Logger:
    def __init__(self):
        self.log_file_name = None
        self.log_file_handle = None
        self.screen_output_enabled = True
        self.report_mode_enabled = False
        self.log_to_file_levels = {"info", "summary", "warn", "error", "report"}
        self.log_to_console_levels = {"progress", "debug", "help", "summary", "warn", "info", "error"}

    def set_log_file(self, filename):
        self.log_file_name = filename
        self.log_file_handle = open(filename, "a", encoding="utf-8")
        self.report_mode_enabled = True
        self.debug(f"Logging enabled: {self.log_file_name}")

    def log(self, msg, timestamp=False, level="info"):
        if timestamp:
            msg = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"

        # Print everything except progress if we're printing everythign to console
        should_echo_to_screen = False
        if self.screen_output_enabled:
            if self.report_mode_enabled:
                if level in self.log_to_console_levels:
                    should_echo_to_screen = True
            else:
                if level != "progress":  # Don't spam when printing full report
                    should_echo_to_screen = True

        # Print to console
        if should_echo_to_screen:
            print(msg)

        # Print to log file
        if level in self.log_to_file_levels:
            self.write_to_file(msg)

    def write_to_file(self, msg):
        if self.log_file_handle:
            self.log_file_handle.write(msg + "\n")
            self.log_file_handle.flush()

    def close(self):
        if self.log_file_handle:
            self.log_file_handle.close()
            self.log_file_handle = None
        self.report_mode_enabled = False

    def describe_levels(self):
        self.help("Logger config:")
        self.help(f"- Console: {sorted(self.log_to_console_levels)}")
        self.help(f"- File:    {sorted(self.log_to_file_levels)}")

    def __del__(self):
        self.close()

    # Public logging interface
    def warn(self, msg, **kwargs):    self.log(msg, level="warn", **kwargs)
    def error(self, msg, **kwargs):   self.log(msg, level="error", **kwargs)
    def debug(self, msg, **kwargs):   self.log(msg, level="debug", **kwargs)

    # Workflow/status indicators
    def progress(self, msg, **kwargs): self.log(msg, level="progress", **kwargs)
    def summary(self, msg, **kwargs):  self.log(msg, level="summary", **kwargs)
    def report(self, msg, **kwargs):   self.log(msg, level="report", **kwargs)

    # Command/help output
    def help(self, msg, **kwargs):     self.log(msg, level="help", **kwargs)


Logger = _Logger()