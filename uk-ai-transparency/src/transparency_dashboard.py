import streamlit as st
import pandas as pd
import json
import os
from blockchain_ledger import UKTransparencyBlockchain
from nlp_explainer import NLPExplainer
import plotly.express as px

class TransparencyDashboard:
    def __init__(self):
        self.blockchain = UKTransparencyBlockchain()
        self.explainer = NLPExplainer()
        self.load_sample_data()
    
    def load_sample_data(self):
        # Load sample decisions
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, '../data/sample_uk_decisions.csv')
            df = pd.read_csv(data_path)
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
    
    def run(self):
        st.set_page_config(
            page_title="UK AI Transparency Framework",
            page_icon="🔍",
            layout="wide"
        )
        
        st.image("https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg", width=60)
        st.title("UK AI Transparency Framework")
        st.markdown("**Immutable registry system for automated government decisions in the UK**")
        
        # Sidebar
        st.sidebar.header("⚙️ Settings")
        
        if st.sidebar.button("🔄 Reset Blockchain"):
            self.blockchain = UKTransparencyBlockchain()
            st.rerun()
        
        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Dashboard", 
            "🔗 Blockchain", 
            "🧠 Explanations", 
            "➕ New Decision"
        ])
        
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
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Blocks", len(self.blockchain.chain))
        
        with col2:
            valid = self.blockchain.validate_chain()
            st.metric("Blockchain Integrity", "✅ Valid" if valid else "❌ Compromised")
        
        with col3:
            departments = len(set(
                block['decision_data']['department'] 
                for block in self.blockchain.chain 
                if isinstance(block['decision_data'], dict)
            ))
            st.metric("Departments", departments)
        
        with col4:
            algorithms = len(set(
                block['decision_data']['algorithm'] 
                for block in self.blockchain.chain 
                if isinstance(block['decision_data'], dict)
            ))
            st.metric("Algorithms", algorithms)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            self.show_department_chart()
        
        with col2:
            self.show_impact_chart()
    
    def show_department_chart(self):
        departments = []
        for block in self.blockchain.chain:
            if isinstance(block['decision_data'], dict):
                dept = block['decision_data'].get('department', 'Unknown')
                departments.append(dept)
        
        if departments:
            dept_counts = pd.Series(departments).value_counts()
            fig = px.pie(
                values=dept_counts.values,
                names=dept_counts.index,
                title="📊 Decisions by Department"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def show_impact_chart(self):
        impacts = []
        for block in self.blockchain.chain:
            if isinstance(block['decision_data'], dict):
                impact = block['decision_data'].get('citizen_impact', 'unknown')
                impacts.append(impact)
        
        if impacts:
            impact_counts = pd.Series(impacts).value_counts()
            fig = px.bar(
                x=impact_counts.index,
                y=impact_counts.values,
                title="🎯 Citizen Impact Level",
                labels={'x': 'Impact Level', 'y': 'Number of Decisions'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def show_blockchain(self):
        st.header("🔗 Full Blockchain Chain")
        
        for i, block in enumerate(self.blockchain.chain):
            with st.expander(f"Block #{block['index']} - {block['timestamp']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Block Metadata:**")
                    st.write(f"📅 Timestamp: {block['timestamp']}")
                    st.write(f"🔢 Proof: {block['proof']}")
                    st.write(f"🔗 Previous Hash: `{block['previous_hash'][:20]}...`")
                    st.write(f"🆔 Current Hash: `{block['hash'][:20]}...`")
                
                with col2:
                    st.write("**Decision Data:**")
                    if isinstance(block['decision_data'], dict):
                        for key, value in block['decision_data'].items():
                            st.write(f"**{key}:** {value}")
                    else:
                        st.write(f"**Data:** {block['decision_data']}")
    
    def show_explanations(self):
        st.header("🧠 NLP Explanations")
        
        for block in self.blockchain.chain:
            if isinstance(block['decision_data'], dict):
                explanation = self.explainer.explain_decision(block['decision_data'])
                
                with st.expander(f"🔍 {explanation['original_decision']}"):
                    st.write(f"**🤖 Algorithm:** {explanation['algorithm']}")
                    st.write(f"**🏛️ Department:** {explanation['department']}")
                    st.info(f"**📝 Explanation:** {explanation['explanation']}")
                    st.write(f"**🔍 Factors considered:** {', '.join(explanation['factors_considered'])}")
                    st.write(f"**🕐 Explanation timestamp:** {explanation['explanation_timestamp']}")
    
    def show_decision_form(self):
        st.header("➕ Register New Decision")
        
        with st.form("new_decision_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                department = st.selectbox(
                    "Department",
                    ["NHS", "DWP", "HMRC", "Local-Gov", "UK-Border", "Environment-Agency"]
                )
                algorithm = st.text_input("Algorithm used", "risk-assessment-v1")
            
            with col2:
                impact = st.selectbox(
                    "Citizen impact",
                    ["low", "medium", "high"]
                )
                decision_text = st.text_area(
                    "Decision text",
                    "Approved application based on automated assessment"
                )
            
            submitted = st.form_submit_button("✅ Register in Blockchain")
            
            if submitted:
                if decision_text.strip():
                    new_block = self.blockchain.add_decision(
                        decision_text=decision_text,
                        algorithm_used=algorithm,
                        department=department,
                        citizen_impact=impact
                    )
                    st.success(f"✅ Decision registered in block #{new_block['index']}")
                    st.rerun()
                else:
                    st.error("❌ Please enter a valid decision text")

if __name__ == "__main__":
    dashboard = TransparencyDashboard()
    dashboard.run()
