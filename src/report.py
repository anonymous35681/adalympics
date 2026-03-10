import pandas as pd

from src.config import ROOT_DIR


def run_analysis():
    data_path = ROOT_DIR / "data" / "whaling_data_clean.csv"
    # Load data with low_memory=False to avoid DtypeWarning
    df = pd.read_csv(data_path, low_memory=False)

    # 1. Data Preparation
    # Convert tonnage to numeric, ignoring errors (will become NaN)
    df["tonnage_num"] = pd.to_numeric(df["tonnage"], errors="coerce")

    # Fill missing product values with zeros for correct summation
    for col in ["oil", "sperm", "bone"]:
        df[col] = df[col].fillna(0)

    # Calculate total production for each voyage
    df["total_production"] = df["oil"] + df["sperm"] + df["bone"]

    # Define "no catch" (if all three indicators are zero)
    # Important: only consider voyages where tonnage is known
    df_with_tonnage = df[df["tonnage_num"].notna()].copy()

    # 2. Grouping
    group_large = df_with_tonnage[df_with_tonnage["tonnage_num"] > 300]
    group_small = df_with_tonnage[df_with_tonnage["tonnage_num"] < 200]

    # 3. Production calculations (mean per voyage)
    avg_prod_large = group_large["total_production"].mean()
    avg_prod_small = group_small["total_production"].mean()
    ratio_prod = avg_prod_large / avg_prod_small if avg_prod_small > 0 else 0

    # 4. "No catch" probability calculations
    # Count voyages with zero production
    no_catch_large = (group_large["total_production"] == 0).sum()
    prob_no_catch_large = (
        no_catch_large / len(group_large) if len(group_large) > 0 else 0
    )

    no_catch_small = (group_small["total_production"] == 0).sum()
    prob_no_catch_small = (
        no_catch_small / len(group_small) if len(group_small) > 0 else 0
    )

    # 5. Output results for the report
    print("--- Analysis Results ---")
    print(f"Group > 300 tons: voyage count = {len(group_large)}")
    print(f"Group < 200 tons: voyage count = {len(group_small)}")
    print(f"\nAverage production (>300): {avg_prod_large:.2f}")
    print(f"Average production (<200): {avg_prod_small:.2f}")
    print(f"Difference: {ratio_prod:.2f} times")
    print(f"\nProbability of no catch (>300): {prob_no_catch_large:.2%}")
    print(f"Probability of no catch (<200): {prob_no_catch_small:.2%}")


if __name__ == "__main__":
    run_analysis()
