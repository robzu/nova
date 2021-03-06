# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012, Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Unit Tests for nova.consoleauth.rpcapi
"""

from nova.consoleauth import rpcapi as consoleauth_rpcapi
from nova import context
from nova import flags
from nova.openstack.common import rpc
from nova import test


FLAGS = flags.FLAGS


class ConsoleAuthRpcAPITestCase(test.TestCase):

    def setUp(self):
        super(ConsoleAuthRpcAPITestCase, self).setUp()

    def tearDown(self):
        super(ConsoleAuthRpcAPITestCase, self).tearDown()

    def _test_consoleauth_api(self, method, **kwargs):
        ctxt = context.RequestContext('fake_user', 'fake_project')
        rpcapi = consoleauth_rpcapi.ConsoleAuthAPI()
        expected_retval = 'foo'
        expected_msg = rpcapi.make_msg(method, **kwargs)
        expected_msg['version'] = rpcapi.RPC_API_VERSION

        self.call_ctxt = None
        self.call_topic = None
        self.call_msg = None
        self.call_timeout = None

        def _fake_call(_ctxt, _topic, _msg, _timeout):
            self.call_ctxt = _ctxt
            self.call_topic = _topic
            self.call_msg = _msg
            self.call_timeout = _timeout
            return expected_retval

        self.stubs.Set(rpc, 'call', _fake_call)

        retval = getattr(rpcapi, method)(ctxt, **kwargs)

        self.assertEqual(retval, expected_retval)
        self.assertEqual(self.call_ctxt, ctxt)
        self.assertEqual(self.call_topic, FLAGS.consoleauth_topic)
        self.assertEqual(self.call_msg, expected_msg)
        self.assertEqual(self.call_timeout, None)

    def test_authorize_console(self):
        self._test_consoleauth_api('authorize_console', token='token',
                console_type='ctype', host='h', port='p',
                internal_access_path='iap')

    def test_check_token(self):
        self._test_consoleauth_api('check_token', token='t')
