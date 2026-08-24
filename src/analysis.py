from pathlib import Path
from io import BytesIO
import zipfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = ROOT / "figures"

for folder in (DATA_DIR, RESULTS_DIR, FIGURES_DIR):
    folder.mkdir(exist_ok=True)


# Fixed 30-day window for reproducibility
DATES = pd.date_range("2024-01-01", periods=180, freq="D")


def download_daily_events(date):
    date_str = date.strftime("%Y%m%d")
    url = f"http://data.gdeltproject.org/events/{date_str}.export.CSV.zip"

    print(f"Downloading {date_str}...")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    with zipfile.ZipFile(BytesIO(response.content)) as z:
        filename = z.namelist()[0]

        with z.open(filename) as f:
            df = pd.read_csv(
                f,
                sep="\t",
                header=None,
                dtype=str,
                low_memory=False,
            )

    return df


def build_daily_series():
    rows = []

    for date in DATES:
        try:
            df = download_daily_events(date)

            total_events = len(df)

            # GDELT GoldsteinScale column
            goldstein = pd.to_numeric(df.iloc[:, 30], errors="coerce")

            conflict_events = (goldstein < 0).sum()
            severe_conflict = (goldstein <= -5).sum()

            rows.append({
                "date": date,
                "total_events": total_events,
                "conflict_events": conflict_events,
                "severe_conflict_events": severe_conflict,
            })

        except Exception as e:
            print(f"Skipped {date.date()}: {e}")

    result = pd.DataFrame(rows)

    if len(result) < 10:
        raise RuntimeError(
            "Too few daily files were downloaded successfully."
        )

    result.to_csv(
        DATA_DIR / "gdelt_event_pressure.csv",
        index=False,
    )

    return result


def create_features(df):
    out = df.copy()

    out["conflict_share"] = (
        out["conflict_events"]
        / out["total_events"]
    )

    out["severe_conflict_share"] = (
        out["severe_conflict_events"]
        / out["total_events"]
    )

    lagged = out["conflict_share"].shift(1)

    out["rolling_mean"] = (
        lagged.rolling(window=7, min_periods=4).mean()
    )

    out["rolling_std"] = (
        lagged.rolling(window=7, min_periods=4).std()
    )

    out["rolling_z"] = (
        (out["conflict_share"] - out["rolling_mean"])
        / out["rolling_std"].replace(0, np.nan)
    )

    out["lag1_share"] = out["conflict_share"].shift(1)

    return out


def estimate_model(df):
    model_df = df[
        ["conflict_share", "lag1_share"]
    ].dropna()

    X = sm.add_constant(model_df["lag1_share"])
    y = model_df["conflict_share"]

    model = sm.OLS(y, X).fit(cov_type="HC3")

    return model, model_df


def run_adf(df):
    series = df["conflict_share"].dropna()

    result = adfuller(series, autolag="AIC")

    return {
        "adf_statistic": float(result[0]),
        "p_value": float(result[1]),
        "used_lag": int(result[2]),
        "observations": int(result[3]),
    }


def make_plots(df, model_df):
    fig, ax = plt.subplots(figsize=(11, 6))

    ax.plot(
        df["date"],
        df["conflict_share"],
        label="Conflict-event share",
    )

    ax.plot(
        df["date"],
        df["rolling_mean"],
        label="7-day lagged baseline",
    )

    ax.set_title("Political Event Pressure")
    ax.set_xlabel("Date")
    ax.set_ylabel("Share of events with negative Goldstein score")
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        FIGURES_DIR / "event_pressure_timeseries.png",
        dpi=180,
    )
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.plot(
        df["date"],
        df["rolling_z"],
    )

    ax.axhline(
        2,
        linestyle="--",
        label="Spike threshold",
    )

    ax.set_title("Rolling Political Event Pressure Z-Score")
    ax.set_xlabel("Date")
    ax.set_ylabel("Rolling z-score")
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        FIGURES_DIR / "rolling_zscore.png",
        dpi=180,
    )
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 6))

    ax.scatter(
        model_df["lag1_share"],
        model_df["conflict_share"],
        alpha=0.6,
    )

    ax.set_title("Lag-1 Persistence")
    ax.set_xlabel("Previous day's conflict share")
    ax.set_ylabel("Current day's conflict share")

    fig.tight_layout()
    fig.savefig(
        FIGURES_DIR / "lag_persistence.png",
        dpi=180,
    )
    plt.close(fig)


def save_results(df, model, adf_result):
    spikes = df.loc[
        df["rolling_z"] >= 2,
        [
            "date",
            "total_events",
            "conflict_events",
            "conflict_share",
            "rolling_z",
        ],
    ].copy()

    spikes.to_csv(
        RESULTS_DIR / "spike_days.csv",
        index=False,
    )

    df.to_csv(
        RESULTS_DIR / "processed_event_pressure.csv",
        index=False,
    )

    text = []

    text.append("POLITICAL EVENT PRESSURE")
    text.append("=" * 50)
    text.append("")
    text.append("LAG-1 OLS MODEL")
    text.append("-" * 50)
    text.append(model.summary().as_text())
    text.append("")
    text.append("ADF TEST")
    text.append("-" * 50)
    text.append(str(adf_result))
    text.append("")
    text.append(f"Detected spikes: {len(spikes)}")

    if len(spikes) > 0:
        text.append("")
        text.append("SPIKE DAYS")
        text.append(spikes.to_string(index=False))

    (
        RESULTS_DIR / "model_summary.txt"
    ).write_text(
        "\n".join(text),
        encoding="utf-8",
    )

    return spikes

def analyze_spike_contributors(date_str):
    date = pd.to_datetime(date_str)
    date_code = date.strftime("%Y%m%d")

    url = f"http://data.gdeltproject.org/events/{date_code}.export.CSV.zip"

    print(f"Analyzing spike contributors for {date_code}...")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    with zipfile.ZipFile(BytesIO(response.content)) as z:
        filename = z.namelist()[0]

        with z.open(filename) as f:
            df = pd.read_csv(
                f,
                sep="\t",
                header=None,
                dtype=str,
                low_memory=False,
            )

    # Column 30 = GoldsteinScale
    goldstein = pd.to_numeric(
        df.iloc[:, 30],
        errors="coerce",
    )

    # Keep only conflict-coded events
    conflict_df = df.loc[
        goldstein < 0
    ].copy()

    # GDELT actor country codes
    actor1_country = conflict_df.iloc[:, 7].fillna("Unknown")
    actor2_country = conflict_df.iloc[:, 17].fillna("Unknown")

    all_countries = pd.concat([
        actor1_country,
        actor2_country,
    ])

    identifiable = all_countries[
        all_countries != "Unknown"
    ]

    total_identifiable = len(identifiable)

    country_counts = (
        identifiable
        .value_counts()
        .head(15)
    )

    country_result = country_counts.reset_index()
    country_result.columns = [
        "country_code",
        "count",
    ]

    country_result["share"] = (
        country_result["count"]
        / total_identifiable
    )

    country_result.to_csv(
        RESULTS_DIR / f"spike_contributors_{date_str}.csv",
        index=False,
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        country_result["country_code"],
        country_result["count"],
    )

    ax.set_title(
        f"Top Actor-Country Contributors to Conflict Events\n{date_str}"
    )
    ax.set_xlabel(
        "Conflict-event appearances"
    )
    ax.set_ylabel(
        "GDELT country code"
    )

    ax.invert_yaxis()

    fig.tight_layout()

    fig.savefig(
        FIGURES_DIR / f"spike_contributors_{date_str}.png",
        dpi=180,
    )

    plt.close(fig)

    return country_result
def make_polished_spike_figure(df, spikes):
    plot_df = df.copy()
    spike_df = spikes.copy()

    plot_df["date"] = pd.to_datetime(plot_df["date"])
    spike_df["date"] = pd.to_datetime(spike_df["date"])

    top5 = spike_df.sort_values(
        "rolling_z",
        ascending=False
    ).head(5)

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(
        plot_df["date"],
        plot_df["conflict_share"],
        linewidth=1.8,
        label="Conflict-event share"
    )

    ax.scatter(
        spike_df["date"],
        spike_df["conflict_share"],
        s=45,
        marker="o",
        label="Detected spikes",
        zorder=3
    )

    ax.set_title(
        "Political Event Pressure Across 180 Days\n"
        "Detected Spike Periods and Top 5 Anomalies"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Conflict-event share")
    ax.legend()

    for _, row in top5.iterrows():
        ax.annotate(
            f"{row['date'].strftime('%Y-%m-%d')}\nz={row['rolling_z']:.2f}",
            xy=(row["date"], row["conflict_share"]),
            xytext=(8, 8),
            textcoords="offset points",
            fontsize=8
        )

    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    fig.tight_layout()

    fig.savefig(
        FIGURES_DIR / "political_event_pressure_180d_annotated.png",
        dpi=220
    )

    plt.close(fig)
def main():
    df = build_daily_series()
    df = create_features(df)

    model, model_df = estimate_model(df)
    adf_result = run_adf(df)

    make_plots(df, model_df)

    spikes = save_results(
        df,
        model,
        adf_result,
    )
    make_polished_spike_figure(df, spikes)
    if len(spikes) > 0:
        top_spike_date = pd.to_datetime(
            spikes.iloc[0]["date"]
        ).strftime("%Y-%m-%d")

        contributors = analyze_spike_contributors(
            top_spike_date
        )

        print("")
        print("Top spike contributors:")
        print(contributors.head(10).to_string(index=False))

    print("")
    print("Analysis complete.")
    print(f"Days analyzed: {len(df)}")
    print(f"Detected spikes: {len(spikes)}")
    print(
        f"Lag coefficient: "
        f"{model.params['lag1_share']:.3f}"
    )
    print(
        f"Lag p-value: "
        f"{model.pvalues['lag1_share']:.4g}"
    )
    print(
        f"ADF p-value: "
        f"{adf_result['p_value']:.4g}"
    )


if __name__ == "__main__":
    main()