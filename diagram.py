# Re-import necessary libraries due to kernel reset
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

# title, sum of squares, time, iso time
data = [
    ('Number of Nodes', 8.79e+08, 0.08, 77.25),
    ('Number of Edges', 8.76e+08, 0.56, 79.39),
    ('Degree Distribution', 8.64e+08, 0.82, 75.65),
    ('Elemental Composition', 1.11e+08, 0.33, 14.37),
    ('Bond Type Distribution', 7.62e+08, 1.14, 57.89),
    ('Clustering Coefficients', 8.68e+08, 1.91, 79.13),
    ('WL (1)', 8.26e+07, 2.52, 11.39),
    ('WL (2)', 8.26e+07, 3.81, 12.16),
    ('Isomorphism', 8.26e+07, None, None),  # 83.99
]

# separate columns
names, sums_of_squares, times, iso_times = zip(*data)

# colors
color1 = mcolors.to_rgba("#1F306E")  # primary
color2 = mcolors.to_rgba("#F5487F")  # secondary 1
color3 = mcolors.to_rgba("#8F3B76")  # secondary 2

# Create a figure and axis for horizontal bar chart
fig, ax1 = plt.subplots(figsize=(12, 7))

# First y-axis for sum of squares (horizontal bars)
ax1.barh(names, sums_of_squares, label='Sum of Squares', alpha=0.8, color=color2,
         edgecolor="black")
ax1.set_ylabel('Invariant', fontsize=14)
ax1.set_xlabel('Sum of Squares', color=color1, fontsize=14)
ax1.tick_params(axis='x', labelcolor='black')
ax1.set_yticklabels(names, fontsize=12)

# Create a second x-axis for computation time (excluding "Ground Truth")
ax2 = ax1.twiny()
ax2.scatter(times, names, label='Invariant Computation Time',
            color=color1, s=120, zorder=5)
ax2.scatter(iso_times, names, label='Isomorphism Computation Time',
            color=color3, s=120, zorder=5)
ax2.set_xlabel('Computation Time (s)', color=color2, fontsize=14)
ax2.tick_params(axis='x', labelcolor='black')

# Add a grid for clarity
ax1.grid(True, linestyle="--", alpha=0.5)

# Title and layout
plt.title('Costs and Benefits of Invariants', fontsize=16, pad=20)
fig.tight_layout()
plt.savefig("diagram.png", transparent=True)
