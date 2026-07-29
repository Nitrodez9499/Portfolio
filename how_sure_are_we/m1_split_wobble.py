"""
M1 -- See the wobble.

Take the 150 scored results, split them into two random halves (75/75),
score each half's accuracy separately, and compare. The gap between the
two numbers is what the rest of this project (M2 bootstrap, M3 showdown)
puts a real number on.
"""

import pandas as pd
import numpy as np

# A fixed seed means anyone re-running this script gets the exact same
# split -- that's what "reproducible" means for M1. Change the seed and
# you'll get a different (but equally valid) wobble.
SEED = 42

df = pd.read_csv("results_150_clean.csv")
assert len(df) == 150, f"expected 150 rows, got {len(df)}"

rng = np.random.default_rng(SEED)

# Shuffle the row indices, then cut the deck in half.
indices = rng.permutation(len(df))
half_a_idx = indices[:75]
half_b_idx = indices[75:]

half_a = df.iloc[half_a_idx]
half_b = df.iloc[half_b_idx]

acc_a = half_a["correct"].mean()
acc_b = half_b["correct"].mean()

print(f"Half A: {half_a['correct'].sum()}/75 = {acc_a:.4f} ({acc_a*100:.1f}%)")
print(f"Half B: {half_b['correct'].sum()}/75 = {acc_b:.4f} ({acc_b*100:.1f}%)")
print(f"Gap between halves: {abs(acc_a - acc_b)*100:.1f} percentage points")

half_a.to_csv("half_a_results.csv", index=False)
half_b.to_csv("half_b_results.csv", index=False)
