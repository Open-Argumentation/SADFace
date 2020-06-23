import json
import os
import unittest

import sadface as sf


class TestInitWithConfig(unittest.TestCase):
    def setUp(self):
        sf.reset()

    def tearDown(self):
        sf.reset()
    
    def test_init_with_config(self):
        """
        Tests: sadface.init() 
        
        Uses a user specified configuration that is different to the default
        """
        sf.config.set_location("etc/test.cfg")
        sf.config.load()
        sf.init()
        out = sf.sd
        out['metadata']['core']['created'] = ""
        out['metadata']['core']['edited'] = ""
        out['metadata']['core']['id'] = ""
        expected = json.loads('{ "edges": [], "metadata": { "core": { "analyst_email": "siwells@gmail.com", "analyst_name": "Simon Wells", "created": "", "edited": "", "id": "", "version": "0.2" } }, "nodes": [], "resources": []}')
        self.assertEqual(out, expected)


class TestInit(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_init(self):
        """
        Tests: sadface.init()
        """
        sf.init()
        out = sf.sd
        out['metadata']['core']['created'] = ""
        out['metadata']['core']['edited'] = ""
        out['metadata']['core']['id'] = ""

        expected = json.loads('{ "edges": [], "metadata": { "core": { "analyst_email": "user@email.address", "analyst_name": "A User", "created":"", "edited":"", "id":"", "version": "0.2" } }, "nodes": [], "resources": []}')
        self.assertEqual(out, expected)
        


if __name__ == "__main__":
    
    unittest.main()
