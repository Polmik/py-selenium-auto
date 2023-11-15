from datetime import datetime, timedelta


class Timer:
    @property
    def elapsed(self) -> timedelta:
        return self.end_date - self.start_time

    def __enter__(self):
        self.start_time = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_date = datetime.now()
