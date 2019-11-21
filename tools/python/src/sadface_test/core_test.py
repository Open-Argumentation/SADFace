import datetime
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

    def test_add_resource(self):
        """
        TESTS: sadface.add_resource(content)

        "content":content, "type":"text", "metadata":{ "core": {}}
        """
        sf.init()
        new_resource = sf.add_resource("DAKA DAKA")
        new_resource_content = new_resource.get("content")
        new_resource_type = new_resource.get("type")
        
        self.assertTrue(new_resource.get("id"))
        self.assertTrue(new_resource.get("metadata"))
        self.assertTrue(type(new_resource.get("metadata")) is dict)

        expected = {"core"}
        self.assertEquals(set(expected), set(new_resource.get("metadata")))


        self.assertEqual(new_resource_content, "DAKA DAKA")
        self.assertEqual(new_resource_type, "text")

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

        text2 = "MORE DAKA"
        sf.add_notes(text2)
        self.assertEqual(sf.get_notes(), text2)

    def test_default_add_scheme(self):
        """
        TESTS: sadface.add_scheme() wit default values

        Add a scheme, retrieve it, ensure that the retrieved
        scheme matches that which was added
        """
        sf.init()
        scheme = sf.add_scheme("test scheme")
        scheme_id = scheme.get("id")
        result = sf.get_scheme(scheme_id)
        result_id = result.get("id")
        self.assertEqual(result_id, scheme_id)

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

    def test_default_clear_notes(self):
        """
        Tests: sadface.clear_notes()
        """
        sf.init()
        self.assertEqual(sf.get_notes(), None)

        text = "DAKA DAKA"
        sf.add_notes(text)
        self.assertEqual(sf.get_notes(), text)

        sf.clear_notes()
        self.assertEqual(sf.get_notes(), None)

    def test_default_get_analyst(self):
        """
        TESTS: sadface.get_analyst()
        """
        sf.init()
        analyst = "A User"
        retrieved_analyst = sf.get_analyst()        
        self.assertEqual(retrieved_analyst, analyst)

    def test_default_get_atom(self):
        """
        TESTS: sadface.get_atom()
        """
        sf.init()
        self.assertEqual(sf.get_atom("unknown-id"), None)

        text = "DAKA DAKA"
        atom = sf.add_atom(text)
        atom_id = atom.get("id")
        result = sf.get_atom(atom_id)
        result_id = result.get("id")
        self.assertEqual(result_id, atom_id)

    def test_default_get_atom_id(self):
        """
        TESTS: sadface.get_atom_id()
        """
        sf.init()

        # Check behaviour when no atom to match against
        self.assertEqual(sf.get_atom_id("unknown-text"), None)

        # Add an atom, retrieve it by text content, and compare
        text = "DAKA DAKA"
        atom = sf.add_atom(text)
        atom_id = atom.get("id")
        retrieved_id = sf.get_atom_id(text)
        self.assertEqual(retrieved_id, atom_id)

    def test_default_get_atom_text(self):
        """
        TESTS: sadface.get_atom_text()
        """
        sf.init()

        # Check behaviour when no atom to match against
        self.assertEqual(sf.get_atom_text("unknown-id"), None)

        # Add an atom, retrieve it by text content, and compare
        text = "DAKA DAKA"
        atom = sf.add_atom(text)
        atom_id = atom.get("id")
        retrieved_text = sf.get_atom_text(atom_id)
        self.assertEqual(retrieved_text, text)


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
        TESTS: sadface.get_scheme() with default values
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

    def test_get_resource(self):
        """
        TESTS: sadface.get_resource(resource_id)
        """
        sf.init()
        new_resource = sf.add_resource("DAKA DAKA")
        new_resource_id = new_resource.get("id")
        
        retrieved_resource = sf.get_resource(new_resource_id)
        self.assertEqual(retrieved_resource, new_resource)
        

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

    def test_new_atom(self):
        """
        TESTS: sadface.new_atom()

        An atom dict should look like this:

            {"id":new_uuid(), "type":"atom", "text":text, "sources":[], "metadata":{}}

        So we check that it has the right keys and default values
        """
        text = "DAKA DAKA"
        atom = sf.new_atom(text)
        self.assertTrue(atom.get("id"))
        self.assertTrue(atom.get("type"))
        self.assertTrue(atom.get("type"), "atom")
        self.assertTrue(atom.get("text"))
        self.assertTrue(atom.get("text"), text)
        self.assertTrue(type(atom.get("sources")) is list)
        self.assertEqual(len(atom.get("sources")), 0)
        self.assertTrue(type(atom.get("metadata")) is dict)
        self.assertTrue(atom.get("metadata"))

    def test_new_edge(self):
        """
        TESTS: sadface.new_edge()

        An edge dict should look like this:

            {"id":new_uuid(), "source_id":source_id, "target_id":target_id}

        So we check that it has the right keys and default values
        """
        text = "DAKA DAKA"
        src_atom = sf.new_atom(text)
        src_id = src_atom.get("id")
        dest_atom = sf.new_atom(text)
        dest_id = dest_atom.get("id")

        edge = sf.new_edge(src_id, dest_id)

        self.assertTrue(edge.get("id"))
        out = edge.get("id")
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

        self.assertTrue(edge.get("source_id"))
        out = edge.get("source_id")
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

        self.assertTrue(edge.get("target_id"))
        out = edge.get("target_id")
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

    def test_new_resource(self):
        """
        TESTS: sadface.new_resource()
        """
        content = "DAKA DAKA"
        res = sf.new_resource(content)
        
        self.assertTrue(res.get("id"))
        out = res.get("id")
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

        self.assertTrue(res.get("content"))
        self.assertEqual(res.get("content"), content)

        self.assertTrue(res.get("type"))
        self.assertEqual(res.get("type"), "text")

        self.assertTrue(res.get("metadata"))
        self.assertTrue(type(res.get("metadata")) is dict)


    def test_new_sadface(self):
        """
        TESTS: sadface.new_sadface()
        """
        sd = sf.new_sadface()

        self.assertTrue(sd.get("metadata"))
        self.assertTrue(type(sd.get("metadata")) is dict)

        self.assertTrue(sd.get("metadata").get("core"))
        self.assertTrue(type(sd.get("metadata").get("core")) is dict)

        self.assertTrue(sd.get("metadata").get("core").get("version"))
        self.assertTrue(type(sd.get("metadata").get("core").get("version")) is str)

        self.assertTrue(sd.get("id"))
        self.assertTrue(type(sd.get("id")) is str)
        out = sd.get("id")
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)
        
        self.assertTrue(sd.get("metadata").get("core").get("analyst_name"))
        self.assertTrue(type(sd.get("metadata").get("core").get("analyst_name")) is str)
        
        self.assertTrue(sd.get("metadata").get("core").get("analyst_email"))
        self.assertTrue(type(sd.get("metadata").get("core").get("analyst_email")) is str)
        
        self.assertTrue(sd.get("metadata").get("core").get("created"))
        self.assertTrue(type(sd.get("metadata").get("core").get("created")) is str)

        self.assertTrue(sd.get("metadata").get("core").get("edited"))
        self.assertTrue(type(sd.get("metadata").get("core").get("edited")) is str)

        self.assertTrue(type(sd.get("resources")) is list)
        self.assertEqual(len(sd.get("resources")), 0)
        
        self.assertTrue(type(sd.get("nodes")) is list)
        self.assertEqual(len(sd.get("nodes")), 0)

        self.assertTrue(type(sd.get("edges")) is list)
        self.assertEqual(len(sd.get("edges")), 0)

    def test_new_scheme(self):
        """
        TESTS: sadface.new_scheme()
        """
        name = "DAKA"
        sch = sf.new_scheme(name)

        self.assertTrue(sch.get("id"))
        out = sch.get("id")
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

        self.assertTrue(sch.get("type"))
        self.assertEqual(sch.get("type"), "scheme")

        self.assertTrue(sch.get("name"))
        self.assertEqual(sch.get("name"), name)

        self.assertTrue(sch.get("metadata"))
        self.assertTrue(type(sch.get("metadata")) is dict)
    
    def test_new_source(self):
        """
        TESTS: sadface.new_source()
        {"resource_id":resource_id, "text":text, "offset":offset, "length":length}
        """
        test_id = sf.new_uuid()
        test_txt = "DAKA DAKA MORE DAKA"
        test_offset = 100
        src = sf.new_source(test_id, test_txt, test_offset)

        self.assertTrue(src.get("resource_id"))
        out = src.get("resource_id")
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

        self.assertTrue(src.get("text"))
        self.assertEqual(src.get("text"), test_txt)
    
        self.assertTrue(src.get("offset"))
        self.assertEqual(src.get("offset"), test_offset)

        self.assertTrue(src.get("length"))
        self.assertEqual(src.get("length"), len(test_txt))

    def test_new_uuid(self):
        """
        TESTS: sadface.new_uuid()
        """
        out = sf.new_uuid()
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

    def test_now(self):
        """
        TESTS: sadface.now()
        """
        current = datetime.datetime.fromisoformat(sf.now())
        
        self.assertTrue(type(current) is datetime.datetime)

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

    def test_set_atom_text(self):
        """
        TESTS: sadface.set_atom_text()
        """
        sf.init()

        atom = sf.add_atom("DAKA DAKA")
        atom_id = atom.get("id")
        sf.set_atom_text(atom_id, "MORE DAKA")
        self.assertEqual(sf.get_atom_text(atom_id),"MORE DAKA")

    def test_set_claim(self):
        """
        TESTS: sadface.set_claim()
        """
        sf.init()
        self.assertEqual(sf.get_claim(), None)

        atom = sf.add_atom("DAKA DAKA")
        atom_id = atom.get("id")
        sf.set_claim(atom_id)
        self.assertEqual(sf.get_claim(), atom_id)


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
