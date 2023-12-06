import pandas as pd


def convert_csv_to_excel(csv_file_path, excel_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Write to an Excel file
    df.to_excel(excel_file_path, index=False)

    print(f"File converted and saved as '{excel_file_path}'")


convert_csv_to_excel('subsequences.csv', 'subsequences.xlsx')
convert_csv_to_excel('subsequences_with_ids.csv', 'subsequences_with_ids.xlsx')