from learning.services.utils import calculate_percentage


class TestCalculatePercentage:
    def test_normal_case(self):
        assert calculate_percentage(1, 4) == 25

    def test_full_completion(self):
        assert calculate_percentage(10, 10) == 100

    def test_zero_completed(self):
        assert calculate_percentage(0, 10) == 0

    def test_zero_total_returns_zero(self):
        assert calculate_percentage(0, 0) == 0

    def test_rounds_to_nearest_integer(self):
        # 1/3 ≈ 33.33... → rounds to 33
        assert calculate_percentage(1, 3) == 33

    def test_rounds_up_when_appropriate(self):
        # 2/3 ≈ 66.67... → rounds to 67
        assert calculate_percentage(2, 3) == 67
