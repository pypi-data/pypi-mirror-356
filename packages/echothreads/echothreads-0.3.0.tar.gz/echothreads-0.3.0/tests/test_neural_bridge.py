import unittest
from echoshell.neural_bridge import NeuralBridge
from echoshell.redis_connector import RedisConnector

class TestNeuralBridge(unittest.TestCase):
    def setUp(self):
        self.redis = RedisConnector()
        self.bridge = NeuralBridge(self.redis)

    def test_offline_publish_subscribe(self):
        received = {}
        def handler(msg):
            received.update(msg)
        self.bridge.subscribe('channel:agent:handoff', handler)
        self.bridge.publish_handoff({'id': 'test', 'task': 'demo'})
        self.assertEqual(received.get('id'), 'test')

if __name__ == '__main__':
    unittest.main()
