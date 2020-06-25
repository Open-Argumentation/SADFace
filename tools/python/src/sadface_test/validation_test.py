import configparser
import json
import os
import unittest

import sadface as sf

class TestVerification(unittest.TestCase):
    def setUp(self):
        sf.reset()

    def tearDown(self):
        sf.reset()

    def test_verify(self):
        """
        TESTS: sadface.validation.verify()
        """
        pass

        minimal_good = {'edges':[],'metadata':{'core':{'analyst_email':'user@email.address','analyst_name':'A User','created':'2020-06-25T18:05:36','edited':'2020-06-25T18:05:36','id':'235bfdee-2406-4c40-97cc-6f4c2539c69e','version':'0.2'}},'nodes':[],'resources':[]}

        result, problems = sf.validation.verify(minimal_good)
        self.assertEqual(False, result)
        self.assertEqual([], problems)
        
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
        """


if __name__ == "__main__":
    
    unittest.main()
