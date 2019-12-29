import unittest


def add(a, b):
    return a + b


class MyClass(unittest.TestCase):

    def setUp(self):
        print("start test case")

    def tearDown(self):
        print("end test case")

    def test_case(self):
        c = add(3, 4)
        self.assertEqual(c, 7)

    def test_case2(self):
        c = add(3.1, 4.2)
        self.assertEqual(c, 7.300000000000001)

    def test_case3(self):
        c = add(-13, 4)
        self.assertEqual(c, -9)

    def test_case4(self):
        c = add("a", "b")
        self.assertEqual(c, "ab")


if __name__ == '__main__':
    unittest.main()
