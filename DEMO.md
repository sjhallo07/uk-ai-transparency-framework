# 🇬🇧 UK AI Transparency Dashboard Demo

This page demonstrates the main features of the UK AI Transparency Framework dashboard, designed for government AI decision transparency using blockchain and NLP.

---

## 🚦 Quick Start Demo

### 1. Launch the Dashboard

```bash
# Activate your Python 3.11+ virtual environment (example for Windows PowerShell)
.venv311\Scripts\Activate.ps1

# Run the Streamlit dashboard
streamlit run uk-ai-transparency/src/transparency_dashboard.py
```

- The dashboard will open in your browser at `http://localhost:8501` by default.

### 2. Dashboard Features

- **Blockchain Ledger Tab**: View the immutable chain of AI decisions, each with cryptographic hashes and timestamps.
- **NLP Explainer Tab**: See human-readable explanations for each automated decision, powered by NLP.
- **Data Visualizations**: Explore UK government sample data with interactive charts and tables.

---

## 🖼️ Demo Screenshots

> _Replace these with real screenshots for production_

- ![Dashboard Home](uk-ai-transparency/docs/dashboard_home_placeholder.png)
- ![Blockchain Tab](uk-ai-transparency/docs/blockchain_tab_placeholder.png)
- ![NLP Explainer Tab](uk-ai-transparency/docs/nlp_tab_placeholder.png)

---

## 📝 Example Output

- **Blockchain Block Example:**
  ```json
  {
    "index": 2,
    "timestamp": "2025-11-12 10:15:00",
    "data": "AI decision: NHS patient triage",
    "previous_hash": "...",
    "hash": "..."
  }
  ```
- **NLP Explanation Example:**
  ```json
  {
    "decision": "NHS patient triage",
    "explanation": "The AI system prioritized this patient based on urgency and symptoms."
  }
  ```

---

## 📚 More Information

- [Project README](uk-ai-transparency/README.md)
- [Sample Data](uk-ai-transparency/data/sample_uk_decisions.csv)
- [Source Code](uk-ai-transparency/src/)

---

© 2025 sjhallo07. For research and demonstration purposes only.
