import unittest
from unittest.mock import patch

# from controller import Controller
import controller
c = controller.Controller()


class TestController(unittest.TestCase):

    @patch('builtins.input', return_value='food')
    def test_validate_word(self, input):
        self.assertEqual(c.validate_word(), 'food')

    @patch('builtins.input', return_value='55food')
    def test_validate_int_before_word(self, input):
        self.assertFalse(c.validate_word(), False)

    @patch('builtins.input', return_value='55food')
    def test_validate_word_int_raise_error(self, input):
        try:
            c.validate_word()
        except:
            raise ValueError('should raise an exception')

    @patch('builtins.input', return_value='#$%#%food')
    def test_validate_word_symbols_raise_error(self, input):
        try:
            c.validate_word()
        except:
            raise ValueError('should raise an exception')

    @patch('builtins.input', return_value="\U0001f600")  # emoji
    def test_validate_emoji_passes(self, input):
        self.assertEqual(c.validate_word(), None)


    def test_pattern_word(self):
        x = "some_word"
        self.assertRegex(x, r"^[a-zA-Z_][a-zA-Z0-9_]+$")


    def test_pattern_int_between_letters(self):
        x = "so4me_w4o4rd"
        self.assertRegex(x, r"^[a-zA-Z_][a-zA-Z0-9_]+$")

    def test_validate_date_in_expense_pattern(self):
        x = "11%12%2021 donuts - 40"
        pattern = r"^((\d{2}[^a-zA-Z\d\s]\d{2}[^a-zA-Z\d\s](?:20[1-1][0-9]|200[0-9]|202[0-1]))" \
                  r"(\s+[a-zA-Z_][a-zA-Z0-9_]+\s+)(?:-)(\s+[1-9][0-9]*|[0]?)\s*)$"
        self.assertRegex(x, pattern)

    def test_validate_spaces_in_expense_pattern(self):
        x = "  11/12/2021      donuts   -  40  "
        pattern = r"^\s*((\d{2}[^a-zA-Z\d\s]\d{2}[^a-zA-Z\d\s](?:20[1-1][0-9]|200[0-9]|202[0-1]))" \
                    r"(\s+[a-zA-Z_][a-zA-Z0-9_]+\s+)(?:-)(\s+[1-9][0-9]*|[0]?)\s*)$"
        self.assertRegex(x, pattern)



    @patch('builtins.input', return_value="00.00.2021")
    def test_validate_date_zeros_raise_error(self, input):
        try:
            c.validate_word()
        except:
            raise ValueError('should raise an exception')

    @patch('builtins.input', return_value="32.11.2021")
    def test_validate_date_day_raise_error(self, input):
        try:
            c.validate_word()
        except:
            raise ValueError('should raise an exception')

    @patch('builtins.input', return_value="01.31.2021")
    def test_validate_date_month_raise_error(self, input):
        try:
            c.validate_word()
        except:
            raise ValueError('should raise an exception')

    @patch('builtins.input', return_value="20.11.2099")
    def test_validate_date__big_year_raise_error(self, input):
        try:
            c.validate_word()
        except:
            raise ValueError('should raise an exception')

    # input date bigger than today
    def test_compare_dates(self):
        s = "29.11.2021"
        with self.assertRaises(ValueError):
            c.compare_dates(s)

    @patch('builtins.input', return_value="3")
    def test_get_fk_user_id_int_input(self, input):
        try:
            c.get_fk_user_id()
        except:
            raise ValueError('number should be int')

    @patch('builtins.input', return_value=3.0)
    def test_get_fk_user_id_float_input(self, input):
        try:
            c.get_fk_user_id()
        except:
            raise ValueError('number should be int')


if __name__ == '__main__':
    unittest.main()
