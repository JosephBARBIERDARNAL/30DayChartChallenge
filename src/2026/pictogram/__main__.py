import matplotlib.pyplot as plt
from pywaffle import Waffle
from pyfonts import load_google_font, set_default_font
from highlight_text import fig_text

# data source
# https://wearesocial.com/uk/blog/2025/10/digital-2026-global-overview-report/
people_using_internet = 6.04 * 1e9
people_total = 8.25 * 1.0e9
share_people_using_internet = (people_using_internet / people_total) * 100

set_default_font(load_google_font("Lexend Deca"))

fig, ax = plt.subplots(figsize=(6, 6))
fig.set_facecolor("#f8f9fa")
ax.set_facecolor("#f8f9fa")

Waffle.make_waffle(
    ax=ax,
    rows=10,
    columns=10,
    interval_ratio_x=0.1,
    colors=["#0d3b66", "#e07a5f"],
    values=[share_people_using_internet, 100 - share_people_using_internet],
    icons=["person", "person"],
    vertical=True,
    font_size=30,
)

fig_text(
    x=0.485,
    y=0.97,
    s=f"<{share_people_using_internet:.0f}%> of humans are using the Internet",
    size=18,
    ha="center",
    highlight_textprops=[{"color": "#0d3b66", "weight": "bold"}],
)

fig_text(
    x=0.485,
    y=0.92,
    s=f"This represents <{(round(people_using_internet / 1e9, 2))}B> out of the world's {(round(people_total / 1e9, 1))}B people, as of 2026",
    size=11,
    alpha=0.5,
    ha="center",
    highlight_textprops=[{"color": "#0d3b66", "weight": "bold", "alpha": 1}],
)
fig_text(
    x=0.1,
    y=0.06,
    s="<Data>: Digital Report 2026 (wearesocial.com)",
    size=7,
    alpha=0.8,
    color="#555555",
    highlight_textprops=[{"weight": "bold"}],
)
fig_text(
    x=0.1,
    y=0.04,
    s="<Graphic>: Joseph Barbier",
    size=7,
    alpha=0.8,
    color="#555555",
    highlight_textprops=[{"weight": "bold"}],
)

margin = 0.1
fig.subplots_adjust(
    bottom=margin, top=1 - (margin + 0.04), left=margin, right=1 - margin
)

plt.savefig("src/2026/pictogram/chart.png", dpi=200)
