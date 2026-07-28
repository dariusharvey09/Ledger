#pomodoro timer - basic

import tkinter as tk

# DEFAULT SETTINGS
WORK_MINUTES = 25
BREAK_MINUTES = 5


class LedgerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ledger")
        self.root.geometry("320x260")
        self.root.resizable(False, False)

        self.is_work_session = True
        self.remaining_seconds = WORK_MINUTES * 60
        self.running = False
        self.timer_job = None #holds the .after() job id so it can be cancelled

        self._build_ui()
        self._update_display()

    def _build_ui(self):
        self.mode_label = tk.Label(
            self.root, text="Work Session", font=("Segoe UI", 14, "bold")
        )
        self.mode_label.pack(pady=(20, 5))

        self.time_label = tk.Label(self.root, text="25:00", font=("Segoe UI", 40))
        self.time_label.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        self.start_pause_btn = tk.Button(
            button_frame, text="Start", width=10, command=self.toggle_start_pause
        )
        self.start_pause_btn.grid(row=0, column=0, padx=5)

        self.skip_btn = tk.Button(
            button_frame, text="Skip", width=10, command=self.skip_session
        )
        self.skip_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(self.root, text="Reset", command=self.reset_timer)
        self.reset_btn.pack(pady=5)

    def toggle_start_pause(self):
        if self.running:
            self._pause()
        else:
            self._start()

    def _start(self):
        self.running = True
        self.start_pause_btn.config(text="Pause")
        self._tick()

    def _pause(self):
        self.running = False
        self.start_pause_btn.config(text="Start")
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def _tick(self):
        if not self.running:
            return

        if self.remaining_seconds <= 0:
            self._session.complete()
            return

        self._update_display()
        self.remaining_seconds -= 1
        self.timer_job = self.root.after(1000, self._tick)

    def _session_complete(self):
        self.running = False
        self.start_pause_btn.config(text="Start")
        # TO DO: log this completed session to SQLite here
        # TO DO: if this was a work session, trigger the reflection prompt here
        self._switch_session(auto=True)

    def skip_session(self):
        self._pause()
        # TO DO: log this an an incomplete/skipped session
        self._switch_session(auto=False)

    def _switch_session(self, auto):
        self.is_work_session = not self.is_work_session
        self.remaining_seconds = (
            WORK_MINUTES * 60 if self.is_work_session else "Break"
        )
        self._update_display()

    def reset_timer(self):
        self._pause()
        self.remaining_seconds = WORK_MINUTES * 60 if self.is_work_session else BREAK_MINUTES * 60
        self._update_display()

    def _update_display(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LedgerApp(root)
    root.mainloop()
