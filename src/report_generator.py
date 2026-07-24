def save_report(report_df, output_path):
    """
    Save the reconciliation report to a CSV file.
    """
    report_df.to_csv(output_path, index=False)
    print(f"Report saved to: {output_path}")