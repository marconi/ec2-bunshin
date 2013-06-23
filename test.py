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
        self.app_instance = InstanceType(**config.EC2_INSTANCES['app'])

    def tearDown(self):
        self.app_instance.terminate()

    def test_launching(self):
        self.assertEqual(self.app_instance.instances, [])
        self.app_instance.launch()
        self.assertNotEqual(self.app_instance.instances, [])

        self.assertEqual(self.app_instance.states[0], 'pending')
        time.sleep(60)
        self.assertEqual(self.app_instance.states[0], 'running')


class TestInstancePrep(unittest.TestCase):

    def setUp(self):
        self.app_instance = InstanceType(**test_config.EC2_INSTANCES['app'])

    def tearDown(self):
        self.app_instance.terminate()

    def test_install_saltstack(self):
        self.app_instance.launch()

        self.assertEqual(self.app_instance.states[0], 'pending')
        time.sleep(60)
        self.assertEqual(self.app_instance.states[0], 'running')
        utils.join_instance(self.app_instance.instances[0])


class TestProxyUpdate(unittest.TestCase):

    def setUp(self):
        self.app_instance = InstanceType(**test_config.EC2_INSTANCES['app'])

    def tearDown(self):
        self.app_instance.terminate()

    def test_update_config(self):
        self.app_instance.launch()
        time.sleep(60)
        utils.join_instance(self.app_instance.instances[0])
        utils.update_proxy(self.app_instance.instances)


if __name__ == '__main__':
    unittest.main()
