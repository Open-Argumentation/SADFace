import json
import os
import unittest

from uuid import UUID

import sadface as sf

class TestCore(unittest.TestCase):
    def setUp(self):
        sf.reset()

    def tearDown(self):
        sf.reset()

    def test_default_get_claim(self):
        """
        Tests: sadface.get_claim() with default values after init
        """
        sf.init()
        out = sf.get_claim()
        print(out)
        expected = None
        self.assertEqual(out, expected)

    def test_default_get_description(self):
        """
        Tests: sadface.get_description() with defaults values
        after init
        """
        sf.init()
        out = sf.get_description()
        expected = None
        self.assertEqual(out, expected)

    def test_default_get_document_id(self):
        """
        Tests: sadface.get_argument_id() with default values after init
        """
        sf.init()
        out = sf.get_document_id()
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

    def test_default_get_notes(self):
        """
        Tests: sadface.get_notes() with default values after init
        """
        sf.init()
        out = sf.get_notes()
        print(out)
        expected = None
        self.assertEqual(out, expected)

    def test_default_get_title(self):
        """
        Tests: sadface.get_title() with defaults values
        after init
        """
        sf.init()
        out = sf.get_title()
        expected = None
        self.assertEqual(out, expected)

    def test_default_get_version(self):
        """
        Tests: sadface.get_version()
        """
        sf.init()
        out = sf.get_version()
        expected = "0.2"
        self.assertEqual(out, expected)

    def test_default_list_arguments(self):
        """
        Tests: sadface.get_arguments() with default values after init
        """
        sf.init()
        out = sf.list_arguments()
        expected = []
        self.assertEqual(out, expected)

    def test_default_list_atoms(self):
        """
        Tests: sadface.list_atoms() with default values after init
        """
        sf.init()
        out = sf.list_atoms()
        expected = []
        self.assertEqual(out, expected)

    def test_default_list_schemes(self):
        """
        Tests: sadface.get_arguments() with default values after init
        """
        sf.init()
        out = sf.list_schemes()
        expected = []
        self.assertEqual(out, expected)

    def test_reset(self):
        """
        Tests: sadface.reset()

        A sadface document is created and manipulated then reset is used
        to return the document to it's initial state
        """

        # Iniitialise a SADFace document
        sf.init()
        expected = None
        out = sf.get_title()
        self.assertEqual(out, expected)

        # Explicitly alter it
        expected = "DAKA DAKA"
        sf.set_title(expected)
        out = sf.get_title()
        self.assertEqual(out, expected)

        # Reset the document - this should now be in the pre-init, empty-dict state
        sf.reset()
        expected = {}
        out = sf.sd
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