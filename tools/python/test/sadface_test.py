import json
import os
import sadface as sf 
import unittest

class TestSADFaceFunctions(unittest.TestCase):
    def setUp(self):
       pass
    
    def test_init(self):
        out = sf.init()
        out['metadata']['core']['created'] = ""
        out['metadata']['core']['edited'] = ""
        out['metadata']['core']['id'] = ""

        expected = json.loads('{ "edges": [], "metadata": { "core": { "analyst_email": "user@email.address", "analyst_name": "A User", "created":"", "edited":"", "id":"", "version": "0.2" } }, "nodes": [], "resources": []}')
        self.assertEqual(out, expected)

    def test_init_with_config(self):
        sf.config.set_config_location("deploy/etc/simon.cfg")
        sf.config.load()
        out = sf.init()
        out['metadata']['core']['created'] = ""
        out['metadata']['core']['edited'] = ""
        out['metadata']['core']['id'] = ""
        expected = json.loads('{ "edges": [], "metadata": { "core": { "analyst_email": "siwells@gmail.com", "analyst_name": "Simon Wells", "created": "", "edited": "", "id": "", "version": "0.2" } }, "nodes": [], "resources": []}')
        self.assertEqual(out, expected)


    def test_get_version(self):
        sf.sd = sf.init()
        out = sf.get_version();
        expected = "0.2"
        self.assertEqual(out, expected)

if __name__ == "__main__":
    
    unittest.main()
