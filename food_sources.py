"""Top 10 foods in Tanzania: % of households who buy vs grow."""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("tza_food_acquired.csv", low_memory=False)

df["bought"] = (df["quant_purchase"].fillna(0) > 0) | (df["value_purchase"].fillna(0) > 0)
df["grown"]  = df["quant_own"].fillna(0) > 0

top10 = df["j"].value_counts().head(10).index
res = (df[df["j"].isin(top10)]
       .groupby("j")[["bought", "grown"]].mean()
       .mul(100)
       .sort_values("grown"))

y = np.arange(len(res))
fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(y + 0.2, res["bought"], 0.4, color="#6B4E9B", label="Purchased")
ax.barh(y - 0.2, res["grown"],  0.4, color="#4A8C3F", label="Self-produced")
for i, (b, g) in enumerate(zip(res["bought"], res["grown"])):
    ax.text(b + 1, i + 0.2, f"{b:.0f}%", va="center", fontsize=9)
    ax.text(g + 1, i - 0.2, f"{g:.0f}%", va="center", fontsize=9)

ax.set_yticks(y)
ax.set_yticklabels([f.title()[:40] for f in res.index], fontsize=9)
ax.set_xlim(0, 110)
ax.set_xlabel("% of households consuming this food")
ax.set_title("Where Tanzanian households get their food", fontsize=14, weight="bold", loc="left")
ax.legend(loc="lower right", frameon=False)
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
plt.savefig("tza_food_sources.png", dpi=200, bbox_inches="tight")
print(res.round(1))
