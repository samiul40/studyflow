from learning.templatetags.learning_filters import (
    format_duration,
    hours_from_minutes,
    remaining_mins,
)


class TestFormatDuration:
    def test_zero_returns_0m(self):
        assert format_duration(0) == "0m"

    def test_none_returns_0m(self):
        assert format_duration(None) == "0m"

    def test_minutes_only(self):
        assert format_duration(45) == "45m"

    def test_hours_only(self):
        assert format_duration(120) == "2h"

    def test_hours_and_minutes(self):
        assert format_duration(90) == "1h 30m"

    def test_exactly_one_hour(self):
        assert format_duration(60) == "1h"

    def test_one_minute(self):
        assert format_duration(1) == "1m"

    def test_large_value(self):
        assert format_duration(150) == "2h 30m"


class TestHoursFromMinutes:
    def test_zero_returns_0(self):
        assert hours_from_minutes(0) == 0

    def test_none_returns_0(self):
        assert hours_from_minutes(None) == 0

    def test_less_than_one_hour(self):
        assert hours_from_minutes(45) == 0

    def test_exactly_one_hour(self):
        assert hours_from_minutes(60) == 1

    def test_90_minutes_returns_1(self):
        assert hours_from_minutes(90) == 1

    def test_120_minutes_returns_2(self):
        assert hours_from_minutes(120) == 2


class TestRemainingMins:
    def test_zero_returns_0(self):
        assert remaining_mins(0) == 0

    def test_none_returns_0(self):
        assert remaining_mins(None) == 0

    def test_less_than_one_hour(self):
        assert remaining_mins(45) == 45

    def test_exactly_one_hour_returns_0(self):
        assert remaining_mins(60) == 0

    def test_90_minutes_returns_30(self):
        assert remaining_mins(90) == 30

    def test_120_minutes_returns_0(self):
        assert remaining_mins(120) == 0
