import unittest

class SimpleTest(unittest.TestCase):
    def testFail(self):
        self.failUnless(True)

if __name__ == '__main__':
    unittest.main()