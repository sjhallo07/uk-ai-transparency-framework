import sys
from pathlib import Path
import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from src.nlp_explainer import NLPExplainer

def test_keywords_found():
    decision = {
        'decision': "Applicant flagged for fraud and missing documents",
        'algorithm': 'fraud-detection',
        'department': 'HMRC'
    }
    res = NLPExplainer().explain_decision(decision)
    # Check that explanation and factors are as expected
    assert 'flagged for review' in res['explanation']
    assert 'fraud' in decision['decision'].lower() or 'missing' in decision['decision'].lower()
    assert isinstance(res['factors_considered'], list)


def test_no_keywords_fallback():
    decision = {
        'decision': "A short benign note with no key terms",
        'algorithm': 'default',
        'department': 'TestDept'
    }
    res = NLPExplainer().explain_decision(decision)
    assert isinstance(res, dict)
    assert res['factors_considered'] == ['multiple established criteria']
