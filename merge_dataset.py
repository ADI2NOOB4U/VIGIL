import pandas as pd

files = [
    "phishing_url_dataset_unique.csv",
    "malicious_phish.csv",
    "PhiUSIIL_Phishing_URL_Dataset.csv",
    "dataset_phishing.csv",
    "fixed_dataset_phishing.csv"  # ✅ ADD THIS
]

dfs = []

for file in files:
    print(f"Processing: {file}")
    try:
        df = pd.read_csv(file)
    except:
        print(f"❌ File missing: {file}")
    continue

    # fix duplicate columns
    df.columns = [f"{col}_{i}" if list(df.columns).count(col) > 1 else col 
              for i, col in enumerate(df.columns)]
    df.columns = [c.lower() for c in df.columns]
    df = df.loc[:, ~df.columns.duplicated()]

    # fix url
    for col in df.columns:
        if 'url' in col:
            df.rename(columns={col: 'url'}, inplace=True)

    # fix label
    for col in df.columns:
        if 'label' in col or 'class' in col or 'result' in col or 'type' in col:
            df.rename(columns={col: 'label'}, inplace=True)

    # skip bad files
    if 'url' not in df.columns or 'label' not in df.columns:
        print(f"❌ Skipped {file}")
        continue

    temp = df[['url', 'label']].copy()
temp = df[['url', 'label']].copy()
dfs.append(temp)

# merge
dfs = [d.reset_index(drop=True) for d in dfs]
final_df = pd.concat(dfs, ignore_index=True)

# clean
final_df = final_df.dropna().drop_duplicates()

final_df.to_csv("final_dataset.csv", index=False)

print("✅ DONE:", len(final_df))