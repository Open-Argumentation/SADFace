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

    def test_default_add_atom(self):
        """
        Tests: sadface.add_atom()
        """
        sf.init()

        # Check we have no atoms in the default document
        num_atoms = len(sf.list_atoms())
        self.assertEqual(num_atoms, 0)

        # Add an atom then check how many atoms we have
        atom_text = "test atom"
        atom = sf.add_atom(atom_text)
        atom_id = atom.get("id")
        num_atoms = len(sf.list_atoms())
        self.assertEqual(num_atoms, 1)

        # Retrieve the new atom and check that it
        # contains the expected text
        atom = sf.get_atom(atom_id)
        self.assertEqual(atom.get("text"), atom_text)

    def test_default_add_notes(self):
        """
        Tests: sadface.add_notes()
        """
        sf.init()
        self.assertEqual(sf.get_notes(), None)
        text = "DAKA DAKA"
        sf.add_notes(text)
        self.assertEqual(sf.get_notes(), text)

    def test_default_append_notes(self):
        """
        TESTS: sadface.append_notes()
        """
        sf.init()
        text = "DAKA DAKA"
        sf.append_notes(text)
        self.assertEqual(sf.get_notes(), text)
        
        text2 = "MORE DAKA"
        sf.append_notes(text2)
        self.assertEqual(sf.get_notes(), text+text2)
        

    def test_default_get_claim(self):
        """
        Tests: sadface.get_claim() with default values after init
        """
        sf.init()
        out = sf.get_claim()
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
        expected = None
        self.assertEqual(out, expected)

    def test_default_get_scheme(self):
        """

        """
        sf.init()
        result = sf.get_node("invalid-uuid")
        self.assertEqual(result, None)

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

    def test_get_scheme(self):
        """
        TESTS: sadface.get_scheme() after a scheme has been added
        """
        sf.init()
        scheme_node = sf.add_scheme("test-scheme")
        scheme_node_id = scheme_node.get("id")

        result = sf.get_scheme(scheme_node_id)
        self.assertEqual(result.get("id"), scheme_node_id)
        self.assertEqual(result.get("text"), scheme_node.get("text"))

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
