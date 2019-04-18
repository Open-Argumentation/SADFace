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

class TestLoad(unittest.TestCase):
    def setUp(self):
        sf.reset()
        sf.config.set_location("etc/defaults.cfg")

    def tearDown(self):
        sf.reset()

    def test_load(self):
        """
        Tests: sadface.config.load()

        """
        sf.config.load()
        out = sf.config.current.get("analyst", "name")
        expected = 'A User'
        self.assertEqual(out, expected)

class TestLoadNoConfig(unittest.TestCase):
    def setUp(self):
        sf.reset()

    def tearDown(self):
        sf.reset()
    
    def test_load_no_config(self):
        """
        Tests: sadface.config.load()

        Ensure that if load is called but location isn't set then an
        exception must be raised
        """
        with self.assertRaises(Exception) as context:
            sf.config.load()
        out = str(context.exception)
        expected = 'Tried to load config file but location is set to None'
        self.assertEqual(out, expected)


if __name__ == "__main__":
    
    unittest.main()
