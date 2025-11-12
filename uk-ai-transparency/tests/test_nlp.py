import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from src.nlp_explainer import NLPExplainer

explain_text_decision = NLPExplainer().explain_text_decision


def test_keywords_found():
    text = "Applicant flagged for fraud and missing documents"
    res = explain_text_decision(text)
    keys = {r["keyword"] for r in res}
    assert "fraud" in keys and "missing" in keys


def test_no_keywords_fallback():
    text = "A short benign note with no key terms"
    res = explain_text_decision(text)
    assert isinstance(res, list)
    assert res[0]["keyword"] == "none"
