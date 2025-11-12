import re
from datetime import datetime


class NLPExplainer:
    def __init__(self):
        self.explanation_templates = {
            "risk-assessment": [
                "The system analyzed multiple risk factors and {action} based on the identified profile.",
                "The risk assessment considered key variables and determined that {action} was the appropriate course."
            ],
            "eligibility-check": [
                "After verifying eligibility criteria, the system {action} the application.",
                "The automated validation {action} the request after confirming requirements."
            ],
            "fraud-detection": [
                "The algorithm detected anomalous patterns and {action} for further investigation.",
                "Based on behavior analysis, the system {action} this transaction."
            ],
            "default": [
                "The system processed the information and {action} according to established parameters.",
                "The automated decision {action} after complete analysis."
            ]
        }

    def explain_decision(self, decision_data):
        algorithm = decision_data.get('algorithm', '').lower()
        decision_text = decision_data.get('decision', '').lower()
        department = decision_data.get('department', '')

        # Determine algorithm type
        algo_type = self._Classify_algorithm(algorithm)

        # Determine action
        action = self._extract_action(decision_text)

        # Select template
        template = self.explanation_templates.get(algo_type, self.explanation_templates["default"])[0]

        explanation = template.format(action=action)

        return {
            'original_decision': decision_data.get('decision'),
            'algorithm': algorithm,
            'department': department,
            'explanation': explanation,
            'explanation_timestamp': str(datetime.now()),
            'factors_considered': self._extract_factors(decision_text)
        }

    def _Classify_algorithm(self, algorithm):
        algorithm = algorithm.lower()
        if 'risk' in algorithm:
            return 'risk-assessment'
        elif 'eligibility' in algorithm:
            return 'eligibility-check'
        elif 'fraud' in algorithm:
            return 'fraud-detection'
        else:
            return 'default'

    def _extract_action(self, decision_text):
        text = decision_text.lower()
        if any(word in text for word in ['approved', 'approve', 'granted']):
            return 'approved the request'
        elif any(word in text for word in ['denied', 'deny', 'rejected']):
            return 'denied the request'
        elif any(word in text for word in ['flagged', 'flag', 'detected']):
            return 'flagged for review'
        elif any(word in text for word in ['recommended', 'suggested']):
            return 'recommended proceeding'
        else:
            return 'processed the information'

    def _extract_factors(self, decision_text):
        factors = []
        text = decision_text.lower()

        if any(word in text for word in ['benefit', 'payment']):
            factors.append('economic criteria')
        if any(word in text for word in ['medical', 'treatment', 'health']):
            factors.append('health conditions')
        if any(word in text for word in ['risk', 'security']):
            factors.append('security assessment')
        if any(word in text for word in ['priority', 'urgency']):
            factors.append('urgency level')

        return factors if factors else ['multiple established criteria']

# Test the module
if __name__ == "__main__":
    explainer = NLPExplainer()

    test_decisions = [
        {'decision': 'Approved housing benefit for citizen 12345', 'algorithm': 'eligibility-check', 'department': 'DWP'},
        {'decision': 'Flagged potential fraud in tax return', 'algorithm': 'fraud-detection', 'department': 'HMRC'},
        {'decision': 'Recommended high priority medical treatment', 'algorithm': 'risk-assessment', 'department': 'NHS'}
    ]

    print("🧠 Testing NLP Explanation Module:")
    print("=" * 60)

    for i, decision in enumerate(test_decisions, 1):
        explanation = explainer.explain_decision(decision)
        print(f"📋 Decision {i}: {explanation['original_decision']}")
        print(f"   🤖 Algorithm: {explanation['algorithm']}")
        print(f"   🏛️ Department: {explanation['department']}")
        print(f"   📝 Explanation: {explanation['explanation']}")
        print(f"   🔍 Factors: {', '.join(explanation['factors_considered'])}")
        print("-" * 60)
