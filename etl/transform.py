import pandas as pd
import os

INPUT_DIR = "../input"
OUTPUT_DIR = "../output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------
# Load CSV files
# -----------------------------------------
def load_all_csv():
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".csv")]
    print("Found CSV files:", files)

    dfs = []
    for file in files:
        path = os.path.join(INPUT_DIR, file)
        print("Reading:", path)

        df = pd.read_csv(path)
        df["source_file"] = file
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


# -----------------------------------------
# Clean and normalize data
# -----------------------------------------
def clean_data(df):
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    if "score_(%)" in df.columns:
        df.rename(columns={"score_(%)": "score"}, inplace=True)

    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["lecture"] = pd.to_numeric(df["lecture"], errors="coerce")
    df["username"] = df["username"].astype(str).str.strip()

    return df


# -----------------------------------------
# Remove duplicates
# -----------------------------------------
def remove_duplicates(df):
    before = len(df)
    df_clean = df.drop_duplicates(subset=["username", "lecture"], keep="last")
    after = len(df_clean)

    print(f"Removed duplicates: {before - after}")
    return df_clean


# -----------------------------------------
# Build leaderboard
# -----------------------------------------
def build_leaderboard(df):
    leaderboard = (
        df.groupby("username")
        .agg(
            lectures=("lecture", "nunique"),
            total_score=("score", "sum"),
        )
        .reset_index()
    )

    leaderboard = leaderboard.sort_values("total_score", ascending=False)

    leaderboard["rating"] = range(1, len(leaderboard) + 1)

    leaderboard = leaderboard[["rating", "username", "lectures", "total_score"]]

    leaderboard.reset_index(drop=True, inplace=True)

    return leaderboard


# -----------------------------------------
# MAIN
# -----------------------------------------
df_raw = load_all_csv()
df_clean = clean_data(df_raw)
df_unique = remove_duplicates(df_clean)

leaderboard = build_leaderboard(df_unique)

print("\n=== FINAL LEADERBOARD ===")
print(leaderboard.to_string(index=False))   # 🔥 No index printed
print(leaderboard.info())

leaderboard.to_csv(os.path.join(OUTPUT_DIR, "leaderboard.csv"), index=False)
print("\nSaved leaderboard → output/leaderboard.csv")
