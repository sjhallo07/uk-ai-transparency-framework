from pathlib import Path
import sys
import pprint

# add package root so we can import `src`
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.blockchain_ledger import UKTransparencyBlockchain
from src.nlp_explainer import NLPExplainer


def main():
    ledger_path = ROOT / "data" / "example_ledger.csv"
    lb = UKTransparencyBlockchain()
    print("Appending two records to ledger...")
    lb.add_decision("approve", "example-algorithm", "Example-Dept", "low")
    lb.add_decision("decline", "example-algorithm", "Example-Dept", "low")
    ok = lb.validate_chain()
    print("Ledger ok:", ok)

    text = "Applicant flagged for possible fraud and missing documents"
    print("Explanation for text:")
    explainer = NLPExplainer()
    pprint.pprint(explainer.explain_decision(text))


if __name__ == "__main__":
    main()
