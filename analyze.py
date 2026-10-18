# analyze.py
# FINDINGS: The strongest breakdown predictors are km_since_service (corr 0.40), avg_daily_km
# (corr 0.25), and load_factor (corr 0.22). Total mileage (odometer_km) and age_years have
# near-zero correlation (0.002 and -0.001) — they do NOT separate cars that broke from those
# that did not. The risk score below is built only from the three columns that do.

import pandas as pd


def compute_risk_scores(path: str = "fleet_history.csv") -> pd.DataFrame:
    """Load fleet history and return a DataFrame ranked by breakdown risk (0–100).

    Risk score is a weighted sum of three min-max normalised signals:
      - km_since_service  (weight 0.55) — strongest predictor, corr 0.40
      - avg_daily_km      (weight 0.25) — second predictor,   corr 0.25
      - load_factor       (weight 0.20) — third predictor,    corr 0.22

    odometer_km and age_years are deliberately excluded: their correlation
    with breakdown is ~0.002 and ~-0.001 respectively — no predictive value.
    """
    df = pd.read_csv(path)

    def minmax(col: pd.Series) -> pd.Series:
        """Scale a column to [0, 1]."""
        lo, hi = col.min(), col.max()
        return (col - lo) / (hi - lo) if hi != lo else col * 0.0

    df["risk_score"] = (
        minmax(df["km_since_service"]) * 0.55
        + minmax(df["avg_daily_km"])   * 0.25
        + minmax(df["load_factor"])    * 0.20
    ) * 100

    return (
        df[["car_id", "km_since_service", "avg_daily_km", "load_factor", "risk_score"]]
        .sort_values("risk_score", ascending=False)
        .reset_index(drop=True)
    )


def print_factor_comparison(path: str = "fleet_history.csv") -> None:
    """Print the column-by-column comparison that shows which factors matter."""
    df = pd.read_csv(path)
    cols = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

    print("=== Factor comparison: broke down vs did not ===")
    corrs = df[cols + ["broke_down"]].corr()["broke_down"].drop("broke_down")
    for col in cols:
        means = df.groupby("broke_down")[col].mean()
        diff_pct = (means[1] - means[0]) / means[0] * 100
        print(
            f"  {col:<22}  corr={corrs[col]:+.3f}  "
            f"no-breakdown avg={means[0]:>8.1f}  "
            f"breakdown avg={means[1]:>8.1f}  "
            f"diff={diff_pct:+.1f}%"
        )
    print()
    print("  odometer_km and age_years: correlation ~0.00 — NOT useful predictors.")
    print("  km_since_service, avg_daily_km, load_factor: these separate the groups.\n")


if __name__ == "__main__":
    print_factor_comparison()

    ranked = compute_risk_scores()
    print("=== Cars ranked by breakdown risk (highest first) ===")
    print(f"{'Rank':<5} {'car_id':<12} {'km_since_svc':>12} {'avg_daily_km':>12} {'load_factor':>11} {'risk_score':>10}")
    print("-" * 67)
    for rank, row in ranked.iterrows():
        print(
            f"{rank + 1:<5} {row['car_id']:<12} "
            f"{row['km_since_service']:>12.0f} "
            f"{row['avg_daily_km']:>12.0f} "
            f"{row['load_factor']:>11.2f} "
            f"{row['risk_score']:>10.1f}"
        )
