
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Define the Pantone colors using their RGB hex codes
colors = {
    "regular": "#3C608A",  # Pantone 653
    "reverse": "#E43E47",  # Pantone 71
    "random": "#D3D8D6",   # Pantone 427
    "deviation": "#333638" # Pantone 426 (optional)
}


# Add percentage labels above the bars
def add_labels(rects,ax):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def display_confidence_split(q_df,title):
    
    # Extract data for plotting
    labels = q_df.index.tolist()  # Assuming row indices represent the confidence levels
    regular_order = q_df["regular order"].apply(lambda x: float(x.strip('%'))).tolist()
    reverse_order = q_df["reverse order"].apply(lambda x: float(x.strip('%'))).tolist()
    random_order = q_df["random order"].apply(lambda x: float(x.strip('%'))).tolist()

    # Set up the positions for the bars
    x = np.arange(len(labels))  # the label locations
    width = 0.25  # the width of the bars

    # Create a single grouped bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    rects1 = ax.bar(x - width, regular_order, width, label='Regular Order', color=colors["regular"])
    rects2 = ax.bar(x, reverse_order, width, label='Reverse Order', color=colors["reverse"])
    rects3 = ax.bar(x + width, random_order, width, label='Random Order', color=colors["random"])

    # Add labels and customizations
    ax.set_xlabel('Confidence Level')
    ax.set_ylabel('Percentage')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    # Add a legend to distinguish between Regular, Reverse, and Random Orders
    ax.legend()

    add_labels(rects1,ax)
    add_labels(rects2,ax)
    add_labels(rects3,ax)

    # Adjust the layout to prevent overlap
    plt.tight_layout()

    # Show the plot
    plt.show()
