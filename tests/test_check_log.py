import pytest
from check_log import CheckLog
from datetime import datetime

def test_check_log_creation():
    log1 = CheckLog(habit_id= 1)
    assert log1.habit_id == 1

def test_check_log_date_automatically_set():
    log1 = CheckLog(habit_id=1)
    assert log1.check_off_date is not None

def test_check_log_log_id_default():
    log1 = CheckLog(habit_id = 1)
    assert log1.log_id is None
