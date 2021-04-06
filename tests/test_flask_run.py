import unittest
import subprocess

class SimpleTest(unittest.TestCase):
    def test_starts_without_fail(self):
        result = subprocess.call('gunicorn ../setup:app')
        print(result)

if __name__ == '__main__':
    unittest.main()