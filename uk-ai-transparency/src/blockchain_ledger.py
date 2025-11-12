import hashlib
import datetime
import json


class UKTransparencyBlockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0', 
                         decision_data="Genesis block - UK AI Transparency Framework")

    def create_block(self, proof, previous_hash, decision_data):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'decision_data': decision_data
        }
        # Calculate hash AFTER creating the block
        block['hash'] = self.hash_block(block)
        self.chain.append(block)
        return block

    def hash_block(self, block):
        # Create copy to avoid modifying original
        block_copy = block.copy()
        if 'hash' in block_copy:
            del block_copy['hash']
        encoded_block = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def add_decision(self, decision_text, algorithm_used, department="UK-Gov", citizen_impact="medium"):
        previous_block = self.chain[-1]
        new_block_data = {
            'decision': decision_text,
            'algorithm': algorithm_used,
            'department': department,
            'citizen_impact': citizen_impact,
            'timestamp': str(datetime.datetime.now())
        }
        return self.create_block(
            proof=previous_block['proof'] + 1,
            previous_hash=previous_block['hash'],
            decision_data=new_block_data
        )

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Verify current hash
            if current_block['hash'] != self.hash_block(current_block):
                return False
            
            # Verify link to previous block
            if current_block['previous_hash'] != previous_block['hash']:
                return False
                
        return True

    def print_chain(self):
        for block in self.chain:
            print(f"🔗 Block #{block['index']}")
            print(f"   Timestamp: {block['timestamp']}")
            print(f"   Data: {block['decision_data']}")
            print(f"   Previous Hash: {block['previous_hash'][:20]}...")
            print(f"   Hash: {block['hash'][:20]}...")
            print("   " + "="*50)

# Example usage for testing
if __name__ == "__main__":
    print("🚀 Initializing UK AI Transparency Blockchain...")
    
    # Create blockchain
    uk_blockchain = UKTransparencyBlockchain()
    
    # Add some example decisions
    decisions = [
        ("Approved housing benefit for citizen 12345", "eligibility-ai-v2", "DWP", "high"),
        ("Denied planning permission for construction", "planning-algorithm", "Local-Gov", "medium"),
        ("Recommended medical treatment pathway", "nhs-triage-ai", "NHS", "high")
    ]
    
    for decision in decisions:
        uk_blockchain.add_decision(*decision)
    
    # Display the chain
    uk_blockchain.print_chain()
    
    # Validate integrity
    print(f"✅ Chain valid: {uk_blockchain.validate_chain()}")
    print(f"📊 Total blocks: {len(uk_blockchain.chain)}")
