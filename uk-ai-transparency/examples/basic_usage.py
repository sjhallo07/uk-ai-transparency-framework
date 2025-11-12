from pathlib import Path
import sys
import pprint

# add package root so we can import `src`
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.blockchain_ledger import BlockchainLedger
from src.nlp_explainer import NLPExplainer


def main():
    ledger_path = ROOT / "data" / "example_ledger.csv"
    lb = BlockchainLedger(str(ledger_path))
    print("Appending two records to ledger...")
    lb.append_record({"applicant": "Alice", "decision": "approve"})
    lb.append_record({"applicant": "Bob", "decision": "decline", "note": "Missing documents"})
    ok, bad = lb.verify_integrity()
    print("Ledger ok:", ok, "first_bad:", bad)

    text = "Applicant flagged for possible fraud and missing documents"
    print("Explanation for text:")
    explainer = NLPExplainer()
    pprint.pprint(explainer.explain(text))


if __name__ == "__main__":
    main()
