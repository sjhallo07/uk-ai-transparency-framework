import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import csv
from blockchain_ledger import UKTransparencyBlockchain
from nlp_explainer import NLPExplainer

# Path to your CSV file
csv_path = "uk-ai-transparency/data/sample_uk_decisions.csv"

blockchain = UKTransparencyBlockchain()
explainer = NLPExplainer()

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader, 1):
        # Add to blockchain
        block = blockchain.add_decision(
            decision_text=row['decision_text'],
            algorithm_used=row['algorithm_used'],
            department=row['department'],
            citizen_impact=row['impact_level']
        )
        # Prepare for NLP explainer
        decision_data = {
            'decision': row['decision_text'],
            'algorithm': row['algorithm_used'],
            'department': row['department']
        }
        explanation = explainer.explain_decision(decision_data)
        print(f"\n🔗 Block #{block['index']}")
        print(f"   Data: {block['decision_data']}")
        print(f"   Hash: {block['hash'][:20]}...")
        print(f"   NLP Explanation: {explanation['explanation']}")
        print(f"   Factors: {', '.join(explanation['factors_considered'])}")
        print("-" * 60)

# Validate blockchain
print(f"\n✅ Blockchain valid: {blockchain.validate_chain()}")
print(f"📊 Total blocks: {len(blockchain.chain)}")
