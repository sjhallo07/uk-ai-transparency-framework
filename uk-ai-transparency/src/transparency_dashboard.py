import streamlit as st
import pandas as pd
import json
from blockchain_ledger import UKTransparencyBlockchain
from nlp_explainer import NLPExplainer
import plotly.express as px
from flask import Flask, abort, jsonify  # Added import for Flask, abort and jsonify
from pathlib import Path

app = Flask(__name__)

class TransparencyDashboard:
    def __init__(self):
        self.blockchain = UKTransparencyBlockchain()
        self.load_sample_data()
    
    def load_sample_data(self):
        # Load example decisions
        try:
            df = pd.read_csv('../data/sample_uk_decisions.csv')
            for _, row in df.iterrows():
                self.blockchain.add_decision(
                    decision_text=row['decision_text'],
                    algorithm_used=row['algorithm_used'],
                    department=row['department'],
                    citizen_impact=row['impact_level']
                )
            st.success("✅ Sample data loaded successfully")
        except Exception as e:
            st.warning(f"⚠️ Could not load sample data: {e}")


        class TransparencyDashboard:
            def __init__(self):
                self.blockchain = UKTransparencyBlockchain()
                self.explainer = NLPExplainer()
                # Load sample data only if ledger contains only the genesis block
                if len(self.blockchain.chain) <= 1:
                    self.load_sample_data()

            def load_sample_data(self):
                data_file = Path(__file__).resolve().parent.parent / "data" / "sample_uk_decisions.csv"
                if not data_file.exists():
                    st.warning(f"Sample data not found at {data_file}")
                    return
                try:
                    df = pd.read_csv(data_file)
                    for _, row in df.iterrows():
                        # Be tolerant of column name differences
                        decision_text = row.get('decision_text') or row.get('decision')
                        algorithm_used = row.get('algorithm_used') or row.get('algorithm')
                        department = row.get('department')
                        impact = row.get('impact_level') or row.get('citizen_impact')
                        self.blockchain.add_decision(
                            decision_text=str(decision_text),
                            algorithm_used=str(algorithm_used),
                            department=str(department),
                            citizen_impact=str(impact)
                        )
                    st.success("✅ Sample data loaded successfully")
                except Exception as e:
                    st.warning(f"⚠️ Could not load sample data: {e}")

            def run(self):
                st.set_page_config(page_title="UK AI Transparency Framework", page_icon="🔍", layout="wide")
                st.title("🔍 UK AI Transparency Framework")
                st.markdown("**Immutable registry system for UK government automated decisions**")

                # Sidebar
                st.sidebar.header("⚙️ Configuration")
                if st.sidebar.button("🔄 Reset Blockchain"):
                    self.blockchain = UKTransparencyBlockchain()
                    st.experimental_rerun()

                # Main tabs
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔗 Blockchain", "🧠 Explanations", "➕ New Decision"])

                with tab1:
                    self.show_dashboard()
                with tab2:
                    self.show_blockchain()
                with tab3:
                    self.show_explanations()
                with tab4:
                    self.show_decision_form()

            def show_dashboard(self):
                st.header("📊 System Overview")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total Blocks", len(self.blockchain.chain))
                with col2:
                    valid = self.blockchain.validate_chain()
                    st.metric("Blockchain Integrity", "✅ Valid" if valid else "❒ Compromised")
                with col3:
                    departments = len({
                        block['decision_data'].get('department')
                        for block in self.blockchain.chain
                        if isinstance(block.get('decision_data'), dict)
                    })
                    st.metric("Departments", departments)
                with col4:
                    algorithms = len({
                        block['decision_data'].get('algorithm')
                        for block in self.blockchain.chain
                        if isinstance(block.get('decision_data'), dict)
                    })
                    st.metric("Algorithms", algorithms)

                # Charts
                c1, c2 = st.columns(2)
                with c1:
                    self.show_department_chart()
                with c2:
                    self.show_impact_chart()

            def show_department_chart(self):
                departments = [
                    block['decision_data'].get('department', 'Unknown')
                    for block in self.blockchain.chain
                    if isinstance(block.get('decision_data'), dict)
                ]
                if departments:
                    dept_counts = pd.Series(departments).value_counts()
                    fig = px.pie(values=dept_counts.values, names=dept_counts.index, title="📊 Decisions by Department")
                    st.plotly_chart(fig, use_container_width=True)

            def show_impact_chart(self):
                impacts = [
                    block['decision_data'].get('citizen_impact', 'unknown')
                    for block in self.blockchain.chain
                    if isinstance(block.get('decision_data'), dict)
                ]
                if impacts:
                    impact_counts = pd.Series(impacts).value_counts()
                    fig = px.bar(x=impact_counts.index, y=impact_counts.values, title="🎯 Citizen Impact Level",
                                 labels={'x': 'Impact Level', 'y': 'Number of Decisions'})
                    st.plotly_chart(fig, use_container_width=True)

            def show_blockchain(self):
                st.header("🔗 Complete Blockchain")
                for block in self.blockchain.chain:
                    with st.expander(f"Block #{block['index']} - {block['timestamp']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Block Metadata:**")
                            st.write(f"📅 Timestamp: {block['timestamp']}")
                            st.write(f"🔢 Proof: {block.get('proof')}")
                            prev = block.get('previous_hash', '')
                            st.write(f"🔗 Previous Hash: `{prev[:20]}...`")
                            st.write(f"🆔 Current Hash: `{block.get('hash')[:20]}...`")
                        with col2:
                            st.write("**Decision Data:**")
                            data = block.get('decision_data')
                            if isinstance(data, dict):
                                for key, value in data.items():
                                    st.write(f"**{key}:** {value}")
                            else:
                                st.write(f"**Data:** {data}")

            def show_explanations(self):
                st.header("🧠 NLP Explanations")
                for block in self.blockchain.chain:
                    data = block.get('decision_data')
                    if isinstance(data, dict):
                        explanation = self.explainer.explain_decision(data)
                        decision_text = data.get('decision') or data.get('decision_text') or str(data)
                        with st.expander(f"🔍 {decision_text}"):
                            st.write(f"**🤖 Algorithm:** {data.get('algorithm')}")
                            st.write(f"**🏛️ Department:** {data.get('department')}")
                            st.info(f"**📝 Explanation:** {explanation.get('explanation')}")
                            factors = explanation.get('factors_considered', [])
                            if not isinstance(factors, list):
                                factors = [str(factors)] if factors else []
                            st.write(f"**🔍 Factors considered:** {', '.join(map(str, factors))}")
                            st.write(f"**🕐 Explanation date:** {explanation.get('explanation_timestamp')}")

            def show_decision_form(self):
                st.header("➕ Register New Decision")
                with st.form("new_decision_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        department = st.selectbox("Department", ["NHS", "DWP", "HMRC", "Local-Gov", "UK-Border", "Environment-Agency"])
                        algorithm = st.text_input("Algorithm used", "risk-assessment-v1")
                    with col2:
                        impact = st.selectbox("Citizen impact", ["low", "medium", "high"])
                        decision_text = st.text_area("Decision text", "Approved application based on automated assessment")
                    submitted = st.form_submit_button("✅ Register in Blockchain")
                    if submitted:
                        if decision_text.strip():
                            new_block = self.blockchain.add_decision(decision_text=decision_text, algorithm_used=algorithm, department=department, citizen_impact=impact)
                            st.success(f"✅ Decision registered in block #{new_block['index']}")
                            st.experimental_rerun()
                        else:
                            st.error("❌ Please enter valid decision text")


        if __name__ == "__main__":
            dashboard = TransparencyDashboard()
            dashboard.run()
@app.route("/decisions/<int:decision_id>")
def get_decision(decision_id):
    # Load the decisions data (replace the path as needed)
    try:
        df = pd.read_csv('../data/sample_uk_decisions.csv')
    except Exception:
        abort(404)
    if df.empty:
        abort(404)
    row = df[df["id"] == decision_id]
    if row.empty:
        abort(404)
    r = row.iloc[0].to_dict()
    explainer = NLPExplainer()
    explanation = explainer.explain_decision(r)
    r["explanation"] = explanation.get("explanation", "")
    return jsonify(r)


def main():
    """Start the Flask transparency dashboard app.

    This function is suitable for use as a console_scripts entry point:
    `uk-ai-dashboard=src.transparency_dashboard:main`.
    """
    # When running from the package entrypoint, ensure any relative data paths remain valid.
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    # When running from the src/ folder make sure PYTHONPATH includes src/ or run with `python -m src.transparency_dashboard`.
    main()
