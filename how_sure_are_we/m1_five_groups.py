"""
M1 -- Split it up.

Take the 150 scored results, split them into 5 groups of 30, score each
group's accuracy on its own, and note the lowest and highest. That
spread is the "wobble" -- proof that a single accuracy number depends
partly on luck of the draw, not just on how good the model is.
"""

import pandas as pd
import numpy as np

# Fixed seed = reproducible groups. Anyone re-running this script gets
# the exact same 5 groups.
SEED = 42
N_GROUPS = 5
GROUP_SIZE = 30

df = pd.read_csv("results_150_clean.csv")
assert len(df) == 150, f"expected 150 rows, got {len(df)}"

rng = np.random.default_rng(SEED)

# Shuffle all 150 row positions, then slice into 5 equal chunks of 30.
indices = rng.permutation(len(df))
groups = np.array_split(indices, N_GROUPS)

accuracies = []
for i, group_idx in enumerate(groups, start=1):
    group = df.iloc[group_idx]
    acc = group["correct"].mean()
    accuracies.append(acc)
    print(f"Group {i}: {group['correct'].sum()}/{GROUP_SIZE} = {acc:.4f} ({acc*100:.1f}%)")
    group.to_csv(f"group_{i}_results.csv", index=False)

accuracies = np.array(accuracies)
print()
print(f"Lowest:  {accuracies.min()*100:.1f}%")
print(f"Highest: {accuracies.max()*100:.1f}%")
print(f"Average: {accuracies.mean()*100:.1f}%")
print(f"Spread (highest - lowest): {(accuracies.max() - accuracies.min())*100:.1f} percentage points")
