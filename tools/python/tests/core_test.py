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

    def test_add_argument(self):
        """
        TESTS: sadface.add_argument(con_text=None, prem_text=None, con_id=None, prem_id=None)
        """
        sf.initialise()
        con1 = "You should treasure every moment"
        prem1 = ["if you are going to die then you should treasure every moment", "You are going to die"]
        arg1 = sf.add_argument(con_text=con1, prem_text=prem1, con_id=None, prem_id=None)

        self.assertEqual(con1, arg1.get("conclusion").get("text"))
        
        prem1_atom = sf.get_atom(arg1.get("premises")[0])
        self.assertEqual(prem1[0], prem1_atom.get("text"))

        prem2_atom = sf.get_atom(arg1.get("premises")[1])
        self.assertEqual(prem1[1], prem2_atom.get("text"))

    def test_add_conflict(self):
        """
        TESTS: add_conflict(arg_text=None, arg_id=None, conflict_text=None, conflict_id=None)
        """
        sf.initialise()
        a_text = "roses are red"
        c_text = "roses are white"
        conflict = sf.add_conflict(arg_text=a_text, conflict_text=c_text)

        self.assertEqual(a_text, conflict.get("argument").get("text"))
        self.assertEqual(c_text, conflict.get("conflict").get("text"))

        self.assertEqual("conflict", conflict.get("scheme").get("name"))


    def test_add_support(self):
        """
        TESTS: add_support(con_text=None, prem_text=None, con_id=None, prem_id=None)
        """
        sf.initialise()
        con1 = "You should treasure every moment"
        prem1 = ["if you are going to die then you should treasure every moment", "You are going to die"]
        arg1 = sf.add_support(con_text=con1, prem_text=prem1, con_id=None, prem_id=None)

        self.assertEqual(con1, arg1.get("conclusion").get("text"))
        
        prem1_atom = sf.get_atom(arg1.get("premises")[0])
        self.assertEqual(prem1[0], prem1_atom.get("text"))

        prem2_atom = sf.get_atom(arg1.get("premises")[1])
        self.assertEqual(prem1[1], prem2_atom.get("text"))


    def test_add_resource(self):
        """
        TESTS: sadface.add_resource(content)
        """
        sf.initialise()
        new_resource = sf.add_resource("DAKA DAKA")
        new_resource_content = new_resource.get("content")
        new_resource_type = new_resource.get("type")
        
        self.assertTrue(new_resource.get("id"))
        out = new_resource.get("id")
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

        self.assertTrue(new_resource.get("metadata"))
        self.assertTrue(type(new_resource.get("metadata")) is dict)

        expected = {"core"}
        self.assertEqual(set(expected), set(new_resource.get("metadata")))


        self.assertEqual(new_resource_content, "DAKA DAKA")
        self.assertEqual(new_resource_type, "text")

    def test_add_resource_metadata(self):
        """
        TESTS: sadface.add_resource_metadata()
        """
        sf.initialise()

         # Add a resource
        resource_text = "test resource"
        resource = sf.add_resource(resource_text)
        resource_id = resource.get("id")

        # Check resource metadata is empty
        resource = sf.get_resource(resource_id)
        self.assertEqual(resource_id, resource.get("id"))
        meta = resource.get("metadata").get("core")
        self.assertEqual(0, len(meta))

        # add metadata to core namespace
        sf.add_resource_metadata(resource_id, "core", "KEY1", "VALUE1")
        resource = sf.get_resource(resource_id)
        meta = resource.get("metadata").get("core")
        self.assertNotEqual(0, len(meta))
        self.assertEqual("VALUE1", meta.get("KEY1"))

        # add metadata to a new namespace
        sf.add_resource_metadata(resource_id, "META1", "KEY1", "VALUE1")
        resource = sf.get_resource(resource_id)
        meta = resource.get("metadata").get("META1")
        self.assertNotEqual(0, len(meta))
        self.assertEqual("VALUE1", meta.get("KEY1"))

    def test_add_source(self):
        """
        TESTS: sadface.add_source()
        """
        sf.initialise()

        # Add an atom
        text = "DAKA DAKA"
        atom = sf.add_atom(text)
        atom_id =  sf.contains_atom(text)
        
         # Add a resource
        resource_text = "test resource"
        resource = sf.add_resource(resource_text)
        resource_id = resource.get("id")

        # Add source to the atom, referencing the resource
        offset = 5
        length = len(resource_text)
        sf.add_source(atom_id, resource_id, resource_text, offset, length)

        # Now retrieve the source and test it
        s = sf.get_source(atom_id, resource_id)
        self.assertEqual(s.get("resource_id"), resource_id)
        self.assertEqual(s.get("text"), resource_text)
        self.assertEqual(s.get("offset"), offset)
        self.assertEqual(s.get("length"), length)

    def test_add_atom(self):
        """
        Tests: sadface.add_atom()
        """
        sf.initialise()

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

    def test_add_edge(self):
        """
        TESTS: sadface.add_edge()
        """
        sf.initialise()
        source = sf.add_atom("source")
        target = sf.add_atom("target")
        edge = sf.add_edge(source.get("id"), target.get("id"))

        retrieved_edge = sf.get_edge(edge.get("id"))
        self.assertEqual(retrieved_edge.get("source_id"), source.get("id"))
        self.assertEqual(retrieved_edge.get("target_id"), target.get("id"))
        self.assertEqual(retrieved_edge.get("id"), edge.get("id"))

    def test_add_atom_metadata(self):
        """
        TESTS: sadface.add_atom_metadata()
        """
        sf.initialise()

         # Add an atom
        atom_text = "test atom"
        atom = sf.add_atom(atom_text)
        atom_id = atom.get("id")

        # Check atom metadata is empty
        atom = sf.get_atom(atom_id)
        self.assertEqual(atom_id, atom.get("id"))
        meta = atom.get("metadata").get("core")
        self.assertEqual(0, len(meta))

        # add core metadata
        sf.add_atom_metadata(atom_id, "core", "KEY1", "VALUE1")
        atom = sf.get_atom(atom_id)
        meta = atom.get("metadata").get("core")
        self.assertNotEqual(0, len(meta))
        self.assertEqual("VALUE1", meta.get("KEY1"))

        # add metadata to new namespace
        sf.add_atom_metadata(atom_id, "META1", "KEY1", "VALUE1")
        atom = sf.get_atom(atom_id)
        meta = atom.get("metadata").get("META1")
        self.assertNotEqual(0, len(meta))
        self.assertEqual("VALUE1", meta.get("KEY1"))


    def test_add_global_metadata(self):
        """
        TESTS: sadface.add_global_metadata()
        """
        sf.initialise()

        # add core metadata
        sf.add_global_metadata("core", "KEY1", "VALUE1")
        sd = sf.get_document()
        meta = sd.get("metadata").get("core")
        self.assertEqual("VALUE1", meta.get("KEY1"))

        # add metadata to new namespace
        sf.add_global_metadata("META1", "KEY1", "VALUE1")
        sd = sf.get_document()
        meta = sd.get("metadata").get("META1")
        self.assertNotEqual(0, len(meta))
        self.assertEqual("VALUE1", meta.get("KEY1"))


    def test_add_notes(self):
        """
        Tests: sadface.add_notes()
        """
        sf.initialise()
        self.assertEqual(sf.get_notes(), None)

        text = "DAKA DAKA"
        sf.add_notes(text)
        self.assertEqual(sf.get_notes(), text)

        text2 = "MORE DAKA"
        sf.add_notes(text2)
        self.assertEqual(sf.get_notes(), text2)


    def test_add_scheme(self):
        """
        TESTS: sadface.add_scheme() wit default values

        Add a scheme, retrieve it, ensure that the retrieved
        scheme matches that which was added
        """
        sf.initialise()
        scheme = sf.add_scheme("test scheme")
        scheme_id = scheme.get("id")
        result = sf.get_scheme(scheme_id)
        result_id = result.get("id")
        self.assertEqual(result_id, scheme_id)

    def test_add_scheme_metadata(self):
        """
        TESTS: sadface.add_scheme_metadata()
        """
        sf.initialise()

         # Add an scheme
        scheme_text = "test scheme"
        scheme = sf.add_scheme(scheme_text)
        scheme_id = scheme.get("id")

        # Check scheme metadata is empty
        scheme = sf.get_scheme(scheme_id)
        self.assertEqual(scheme_id, scheme.get("id"))
        meta = scheme.get("metadata").get("core")
        self.assertEqual(0, len(meta))

        # add core metadata
        sf.add_scheme_metadata(scheme_id, "core", "KEY1", "VALUE1")
        scheme = sf.get_scheme(scheme_id)
        meta = scheme.get("metadata").get("core")
        self.assertNotEqual(0, len(meta))
        self.assertEqual("VALUE1", meta.get("KEY1"))

        # add metadata to new namespace
        sf.add_scheme_metadata(scheme_id, "META1", "KEY1", "VALUE1")
        scheme = sf.get_scheme(scheme_id)
        meta = scheme.get("metadata").get("META1")
        self.assertNotEqual(0, len(meta))
        self.assertEqual("VALUE1", meta.get("KEY1"))

    def test_append_notes(self):
        """
        TESTS: sadface.append_notes()
        """
        sf.initialise()
        text = "DAKA DAKA"
        sf.append_notes(text)
        self.assertEqual(sf.get_notes(), text)
        
        text2 = "MORE DAKA"
        sf.append_notes(text2)
        self.assertEqual(sf.get_notes(), text+text2)

    def test_clear_notes(self):
        """
        Tests: sadface.clear_notes()
        """
        sf.initialise()
        self.assertEqual(sf.get_notes(), None)

        text = "DAKA DAKA"
        sf.add_notes(text)
        self.assertEqual(sf.get_notes(), text)

        sf.clear_notes()
        self.assertEqual(sf.get_notes(), None)

    def test_contains_atom(self):
        """
        TESTS: sadface.contains_atom(atom_text)
        """
        sf.initialise()

        # Test Retrieving atom that doesn't exist
        self.assertEqual(None, sf.contains_atom("DAKA DAKA"))

        # Add new atom then test retrieving by text
        text = "DAKA DAKA"
        atom = sf.add_atom(text)
        atom_id =  sf.contains_atom(text)
        retrieved_atom = sf.get_atom(atom_id)
        self.assertEqual(atom, retrieved_atom)

    def test_delete_atom(self):
        """
        TESTS: sadface.delete_atom(atom_id)
        """
        sf.initialise()

        # Remove non-existing atom
        with self.assertRaises(ValueError):
            sf.delete_atom("TESTID")

        # Remove known existing atom
        atom = sf.add_atom("TESTATOM")
        retrieved = sf.get_atom(atom.get("id"))
        self.assertEqual(atom, retrieved)
        sf.delete_atom(atom.get("id"))
        retrieved = sf.get_atom(atom.get("id"))
        self.assertEqual(None, retrieved)

    def test_delete_edge(self):
        """
        TESTS: sadface.delete_edge(edge_id)
        """
        sf.initialise()

        # Remove non-existing edge
        with self.assertRaises(ValueError):
            sf.delete_edge("TESTID")
        
        # Remove known existing atom
        source_atom = sf.add_atom("SOURCE")
        target_atom = sf.add_atom("TARGET")
        edge = sf.add_edge(source_atom.get("id"), target_atom.get("id"))
        retrieved = sf.get_edge(edge.get("id"))
        self.assertEqual(edge, retrieved)

        sf.delete_edge(edge.get("id"))
        retrieved = sf.get_edge(edge.get("id"))
        self.assertEqual(None, retrieved)
        
    def test_delete_source(self):
        """
        TESTS: sadface.delete_source(atom_id, resource_id)
        """
        sf.initialise()

        # setup
        a = sf.add_atom("ATOM")
        r = sf.add_resource("hello")
        s = sf.add_source(a.get("id"), r.get("id"), "TEXT", 10, 4)

        # verify existing source
        retrieved = sf.get_source(a.get("id"), r.get("id"))
        self.assertEqual(s.get("id"), retrieved.get("id"))
        self.assertEqual(s, retrieved)

        # Delete source
        sf.delete_source(a.get("id"), r.get("id"))
        retrieved = sf.get_source(a.get("id"), r.get("id"))
        self.assertEqual(None, retrieved)


    def test_delete_resource(self):
        """
        TESTS: sadface.delete_resource(esource_id)
        """
        sf.initialise()

        # Remove non-existing resource
        with self.assertRaises(ValueError):
            sf.delete_resource("FAKE_ID")

        # Remove existing resource
        r = sf.add_resource("NEW RESOURCE")
        retrieved = sf.get_resource(r.get("id"))
        self.assertEqual(r, retrieved)

        sf.delete_resource(r.get("id"))

        retrieved = sf.get_resource(r.get("id"))
        self.assertEqual(None, retrieved)


    def test_delete_scheme(self):
        """
        """
        sf.initialise()

        # Remove non-existing scheme
        with self.assertRaises(ValueError):
            sf.delete_scheme("FAKE_ID")        

        # Remove existing scheme
        s = sf.add_scheme("TEST_SCHEME_NAME")
        retrieved = sf.get_scheme(s.get("id"))
        self.assertEqual(s, retrieved)

    def test_get_analyst(self):
        """
        TESTS: sadface.get_analyst()
        """
        sf.initialise()
        analyst = "A User"
        retrieved_analyst = sf.get_analyst()        
        self.assertEqual(retrieved_analyst, analyst)

    def test_get_atom(self):
        """
        TESTS: sadface.get_atom()
        """
        sf.initialise()
        self.assertEqual(sf.get_atom("unknown-id"), None)

        text = "DAKA DAKA"
        atom = sf.add_atom(text)
        atom_id = atom.get("id")
        result = sf.get_atom(atom_id)
        result_id = result.get("id")
        self.assertEqual(result_id, atom_id)

    def test_get_atom_id(self):
        """
        TESTS: sadface.get_atom_id()
        """
        sf.initialise()

        # Check behaviour when no atom to match against
        self.assertEqual(sf.get_atom_id("unknown-text"), None)

        # Add an atom, retrieve it by text content, and compare
        text = "DAKA DAKA"
        atom = sf.add_atom(text)
        atom_id = atom.get("id")
        retrieved_id = sf.get_atom_id(text)
        self.assertEqual(retrieved_id, atom_id)

    def test_get_atom_metadata(self):
        """
        TESTS: sadface.get_atom_metadata(atom_id, namespace=None, key=None)
        """
        sf.initialise()

        a = sf.add_atom("ATOM")
        sf.add_atom_metadata(a.get("id"), "TEST_NS", "TEST_KEY", "TEST_VAL")
        sf.add_atom_metadata(a.get("id"), "TEST_NS", "TEST_KEY2", "TEST_VA2")
        sf.add_atom_metadata(a.get("id"), "core", "TEST_KEY3", "TEST_VA3")

        expected = {'core': {'TEST_KEY3': 'TEST_VA3'}, 'TEST_NS': {'TEST_KEY': 'TEST_VAL', 'TEST_KEY2': 'TEST_VA2'}}
        m = sf.get_atom_metadata(a.get("id"))
        self.assertEqual(expected, m)

        expected = {'TEST_KEY3': 'TEST_VA3'}
        m = sf.get_atom_metadata(a.get("id"), "core")
        self.assertEqual(expected, m)

        expected = {'TEST_KEY': 'TEST_VAL', 'TEST_KEY2': 'TEST_VA2'}
        m = sf.get_atom_metadata(a.get("id"), "TEST_NS")
        self.assertEqual(expected, m)

        expected = "TEST_VA2"
        m = sf.get_atom_metadata(a.get("id"), "TEST_NS", "TEST_KEY2")
        self.assertEqual(expected, m)


    def test_get_atom_text(self):
        """
        TESTS: sadface.get_atom_text()
        """
        sf.initialise()

        # Check behaviour when no atom to match against
        self.assertEqual(sf.get_atom_text("unknown-id"), None)

        # Add an atom, retrieve it by text content, and compare
        text = "DAKA DAKA"
        atom = sf.add_atom(text)
        atom_id = atom.get("id")
        retrieved_text = sf.get_atom_text(atom_id)
        self.assertEqual(retrieved_text, text)


    def test_get_claim(self):
        """
        Tests: sadface.get_claim() with default values after init
        """
        sf.initialise()
        out = sf.get_claim()
        expected = None
        self.assertEqual(out, expected)

    def test_get_connections(self):
        """
        TESTS: sadface.get_connections()
        """
        sf.initialise()

        # Test with a non-existant ID
        results = sf.get_connections("TESTID")
        self.assertEqual([], results)

        # Test with existing ID that we create with no connections
        source_atom = sf.add_atom("SOURCE")
        results = sf.get_connections(source_atom.get("id"))
        self.assertEqual([], results)

        # Test with existing ID + known added connections
        target_atom = sf.add_atom("TARGET")
        edge = sf.add_edge(source_atom.get("id"), target_atom.get("id"))

        results = sf.get_connections(source_atom.get("id"))
        self.assertNotEqual([], results)
        self.assertEqual(len(results), 1)
        self.assertEqual(edge.get("id"), results[0].get("id"))
        self.assertEqual(source_atom.get("id"), results[0].get("source_id"))
        self.assertEqual(target_atom.get("id"), results[0].get("target_id"))


    def test_get_description(self):
        """
        Tests: sadface.get_description() with defaults values
        after init
        """
        sf.initialise()
        out = sf.get_description()
        expected = None
        self.assertEqual(out, expected)

    def test_get_document_id(self):
        """
        Tests: sadface.get_argument_id() with default values after init
        """
        sf.initialise()
        out = sf.get_document_id()
        result = False
        try:
            if UUID(out, version=4):
                result = True
        except:
            pass
        self.assertTrue(result)

    def test_get_edge(self):
        """
        TESTS: sadface.get_edge()
        """
        sf.initialise()
        source = sf.add_atom("source")
        target = sf.add_atom("target")
        edge = sf.add_edge(source.get("id"), target.get("id"))

        retrieved_edge = sf.get_edge(edge.get("id"))
        self.assertEqual(retrieved_edge.get("source_id"), source.get("id"))
        self.assertEqual(retrieved_edge.get("target_id"), target.get("id"))
        self.assertEqual(retrieved_edge.get("id"), edge.get("id"))

    def test_get_global_metadata(self):
        """
        TESTS: sadface.get_global_metadata(namespace=None, key=None)
        """
        sf.initialise()

        m = sf.get_global_metadata()

        v = sf.get_version()
        docid = sf.get_document_id()

        self.assertEqual(v, m.get("core").get("version"))
        self.assertEqual(docid, m.get("core").get("id") )

        sf.add_global_metadata("TEST_NS", "TEST_KEY", "TEST_VAL")
        sf.add_global_metadata("TEST_NS", "TEST_KEY2", "TEST_VA2")

        expected = {'TEST_KEY': 'TEST_VAL', 'TEST_KEY2': 'TEST_VA2'}
        m = sf.get_global_metadata("TEST_NS")
        self.assertEqual(expected, m)

        expected = "TEST_VA2"
        m = sf.get_global_metadata("TEST_NS", "TEST_KEY2")
        self.assertEqual(expected, m)

    def test_get_node(self):
        """
        TESTS: sadface.get_node()
        """
        sf.initialise()

        # Test with a non-existant ID
        result = sf.get_node("TEST")
        self.assertEqual(None, result)

        # Test with existin ID that we create
        atom = sf.add_atom("TESTATOM")
        result = sf.get_node(atom.get("id"))
        self.assertEqual(atom.get("id"), result.get("id"))

    def test_get_notes(self):
        """
        Tests: sadface.get_notes() with default values after init
        """
        sf.initialise()
        out = sf.get_notes()
        expected = None
        self.assertEqual(out, expected)

    def test_get_resource_metadata(self):
        """
        TESTS: sadface.get_atom_metadata(atom_id, namespace=None, key=None)
        """
        sf.initialise()

        r = sf.add_resource("RESOURCE")
        sf.add_resource_metadata(r.get("id"), "TEST_NS", "TEST_KEY", "TEST_VAL")
        sf.add_resource_metadata(r.get("id"), "TEST_NS", "TEST_KEY2", "TEST_VA2")
        sf.add_resource_metadata(r.get("id"), "core", "TEST_KEY3", "TEST_VA3")

        expected = {'core': {'TEST_KEY3': 'TEST_VA3'}, 'TEST_NS': {'TEST_KEY': 'TEST_VAL', 'TEST_KEY2': 'TEST_VA2'}}
        m = sf.get_resource_metadata(r.get("id"))
        self.assertEqual(expected, m)

        expected = {'TEST_KEY3': 'TEST_VA3'}
        m = sf.get_resource_metadata(r.get("id"), "core")
        self.assertEqual(expected, m)

        expected = {'TEST_KEY': 'TEST_VAL', 'TEST_KEY2': 'TEST_VA2'}
        m = sf.get_resource_metadata(r.get("id"), "TEST_NS")
        self.assertEqual(expected, m)

        expected = "TEST_VA2"
        m = sf.get_resource_metadata(r.get("id"), "TEST_NS", "TEST_KEY2")
        self.assertEqual(expected, m)

    def test_get_scheme(self):
        """
        TESTS: sadface.get_scheme() with default values
        """
        sf.initialise()
        result = sf.get_node("invalid-uuid")
        self.assertEqual(result, None)

    def test_get_scheme_metadata(self):
        """
        TESTS: sadface.get_scheme_metadata(scheme_id, namespace=None, key=None)
        """
        sf.initialise()

        a = sf.add_scheme("scheme")
        sf.add_scheme_metadata(a.get("id"), "TEST_NS", "TEST_KEY", "TEST_VAL")
        sf.add_scheme_metadata(a.get("id"), "TEST_NS", "TEST_KEY2", "TEST_VA2")
        sf.add_scheme_metadata(a.get("id"), "core", "TEST_KEY3", "TEST_VA3")

        expected = {'core': {'TEST_KEY3': 'TEST_VA3'}, 'TEST_NS': {'TEST_KEY': 'TEST_VAL', 'TEST_KEY2': 'TEST_VA2'}}
        m = sf.get_scheme_metadata(a.get("id"))
        self.assertEqual(expected, m)

        expected = {'TEST_KEY3': 'TEST_VA3'}
        m = sf.get_scheme_metadata(a.get("id"), "core")
        self.assertEqual(expected, m)

        expected = {'TEST_KEY': 'TEST_VAL', 'TEST_KEY2': 'TEST_VA2'}
        m = sf.get_scheme_metadata(a.get("id"), "TEST_NS")
        self.assertEqual(expected, m)

        expected = "TEST_VA2"
        m = sf.get_scheme_metadata(a.get("id"), "TEST_NS", "TEST_KEY2")
        self.assertEqual(expected, m)

    def test_get_source(self):
        """
        TESTS: sadface.get_source()
        """
        sf.initialise()

        # Add an atom
        text = "DAKA DAKA"
        atom = sf.add_atom(text)
        atom_id =  sf.contains_atom(text)
        
         # Add a resource
        resource_text = "test resource"
        resource = sf.add_resource(resource_text)
        resource_id = resource.get("id")

        s = sf.get_source(atom_id, resource_id)
        self.assertEqual(s, None)


        # Add source to the atom, referencing the resource
        offset = 5
        length = len(resource_text)
        sf.add_source(atom_id, resource_id, resource_text, offset, length)

        # Now retrieve the source and test it
        s = sf.get_source(atom_id, resource_id)
        self.assertEqual(s.get("resource_id"), resource_id)
        self.assertEqual(s.get("text"), resource_text)
        self.assertEqual(s.get("offset"), offset)
        self.assertEqual(s.get("length"), length)

    def test_get_title(self):
        """
        Tests: sadface.get_title() with defaults values
        after init
        """
        sf.initialise()
        out = sf.get_title()
        expected = None
        self.assertEqual(out, expected)

    def test_get_version(self):
        """
        Tests: sadface.get_version()
        """
        sf.initialise()
        out = sf.get_version()
        expected = "0.5"
        self.assertEqual(out, expected)

    def test_list_arguments(self):
        """
        Tests: sadface.get_arguments() with default values after init
        """
        sf.initialise()
        out = sf.list_arguments()
        expected = []
        self.assertEqual(out, expected)

    def test_list_atoms(self):
        """
        Tests: sadface.list_atoms() with default values after init
        """
        sf.initialise()
        out = sf.list_atoms()
        expected = []
        self.assertEqual(out, expected)

    def test_list_resources(self):
        """
        Tests: sadface.list_resources() 
        """
        sf.initialise()
        out = sf.list_resources()
        expected = []
        self.assertEqual(out, expected)

    def test_list_schemes(self):
        """
        Tests: sadface.get_arguments() with default values after init
        """
        sf.initialise()
        out = sf.list_schemes()
        expected = []
        self.assertEqual(out, expected)

    def test_get_created(self):
        """
        Tests: sadface.get_created()
        """
        sf.initialise()

        # Check that timestamp for creation time is a string
        timestamp = sf.get_created()
        self.assertEqual(True, isinstance(timestamp,str))

    def test_get_edited(self):
        """
        Tests: sadface.get_edited()
        """
        sf.initialise()

        # Check that timestamp for edited time is a string
        timestamp = sf.get_edited()
        self.assertEqual(True, isinstance(timestamp,str))

    def test_get_resource(self):
        """
        TESTS: sadface.get_resource(resource_id)
        """
        sf.initialise()
        new_resource = sf.add_resource("DAKA DAKA")
        new_resource_id = new_resource.get("id")
        
        retrieved_resource = sf.get_resource(new_resource_id)
        self.assertEqual(retrieved_resource, new_resource)
        

    def test_get_scheme(self):
        """
        TESTS: sadface.get_scheme() after a scheme has been added
        """
        sf.initialise()
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

        self.assertTrue(sd.get("metadata").get("core").get("id"))
        self.assertTrue(type(sd.get("metadata").get("core").get("id")) is str)
        out = sd.get("metadata").get("core").get("id")
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
        sf.initialise()
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

    def test_save(self):
        """
        """
        pass

    def test_set_analyst(self):
        """
        TESTS: sadface.set_analyst(analyst_name)
        """
        sf.initialise()

        # TEST 1: Default analyst
        self.assertEqual(sf.get_analyst(), "A User")

        # TEST 2: Set user then retrieve & compare
        new_user = "Known User"
        sf.set_analyst(new_user)
        retrieved_user = sf.get_analyst()
        self.assertEqual(new_user, retrieved_user)

    def test_set_atom_text(self):
        """
        TESTS: sadface.set_atom_text()
        """
        sf.initialise()

        atom = sf.add_atom("DAKA DAKA")
        atom_id = atom.get("id")
        sf.set_atom_text(atom_id, "MORE DAKA")
        self.assertEqual(sf.get_atom_text(atom_id),"MORE DAKA")

    def test_set_claim(self):
        """
        TESTS: sadface.set_claim()
        """
        sf.initialise()
        self.assertEqual(sf.get_claim(), None)

        atom = sf.add_atom("DAKA DAKA")
        atom_id = atom.get("id")
        sf.set_claim(atom_id)
        self.assertEqual(sf.get_claim(), atom_id)

    def test_set_created(self):
        """
        TESTS: sadface.set_analyst(analyst_name)
        """
        sf.initialise()

        # TEST 1: Set created timestamp then retrieve & compare
        timestamp = sf.now()
        sf.set_created(timestamp)
        retrieved_timestamp = sf.get_created()
        self.assertEqual(timestamp, retrieved_timestamp)

    def test_set_description(self):
        """
        Tests: sadface.get_description() & set_description

        1. Set description of doc to known value
        2. Retrieve description & compare
        """
        sf.initialise()
        d = "test description"
        sf.set_description(d)
        out = sf.get_description()
        expected = d
        self.assertEqual(out, expected)

    def test_set_edited(self):
        """
        TESTS: sadface.set_edited(timestamp)
        """
        sf.initialise()

        # TEST 1: Set edited timestamp then retrieve & compare
        timestamp = sf.now()
        sf.set_edited(timestamp)
        retrieved_timestamp = sf.get_edited()
        self.assertEqual(timestamp, retrieved_timestamp)

    def test_set_title(self):
        """
        Tests: sadface.get_title() & set_title
        """
        sf.initialise()
        t = "test title"
        sf.set_title(t)
        out = sf.get_title()
        expected = t
        self.assertEqual(out, expected)

    def test_set_document_id(self):
        """
        TESTS: sadface.set_document_id(id)
        """
        sf.initialise()
        current_id = sf.get_document_id()
        self.assertNotEqual(None, current_id)

        test_id = "1234567890abcdefgh"
        sf.set_document_id(test_id)
        current_id = sf.get_document_id()
        self.assertEqual(test_id, current_id)

    def test_set_scheme_name(self):
        """
        """
        sf.initialise()

        # Test setting non-existent scheme
        with self.assertRaises(Exception) as context:
            sf.set_scheme_name("TEST_ID", "TEST_NAME")
        out = str(context.exception)
        expected = 'Could not set the name of scheme: TEST_ID'
        self.assertEqual(out, expected)

        test_name = "TEST_SCHEME"
        s = sf.add_scheme(test_name)
        retrieved = sf.get_scheme(s.get("id"))
        self.assertEqual(s.get("name"), retrieved.get("name"))

        new_scheme_name = "NEW_SCHEME_NAME"
        sf.set_scheme_name(s.get("id"), new_scheme_name)
        retrieved = sf.get_scheme(s.get("id"))
        self.assertEqual(new_scheme_name, retrieved.get("name"))
        

    def test_verify(self):
        """
        """
        pass



if __name__ == "__main__":
    
    unittest.main()
