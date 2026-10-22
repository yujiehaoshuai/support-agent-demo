import tempfile
import unittest
from pathlib import Path
import support

class SupportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = support.DB
        support.DB = Path(self.tmp.name) / 'test.db'
        support.init_db()
    def tearDown(self):
        support.DB = self.old
        self.tmp.cleanup()
    def test_owner_isolation(self):
        self.assertIn('error', support.lookup_order('A1002'))
        self.assertIn('error', support.create_ticket('A1002', '退货'))
    def test_injection(self):
        self.assertIn('error', support.lookup_order("' OR 1=1 --"))
    def test_idempotency(self):
        self.assertEqual(support.create_ticket('A1001', '退货'), support.create_ticket('A1001', '退货'))
    def test_unknown_policy(self):
        self.assertFalse(support.search_policy('发票')['found'])
    def test_demo(self):
        self.assertEqual(support.demo_answer('A1001退货')[0]['result']['status'], '已签收')
    def test_reason(self):
        self.assertIn('error', support.create_ticket('A1001', ''))

if __name__ == '__main__':
    unittest.main()
