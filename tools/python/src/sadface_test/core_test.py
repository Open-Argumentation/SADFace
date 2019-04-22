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
        out = sf.get_version()
        expected = "0.2"
        self.assertEqual(out, expected)

    def test_get_description(self):
        """
        Tests: sadface.get_description() with defaults values
        after init
        """
        sf.init()
        out = sf.get_description()
        expected = None
        self.assertEqual(out, expected)


    def test_set_description(self):
        """
        Tests: sadface.get_description() & set_description

        1. Set description of doc to known value
        2. Retrieve description & compare
        """
        sf.init()
        d = "test description"
        sf.set_description(d)
        out = sf.get_description()
        expected = d
        self.assertEqual(out, expected)


    def test_get_title(self):
        """
        Tests: sadface.get_title() with defaults values
        after init
        """
        sf.init()
        out = sf.get_title()
        expected = None
        self.assertEqual(out, expected)

    def test_set_title(self):
        """
        Tests: sadface.get_title() & set_title
        """
        sf.init()
        t = "test title"
        sf.set_title(t)
        out = sf.get_title()
        expected = t
        self.assertEqual(out, expected)



if __name__ == "__main__":
    
    unittest.main()
