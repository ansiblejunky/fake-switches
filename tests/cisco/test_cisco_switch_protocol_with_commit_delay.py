from time import time
import unittest

from flexmock import flexmock_teardown
from hamcrest import assert_that
from hamcrest import greater_than

from tests.util.global_reactor import cisco_privileged_password, cisco_switch_ssh_with_commit_delay_port, COMMIT_DELAY
from tests.util.global_reactor import cisco_switch_ip
from tests.util.protocol_util import SshTester, with_protocol


class TestCiscoSwitchProtocolWithCommitDelay(unittest.TestCase):

    def create_client(self):
        return SshTester("ssh", cisco_switch_ip, cisco_switch_ssh_with_commit_delay_port, 'root', 'root')

    def setUp(self):
        self.protocol = self.create_client()

    def tearDown(self):
        flexmock_teardown()

    @with_protocol
    def test_write_memory_with_commit_delay(self, t):
        t.child.timeout = 10
        enable(t)
        start_time = time()
        t.write("write memory")
        t.readln("Building configuration...")
        t.readln("OK")
        t.read("my_switch#")
        end_time = time()

        assert_that((end_time - start_time), greater_than(COMMIT_DELAY))


def enable(t):
    t.write("enable")
    t.read("Password: ")
    t.write_invisible(cisco_privileged_password)
    t.read("my_switch#")
