import json
import os
import unittest

import sadface as sf
#import sadface.config

class TestCore(unittest.TestCase):
    def setUp(self):
        sf.reset()

    def tearDown(self):
        sf.reset()

    def test_get_version(self):
        """
        Tests: sadface.get_version()
        """
        sf.init()
        out = sf.get_version();
        expected = "0.2"
        self.assertEqual(out, expected)

if __name__ == "__main__":
    
    unittest.main()
