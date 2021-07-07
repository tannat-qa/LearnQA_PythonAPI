class TestExample:
    def test_check_math(self):
        a = 5
        b = 9
        excpected_sum = 14
        assert a+b == excpected_sum, f"Sum of variables a and b is not equal to {excpected_sum}"

    def test_check_math2(self):
        a = 5
        b = 11
        excpected_sum = 14
        assert a+b == excpected_sum, f"Sum of variables a and b is not equal to {excpected_sum}"