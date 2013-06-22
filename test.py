import time
import unittest

import config as test_config
from bunshin import config

# monkey patch, should be refactored!
config.AWS_ACCESS_KEY = test_config.AWS_ACCESS_KEY
config.AWS_SECRET_KEY = test_config.AWS_SECRET_KEY
config.SALT_MASTER = test_config.SALT_MASTER
config.SALT_MASTER_USER = test_config.SALT_MASTER_USER

from bunshin import utils
from bunshin.instance import InstanceType


class TestInstanceType(unittest.TestCase):

    def setUp(self):
        self.search_instance = InstanceType(**config.EC2_INSTANCES['search'])

    def tearDown(self):
        self.search_instance.terminate()

    def test_launching(self):
        self.assertEqual(self.search_instance.instances, [])
        self.search_instance.launch()
        self.assertNotEqual(self.search_instance.instances, [])

        self.assertEqual(self.search_instance.states[0], 'pending')
        time.sleep(30)
        self.assertEqual(self.search_instance.states[0], 'running')


class TestInstancePrep(unittest.TestCase):

    def setUp(self):
        self.search_instance = InstanceType(**test_config.EC2_INSTANCES['search'])

    def tearDown(self):
        self.search_instance.terminate()

    def test_install_saltstack(self):
        self.search_instance.launch()
        utils.join_instance(self.search_instance.instances[0])


if __name__ == '__main__':
    unittest.main()
