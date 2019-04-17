import json
import os
import sadface as sf 
import unittest

class TestSADFaceFunctions(unittest.TestCase):
    def setUp(self):
       pass

    def tearDown(self):
        pass
    
    def test_init(self):
        """
        Tests: sadface.init()

        init() returns a dict containing data, e.g. dates & UUIDs, that can vary on each invokation
        so the values for these keys are emptied before comparing to a dict loaded from a known
        good JSON string.
        """
        out = sf.init()
        out['metadata']['core']['created'] = ""
        out['metadata']['core']['edited'] = ""
        out['metadata']['core']['id'] = ""

        expected = json.loads('{ "edges": [], "metadata": { "core": { "analyst_email": "user@email.address", "analyst_name": "A User", "created":"", "edited":"", "id":"", "version": "0.2" } }, "nodes": [], "resources": []}')
        self.assertEqual(out, expected)

    def test_init_with_config(self):
        """
        Tests: sadface.init() 
        
        Uses a user specified configuration that is different to the default
        """
        sf.config.set_config_location("deploy/etc/simon.cfg")
        sf.config.load()
        out = sf.init()
        out['metadata']['core']['created'] = ""
        out['metadata']['core']['edited'] = ""
        out['metadata']['core']['id'] = ""
        expected = json.loads('{ "edges": [], "metadata": { "core": { "analyst_email": "siwells@gmail.com", "analyst_name": "Simon Wells", "created": "", "edited": "", "id": "", "version": "0.2" } }, "nodes": [], "resources": []}')
        self.assertEqual(out, expected)


    def test_get_version(self):
        """
        Tests: sadface.get_version()
        """
        sf.sd = sf.init()
        out = sf.get_version();
        expected = "0.2"
        self.assertEqual(out, expected)

if __name__ == "__main__":
    
    unittest.main()
