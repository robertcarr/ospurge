import unittest
import re

import ospurge

from ospurge import Session


cfg = {'endpoint': 'https://keystone:35357/v3', 'username': 'admin', 'password': 'admin123',
       'user_domain_name': 'default', 'project': 'admin', 'insecure': True }

class TestStuff(unittest.TestCase):
    def setUp(self):
        pass
       # self.session =  Session('admin','admin123', 'admin', 'https://keystone:35357/v3', True,
       #              domain_name='default', user_domain_name='default')

    def test_get_endpoint(self):
        sess = Session(cfg['username'], cfg['password'], cfg['project'], cfg['endpoint'],
                       cfg['insecure'], user_domain_name=cfg['user_domain_name'])
        endpoint=sess.get_endpoint('identity')
        self.assertTrue("http" in endpoint)

    def test_Nova(self):
        self.session = Session('admin', 'admin123', 'admin', 'https://keystone:35357/v3', True,
            user_domain_name='default', project_domain_name='default')
        nova = ospurge.nova_client.Client(session=self.session.session)
        self.assertIsInstance(nova.flavors.list(), list )

    def test_Ceilometer(self):
        sess = Session('admin', 'admin123', 'admin', 'https://keystone:35357/v3', True,
            user_domain_name='default', project_domain_name='default')
        c = ospurge.ceilometer_client.get_client('2', os_username=sess.username, os_password=sess.password, os_tenant_name=sess.project_domain_name,
                        user_domain_name=sess.user_domain_name, os_auth_url=sess.auth_url)
        self.assertIsInstance(c.meters.list(), list)

    def test_Heat(self):
        sess = Session('admin', 'admin123', 'admin', 'https://keystone:35357/v3', True,
            project_domain_name='default', project_name='admin', user_domain_name='default')
        heat = ospurge.heat_client.Client('1', token=sess.token, endpoint=sess.get_endpoint('orchestration'))
        stacks = heat.stacks.list()
        self.assertTrue(list(stacks))

    def test_Neutron(self):
        sess = Session(cfg['username'], cfg['password'], cfg['project'], cfg['endpoint'],
                       cfg['insecure'], user_domain_name=cfg['user_domain_name'])
        neutron = ospurge.neutron_client.Client('2.0', session=sess.session)
        nets = neutron.list_networks()['networks']
        self.assertIsInstance(nets, list)

    def test_cinder(self):
        sess = Session(cfg['username'], cfg['password'], cfg['project'], cfg['endpoint'],
                       cfg['insecure'], user_domain_name=cfg['user_domain_name'])
        cinder = ospurge.cinder_client.Client('2', session=sess.session)
        self.assertIsInstance(cinder.volumes.list(), list)

    def test_glance(self):
        sess = Session(cfg['username'], cfg['password'], cfg['project'], cfg['endpoint'],
                       cfg['insecure'], user_domain_name=cfg['user_domain_name'])
        glance = ospurge.glance_client.Client('1', session=sess.session)
        self.assertIsInstance(glance.images.list(), list)
        
if __name__ == '__main__':
    unittest.main()
