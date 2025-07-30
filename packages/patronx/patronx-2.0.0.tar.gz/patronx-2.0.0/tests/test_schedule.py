from datetime import datetime

import patronx.schedule as schedule


def _setup_scheduler_test(monkeypatch, attr):
    called = []

    # Fake send function to track calls
    monkeypatch.setattr(attr, "send", lambda: called.append(True))

    class FakeCronIter:
        def __init__(self, *args, **kwargs):
            self.count = 0

        def get_next(self, _type):
            self.count += 1
            if self.count > 1:
                raise StopIteration
            return datetime.utcnow()

    monkeypatch.setattr(schedule, "croniter", lambda expr, base: FakeCronIter())

    class FakeThread:
        def __init__(self, target, daemon=False):
            self.target = target
            self.daemon = daemon
            self.started = False

        def start(self):
            self.started = True
            try:
                self.target()
            except StopIteration:
                pass

    monkeypatch.setattr(schedule.threading, "Thread", FakeThread)

    return called, FakeThread

def test_start_backup_scheduler(monkeypatch):
    called, FakeThread = _setup_scheduler_test(monkeypatch, schedule.run_backup_job)
    t = schedule.start_backup_scheduler("* * * * *")
    assert isinstance(t, FakeThread)
    assert t.started
    assert called == [True]

def test_start_cleanup_scheduler(monkeypatch):
    called, FakeThread = _setup_scheduler_test(monkeypatch, schedule.cleanup_old_backups)
    t = schedule.start_cleanup_scheduler("* * * * *")
    assert isinstance(t, FakeThread)
    assert t.started
    assert called == [True]