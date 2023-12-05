import unittest
from PyQuizGame_Logic import display_score,check_answer


class TestCosmic(unittest.TestCase):

    """
    test cases must start with test and must be a method
    """
    file = open('./test_input.txt')
    def test1_answer(self) -> None:# testing score display
        a = 10
        b = 5
        ans = 50
        self.assertEqual(display_score(b,a), ans, 'broken')

    def test2_answer(self) -> None:# testing score display
        a = 10
        b = 9
        ans = 90
        self.assertEqual(display_score(b, a), ans, 'broken')

    def test3_answer(self) -> None:# testing correct answer test
        a = "Hello"
        b = "Hello"
        ans:bool = True
        self.assertEqual(check_answer(a,b), ans, 'broken')
    def test4_answer(self) -> None:# testing correct answer test
        a = "Goodbye"
        b = "Hello"
        ans:bool = False
        self.assertEqual(check_answer(a,b), ans, 'broken')

if __name__ == "__main__":
    unittest.main(verbosity=2)
