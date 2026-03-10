import matplotlib.pyplot as plt
import pandas as pd

from src.config import DPI, OUTPUT_DIR, ROOT_DIR
from src.style import BLUE, TEXT_COLOR, YELLOW, apply_global_style


def run() -> None:
    # 1. Load data
    data_path = ROOT_DIR / "data" / "whaling_data_clean.csv"
    df = pd.read_csv(data_path, low_memory=False)

    # 2. Preprocess
    # Group by 5-year intervals (five-year periods)
    df["five_year"] = (df["yearOut_num"] // 5) * 5

    # Group and calculate mean duration and success
    df["success"] = df[["oil", "sperm", "bone"]].sum(axis=1)

    # Filter for reasonable duration
    df_clean = df[df["voyage_duration"] >= 0]

    grouped = (
        df_clean.groupby("five_year")
        .agg({"voyage_duration": "mean", "success": "mean"})
        .reset_index()
    )

    # Normalization for success to match duration scale roughly for overlay
    max_duration = grouped["voyage_duration"].max()
    max_success = grouped["success"].max()
    if max_success > 0:
        grouped["success_scaled"] = (grouped["success"] / max_success) * max_duration
    else:
        grouped["success_scaled"] = 0

    # Apply style
    apply_global_style()

    # 3. Plot
    _, ax = plt.subplots(figsize=(12, 6))

    # Plot the duration line
    ax.plot(
        grouped["five_year"],
        grouped["voyage_duration"],
        color=BLUE,
        linewidth=2,
        label="Средняя продолжительность рейса",
    )

    # Plot success (orange/yellow dashed line as in sample1.jpg)
    ax.plot(
        grouped["five_year"],
        grouped["success_scaled"],
        color=YELLOW,
        linewidth=2,
        linestyle="--",
        label="Успешность рейсов (отн.)",
    )

    # Find the actual peak of the duration line
    peak_idx = grouped["voyage_duration"].idxmax()
    peak_x = grouped.loc[peak_idx, "five_year"]
    peak_y = grouped.loc[peak_idx, "voyage_duration"]

    # Draw the point (large blue circle)
    ax.plot(peak_x, peak_y, "o", color=BLUE, markersize=12)

    # Text label next to the peak
    ax.text(
        peak_x + 3,
        peak_y,
        f"{int(peak_x)} г.\nсреднее {peak_y:.2f} лет.",
        color=TEXT_COLOR,
        fontsize=12,
        fontweight="bold",
        verticalalignment="center",
    )

    # Visual style following sample1.jpg (but with white background)
    ax.set_title(
        "Динамика средней продолжительности и успешности китобойных рейсов",
        fontsize=16,
        pad=20,
        color=TEXT_COLOR,
    )
    ax.set_xlabel("Год выхода (по пятилетиям)", fontsize=12, labelpad=10)
    ax.set_ylabel("Продолжительность (лет) / Успешность", fontsize=12, labelpad=10)

    # Grid
    ax.grid(True, axis="both", linestyle="--", alpha=0.3)

    # Axis limits and ticks
    ax.set_xlim(grouped["five_year"].min(), grouped["five_year"].max())

    # Legend
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=True)

    # Save
    output_path = OUTPUT_DIR / "graph1.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=DPI, facecolor="white", bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    run()
