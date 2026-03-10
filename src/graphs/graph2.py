import matplotlib.pyplot as plt
import pandas as pd

from src.config import DPI, OUTPUT_DIR, ROOT_DIR
from src.style import BLUE, GREEN, RED, TEXT_COLOR, YELLOW, apply_global_style


def run() -> None:
    # 1. Load data
    data_path = ROOT_DIR / "data" / "whaling_data_clean.csv"
    df = pd.read_csv(data_path)

    # 2. Preprocess
    # Group by 5-year intervals (five-year periods)
    df["five_year"] = (df["yearOut_num"] // 5) * 5

    # Group and calculate mean values per voyage
    # Grouping by 'five_year' and calculating means for the products
    metrics = ["oil", "sperm", "bone", "voyage_duration"]

    # Filter for reasonable duration (remove -100)
    df_clean = df[df["voyage_duration"] >= 0]

    grouped = df_clean.groupby("five_year")[metrics].mean().reset_index()

    # Normalization to [0, 100] for each series to make them comparable
    for metric in metrics:
        max_val = grouped[metric].max()
        if max_val > 0:
            grouped[f"{metric}_norm"] = (grouped[metric] / max_val) * 100
        else:
            grouped[f"{metric}_norm"] = 0

    # Apply style
    apply_global_style()

    # 3. Plot
    _, ax = plt.subplots(figsize=(12, 6))

    # Plot metrics
    ax.plot(
        grouped["five_year"],
        grouped["oil_norm"],
        color=RED,
        linewidth=2,
        label="Ворвань (жир)",
    )
    ax.plot(
        grouped["five_year"],
        grouped["sperm_norm"],
        color=YELLOW,
        linewidth=2,
        label="Спермацет",
    )
    ax.plot(
        grouped["five_year"],
        grouped["bone_norm"],
        color=GREEN,
        linewidth=2,
        label="Китовый ус",
    )

    # Plot duration for comparison (as dashed line like in sample2.jpg)
    ax.plot(
        grouped["five_year"],
        grouped["voyage_duration_norm"],
        color=BLUE,
        linewidth=2,
        linestyle="--",
        label="Средняя продолжительность рейса",
    )

    # Visual style following sample2.jpg (but with white background)
    ax.set_title(
        "Сравнительная динамика добычи и продолжительности рейсов",
        fontsize=16,
        pad=20,
        color=TEXT_COLOR,
    )
    ax.set_xlabel("Год выхода (по пятилетиям)", fontsize=12, labelpad=10)
    ax.set_ylabel("Относительная динамика (%)", fontsize=12, labelpad=10)

    # Grid
    ax.grid(True, axis="both", linestyle="--", alpha=0.3)

    # Axis limits and ticks
    ax.set_xlim(grouped["five_year"].min(), grouped["five_year"].max())
    ax.set_ylim(0, 110)  # A bit above 100 for better view

    # Legend
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2, frameon=True)

    # Save
    output_path = OUTPUT_DIR / "graph2.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=DPI, facecolor="white", bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    run()
