import csv
from nlp_explainer import NLPExplainer

# Path to your CSV file
csv_path = "uk-ai-transparency/data/sample_uk_decisions.csv"

explainer = NLPExplainer()

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader, 1):
        # Prepare the input for NLPExplainer
        decision_data = {
            'decision': row['decision_text'],
            'algorithm': row['algorithm_used'],
            'department': row['department']
        }
        explanation = explainer.explain_decision(decision_data)
        print(f"\n📋 Decision {i}: {explanation['original_decision']}")
        print(f"   🤖 Algorithm: {explanation['algorithm']}")
        print(f"   🏛️ Department: {explanation['department']}")
        print(f"   📝 Explanation: {explanation['explanation']}")
        print(f"   🔍 Factors: {', '.join(explanation['factors_considered'])}")
        print("-" * 60)
