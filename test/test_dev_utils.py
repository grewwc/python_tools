import unittest
from dev_utils.count_empty_space import count_start_empty_space

import pytest 

@pytest.mark.skip(reason='not pytest')
class TestDev_Utils(unittest.TestCase):
    def setUp(self):
        with open(__file__, 'r') as f:
            for line in f:
                if line.find('def') != -1:
                    self.line = line
                    break

    def test_count_start_empty_space(self):
        test_string = self.line
        self.assertEqual(4, count_start_empty_space(test_string))


if __name__ == '__main__':
    unittest.main()
