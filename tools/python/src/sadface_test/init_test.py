import configparser
import json
import os
import unittest

import sadface as sf


class TestInitWithConfig(unittest.TestCase):
    def setUp(self):
        sf.reset()

    def tearDown(self):
        sf.reset()

    def test_config_load(self):
        """
        TESTS: sadface.config.load()
        """

        # No specified configuration file. location is None
        with self.assertRaises(Exception) as context:
            sf.config.load()
            
        self.assertTrue("Tried to load config file but location is set to None" in str(context.exception))

        # With bad configuration file
        sf.config.set_location("src/sadface/aml.py")
        with self.assertRaises(SystemExit):
            sf.config.load()
        
        # With good configuration file
        sf.config.set_location("etc/test.cfg")
        sf.config.load()
        sf.init()
        out = sf.sd
        out['metadata']['core']['created'] = ""
        out['metadata']['core']['edited'] = ""
        out['metadata']['core']['id'] = ""
        expected = json.loads('{ "edges": [], "metadata": { "core": { "analyst_email": "you-killed-my-father@prepare-to-die.com", "analyst_name": "Inigo Montoya", "created": "", "edited": "", "id": "", "version": "0.2" } }, "nodes": [], "resources": []}')
        self.assertEqual(out, expected)


    def test_config_reset(self):
        """
        TESTS: sadface.config.reset()
        """
        current = None
        location = None

        sf.config.reset()
        self.assertEqual(current, sf.config.current)
        self.assertEqual(location, sf.config.location)
        

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
        expected = json.loads('{ "edges": [], "metadata": { "core": { "analyst_email": "you-killed-my-father@prepare-to-die.com", "analyst_name": "Inigo Montoya", "created": "", "edited": "", "id": "", "version": "0.2" } }, "nodes": [], "resources": []}')
        self.assertEqual(out, expected)

    def test_combined_config_init_method(self):
        """

        """
        sf.config.init("etc/test.cfg")
        sf.init()
        out = sf.sd
        out['metadata']['core']['created'] = ""
        out['metadata']['core']['edited'] = ""
        out['metadata']['core']['id'] = ""
        expected = json.loads('{ "edges": [], "metadata": { "core": { "analyst_email": "you-killed-my-father@prepare-to-die.com", "analyst_name": "Inigo Montoya", "created": "", "edited": "", "id": "", "version": "0.2" } }, "nodes": [], "resources": []}')
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
