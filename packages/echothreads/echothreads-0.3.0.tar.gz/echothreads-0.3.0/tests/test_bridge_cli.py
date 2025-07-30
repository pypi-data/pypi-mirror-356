import unittest
from click.testing import CliRunner
from echoshell.cli import cli

class TestBridgeCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_publish_command(self):
        result = self.runner.invoke(cli, ['bridge', 'publish', 'channel:test', '{"foo":"bar"}'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Published to channel:test', result.output)

    def test_listen_command(self):
        # publish first so message is queued
        self.runner.invoke(cli, ['bridge', 'publish', 'channel:listen', '{"a":1}'])
        result = self.runner.invoke(cli, ['bridge', 'listen', 'channel:listen', '--timeout', '0.1'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('{"a": 1}', result.output)

    def test_register_and_list(self):
        reg = self.runner.invoke(cli, ['bridge', 'register', '{"id":"cap1"}'])
        self.assertEqual(reg.exit_code, 0)
        self.assertIn('Registered capability cap1', reg.output)
        list_out = self.runner.invoke(cli, ['bridge', 'list'])
        self.assertIn('cap1', list_out.output)

if __name__ == '__main__':
    unittest.main()
