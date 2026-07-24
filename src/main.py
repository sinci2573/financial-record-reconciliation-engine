from data_loader import load_purchase_data, load_finance_data
from validator import validate_data
from reconciler import reconcile_data
from report_generator import save_report


def main():

    purchase_df = load_purchase_data("data/sample_purchase.csv")
    finance_df = load_finance_data("data/sample_finance.xlsx")

    purchase_df = validate_data(purchase_df)
    finance_df = validate_data(finance_df)

    report = reconcile_data(purchase_df, finance_df)

    print("\nReconciliation Summary\n")
    print(report)

    save_report(report, "data/reconciliation_report.csv")


if __name__ == "__main__":
    main()