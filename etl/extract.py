import pandas as pd
import os

# Path
folder = "../input/"

def xlsx_to_csv(input_path, output_path=None):
    if output_path is None:
        output_path = input_path.replace(".xlsx", ".csv")
    df = pd.read_excel(input_path)
    df.to_csv(output_path)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")
    return output_path

for file in os.listdir(folder):
    if file.endswith(".xlsx"):
        full_path = os.path.join(folder, file)
        xlsx_to_csv(full_path)