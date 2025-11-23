import os
import pathlib

MPL_DIR = pathlib.Path(__file__).resolve().parents[1] / ".cache" / "matplotlib"
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_DIR))
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt

OUTPUT = pathlib.Path(__file__).resolve().parents[1] / "figures" / "peak_rss.png"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

languages = ["Go", "Java", "Node.js", "Python", "Rust"]
rss_mb = [17.52, 343.69, 87.05, 19.83, 11.64]

plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(languages, rss_mb, color="#d1851f")

ax.set_xlabel("Peak RSS (MB)")
ax.set_title("Binary Trees (depth=16)")
ax.invert_yaxis()

for bar, value in zip(bars, rss_mb):
    ax.text(
        value + 5,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.1f}",
        va="center",
        color="white",
    )

plt.tight_layout()
fig.savefig(OUTPUT, dpi=200)
print(f"Saved chart to {OUTPUT}")
