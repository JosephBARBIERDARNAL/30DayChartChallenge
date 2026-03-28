import matplotlib.pyplot as plt
import squarify
import polars as pl
from pyfonts import load_google_font, set_default_font
from drawarrow import ax_arrow


df = pl.read_csv("src/2026/part-to-whole/languages_total.csv")

LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "R": "#198CE7",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178C6",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Rust": "#dea584",
    "Shell": "#89e051",
    "Typst": "#239DAD",
    "Just": "#384D54",
    "C": "#555555",
    "Makefile": "#427819",
    "Jupyter Notebook": "#DA5B0B",
}


languages = df["language"].to_list()
percentages = df["percentage"].to_list()
colors = [LANGUAGE_COLORS[lang] for lang in languages]
language_percentages = dict(zip(languages, percentages))

HIDE_LABELS = {"Makefile", "C", "Just", "Shell", "Typst", "JavaScript"}

labels = list()
for lang, perc in zip(languages, percentages):
    if lang not in HIDE_LABELS:
        if lang in ["HTML", "R"]:
            label = f"{lang}  {round(perc)}%"
        else:
            label = f"{lang}\n{round(perc)}%"
    else:
        label = ""
    labels.append(label)

set_default_font(load_google_font("DM Sans"))
fig, ax = plt.subplots()
squarify.plot(
    sizes=percentages,
    label=labels,
    color=colors,
    ax=ax,
    text_kwargs={"size": 13, "color": "white", "weight": "bold"},
    bar_kwargs={"edgecolor": "black"},
)
ax.set_axis_off()

ax.text(
    x=55,
    y=103,
    s=f"Typst  {round(language_percentages['Typst'])}%",
    color="white",
    size=10,
    weight="bold",
    ha="center",
    va="bottom",
    bbox={
        "edgecolor": "black",
        "linewidth": 0.8,
        "pad": 1,
        "facecolor": LANGUAGE_COLORS["Typst"],
    },
)
ax_arrow(
    [57, 104],
    [70, 100],
    radius=-0.3,
    width=1,
    clip_on=False,
    color="black",
    head_width=3,
    head_length=6,
    fill_head=False,
)

ax.text(
    x=84.5,
    y=53,
    s=f"JavaScript\n{round(language_percentages['JavaScript'])}%",
    size=13,
    weight="bold",
    ha="center",
    va="center",
)

fig.text(
    x=0.5,
    y=1.02,
    s="Which languages do I use the most?",
    ha="center",
    va="top",
    font=load_google_font("Domine"),
    size=20,
)
fig.text(
    x=0.125,
    y=0.1,
    s="Data from all of my public repositories on Github",
    va="top",
    style="italic",
    alpha=0.8,
    color="#555555",
    size=7,
)
fig.text(
    x=0.125,
    y=0.08,
    s="github.com/y-sunflower",
    va="top",
    weight="bold",
    alpha=0.8,
    color="#555555",
    size=7,
)

plt.tight_layout()
plt.savefig("src/2026/part-to-whole/chart.png", dpi=200, bbox_inches="tight")
