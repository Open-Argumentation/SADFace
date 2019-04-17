import json
import os
import unittest

import sadface as sf

class TestConfig(unittest.TestCase):
    def setUp(self):
        sf.reset()        

    def tearDown(self):
        sf.reset()
    
    def test_set_location(self):
        """
        Tests: sadface.config.set_location()

        """
        sf.config.set_location("deploy/etc/test.cfg")
        out = sf.config.location
        expected = "deploy/etc/test.cfg"
        self.assertEqual(out, expected)

if __name__ == "__main__":
    
    unittest.main()
