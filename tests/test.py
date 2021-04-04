import unittest

class SimpleTest(unittest.TestCase):
    def test(self):
        self.failUnless(False)

if __name__ == '__main__':
    unittest.main()