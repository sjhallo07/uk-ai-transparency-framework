import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from blockchain_ledger import UKTransparencyBlockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        # use a temporary ledger file in the tests directory to avoid repo state changes
        ledger_path = os.path.join(os.path.dirname(__file__), 'test_ledger.csv')
        # remove existing test ledger if present
        try:
            os.remove(ledger_path)
        except Exception:
            pass
        self.blockchain = UKTransparencyBlockchain(ledger_path)
    
    def test_chain_initialization(self):
        """Test blockchain initializes with genesis block"""
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0]['previous_hash'], '0')
    
    def test_add_decision(self):
        """Test adding decisions to blockchain"""
        initial_length = len(self.blockchain.chain)
        self.blockchain.add_decision(
            "Test decision", 
            "test-algorithm", 
            "Test-Dept"
        )
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)
    
    def test_chain_validation(self):
        """Test blockchain integrity validation"""
        self.assertTrue(self.blockchain.validate_chain())
    
    def test_block_hashing(self):
        """Test block hashing consistency"""
        block = self.blockchain.chain[0]
        expected_hash = self.blockchain.hash_block(block)
        self.assertEqual(block['hash'], expected_hash)

if __name__ == '__main__':
    unittest.main()
