import sys
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------
st.set_page_config(
    page_title="Financial Record Reconciliation Engine",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------------------------
# Add src folder to Python path
# -----------------------------------------------------
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from data_loader import load_purchase_data, load_finance_data
from validator import validate_data
from reconciler import reconcile_records

# -----------------------------------------------------
# Title
# -----------------------------------------------------
st.title("📊 Financial Record Reconciliation Engine")

st.write(
    "Upload purchase and finance records to automatically identify "
    "missing transactions, mismatched quantities, and part number discrepancies."
)

st.divider()

# -----------------------------------------------------
# File Uploads
# -----------------------------------------------------
purchase_file = st.file_uploader(
    "📄 Upload Purchase CSV",
    type=["csv"]
)

finance_file = st.file_uploader(
    "💰 Upload Finance Excel",
    type=["xlsx"]
)

# -----------------------------------------------------
# Run Reconciliation
# -----------------------------------------------------
if purchase_file is not None and finance_file is not None:

    if st.button("🚀 Run Reconciliation", type="primary"):

        try:
            # Load data
            purchase_df = load_purchase_data(purchase_file)
            finance_df = load_finance_data(finance_file)

            # Validate data
            validate_data(purchase_df)
            validate_data(finance_df)

            # Reconcile
            report = reconcile_records(purchase_df, finance_df)

            # Success message
            st.success(f"✅ {len(report)} discrepancies detected.")

            # ---------------------------------------------
            # KPI Metrics
            # ---------------------------------------------
            purchase_count = len(purchase_df)
            finance_count = len(finance_df)
            discrepancy_count = len(report)

            accuracy = (
                ((purchase_count - discrepancy_count) / purchase_count) * 100
                if purchase_count > 0
                else 0
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("📄 Purchase Records", purchase_count)
            col2.metric("💰 Finance Records", finance_count)
            col3.metric("⚠️ Issues Found", discrepancy_count)
            col4.metric("✅ Accuracy", f"{accuracy:.1f}%")

            st.divider()

            # ---------------------------------------------
            # Report + Chart
            # ---------------------------------------------
            left, right = st.columns([2, 1])

            with left:

                st.subheader("📋 Reconciliation Report")

                st.dataframe(
                    report,
                    use_container_width=True,
                    height=320
                )

            with right:

                st.subheader("📊 Issue Distribution")

                if not report.empty:

                    issue_counts = report["Issue"].value_counts()

                    fig, ax = plt.subplots(figsize=(5, 5))

                    ax.pie(
                        issue_counts,
                        labels=issue_counts.index,
                        autopct="%1.1f%%",
                        startangle=90
                    )

                    ax.axis("equal")

                    st.pyplot(fig)

                else:
                    st.info("No discrepancies found.")

            st.divider()

            # ---------------------------------------------
            # Download Report
            # ---------------------------------------------
            st.download_button(
                label="📥 Download Reconciliation Report",
                data=report.to_csv(index=False),
                file_name="reconciliation_report.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error: {e}")