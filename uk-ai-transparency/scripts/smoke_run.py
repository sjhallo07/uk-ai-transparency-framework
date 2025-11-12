import sys
from pathlib import Path

# Ensure src folder is on path
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
sys.path.insert(0, str(SRC))

from blockchain_ledger import UKTransparencyBlockchain
from nlp_explainer import NLPExplainer

print('Initializing blockchain and explainer...')
blk = UKTransparencyBlockchain()
print('Initial blocks:', len(blk.chain))
new = blk.add_decision('Approved housing benefit for citizen 12345', 'eligibility-check', 'DWP', 'high')
print('Added block index:', new['index'])
print('Total blocks now:', len(blk.chain))

exp = NLPExplainer()
result = exp.explain_decision(blk.chain[-1]['decision_data'])
print('Explanation:', result)
