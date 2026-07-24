import pandas as pd


def reconcile_records(purchase_df, finance_df):
    """
    Compare purchase and finance records to identify discrepancies.
    """

    report = []

    purchase_map = purchase_df.set_index("Transaction_ID").to_dict("index")
    finance_map = finance_df.set_index("Transaction_ID").to_dict("index")

    all_transactions = sorted(set(purchase_map.keys()) | set(finance_map.keys()))

    for txn in all_transactions:

        if txn not in purchase_map:
            report.append({
                "Transaction_ID": txn,
                "Issue": "Extra transaction in Finance"
            })
            continue

        if txn not in finance_map:
            report.append({
                "Transaction_ID": txn,
                "Issue": "Missing transaction in Finance"
            })
            continue

        purchase = purchase_map[txn]
        finance = finance_map[txn]

        if purchase["Part_Number"] != finance["Part_Number"]:
            report.append({
                "Transaction_ID": txn,
                "Issue": "Part number mismatch"
            })

        if purchase["Quantity"] != finance["Quantity"]:
            report.append({
                "Transaction_ID": txn,
                "Issue": "Quantity mismatch"
            })

        if purchase["Unit_Price"] != finance["Unit_Price"]:
            report.append({
                "Transaction_ID": txn,
                "Issue": "Unit price mismatch"
            })

    return pd.DataFrame(report)