import matplotlib.pyplot as plt
import polars as pl
import numpy as np
from highlight_text import fig_text
from pyfonts import load_google_font, set_default_font

df = pl.read_csv("src/2026/slope/ai-excitement.csv")

ages = df["Age"].to_list()
female = df["Female"].to_list()
male = df["Male"].to_list()
x = np.arange(len(ages))
age_labels = [f"{age} yo" for age in ages]

male_color = "#14213d"
female_color = "#335c67"

set_default_font(load_google_font("Schibsted Grotesk"))

fig, ax = plt.subplots()
fig.set_facecolor("#f8f9fa")
ax.set_facecolor("#f8f9fa")
ax.plot(x, female, color=female_color)
ax.plot(x, male, color=male_color)
ax.scatter(x, female, s=150, zorder=10, color=female_color)
ax.scatter(x, male, s=150, zorder=10, color=male_color)
ax.vlines([0, 1, 2, 3, 4, 5], ymin=0, ymax=60, colors="lightgrey", linewidths=1.6)
ax.spines[["left", "right", "bottom", "top"]].set_visible(False)
ax.set_xticks(x, age_labels, size=8)
ax.set_yticks([])
ax.tick_params(size=0, pad=3)
ax.set_ylim(0, 63)

for i, (m, f) in enumerate(zip(male, female)):
    ax.text(i + 0.1, m + 1, f"{m:.0f}%", color=male_color, size=9)
    ax.text(i + 0.1, f + 1, f"{f:.0f}%", color=female_color, size=9)

ax.text(
    x=-0.15,
    y=58,
    s="Men",
    color=male_color,
    alpha=0.9,
    va="center",
    ha="right",
    weight="bold",
    size=9,
)
ax.text(
    x=-0.15,
    y=49.3,
    s="Women",
    color=female_color,
    alpha=0.9,
    va="center",
    ha="right",
    weight="bold",
    size=9,
)

fig_text(
    x=0.5,
    y=0.95,
    s="<Women> are <less> excited about AI than <men>",
    highlight_textprops=[
        {"color": female_color, "weight": "bold"},
        {"style": "italic"},
        {"color": male_color, "weight": "bold"},
    ],
    size=16,
    ha="center",
    va="top",
)

fig_text(
    x=0.11,
    y=0.06,
    s="Percentage of people who are excited about AI, by age group and gender.",
    size=6,
    style="italic",
    alpha=0.75,
    va="top",
)

fig_text(
    x=0.89,
    y=0.07,
    s="<Data>: Digital Report 2026 (wearesocial.com)",
    size=6,
    alpha=0.5,
    highlight_textprops=[{"weight": "bold"}],
    ha="right",
    va="top",
)
fig_text(
    x=0.89,
    y=0.05,
    s="<Graphic>: Joseph Barbier",
    size=6,
    alpha=0.5,
    highlight_textprops=[{"weight": "bold"}],
    ha="right",
    va="top",
)

margin = 0.1
fig.subplots_adjust(
    bottom=margin + 0.04, top=1 - (margin + 0.02), left=margin, right=1 - margin
)

plt.savefig("src/2026/slope/chart.png", dpi=200)
