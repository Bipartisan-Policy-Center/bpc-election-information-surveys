
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

colors = {
    "very_confident": "#2E4465",
    "somewhat_confident": "#3C608A",
    "no_opinion": "#D3D8D6",
    "not_confident": "#5E233B",   
    "not_confident_at_all": "#321420" 
}

def plot_overall_confidence(df):
    # Extract the data from df
    categories = df.columns  # The different vote levels
    # confidence_levels = df.index  # The confidence categories

    # Set up the data for plotting
    very_confident = df.loc["Very confident"] *100#.values
    somewhat_confident = df.loc["Somewhat confident"] *100#.values
    not_confident = df.loc["Not to confident"] *100#.values
    no_opinion = df.loc["Don't know/ No opinion"]*100 #.values
    not_confident_at_all = df.loc["Not confident at all"]*100 #.values

    # Set up the plot for horizontal bars
    fig, ax = plt.subplots(figsize=(12, 3))

    # Y positions for the bars
    y_pos = np.arange(len(categories))

    # Initialize the bottom array for stacking
    bottom = np.zeros(len(categories))

    # Plot each confidence level on top of the previous one
    rects1 = ax.barh(y_pos, very_confident, height=0.8, color=colors["very_confident"], label='Very Confident')
    bottom += very_confident

    rects2 = ax.barh(y_pos, somewhat_confident, height=0.8, color=colors["somewhat_confident"], label='Somewhat Confident', left=bottom)
    bottom += somewhat_confident

    rects3 = ax.barh(y_pos, no_opinion, height=0.8, color=colors["no_opinion"], label='No Opinion', left=bottom)
    bottom += no_opinion

    rects4 = ax.barh(y_pos, not_confident, height=0.8, color=colors["not_confident"], label='Not Confident', left=bottom)
    bottom += not_confident

    rects5 = ax.barh(y_pos, not_confident_at_all, height=0.8, color=colors["not_confident_at_all"], label='Not Confident at All', left=bottom)

    # Add data labels with percentage formatting
    ax.bar_label(rects1, label_type='center', color="white", fmt='%.1f%%')
    ax.bar_label(rects2, label_type='center', color="white", fmt='%.1f%%')
    ax.bar_label(rects3, label_type='center', fmt='%.1f%%')
    ax.bar_label(rects4, label_type='center', color="white", fmt='%.1f%%')
    ax.bar_label(rects5, label_type='center', color="white", fmt='%.1f%%')

    # Customizations
    ax.set_yticks(y_pos)
    ax.set_yticklabels(["your vote","votes in your community","votes in your state","votes in the country"])
    ax.set_xlabel('Percentage')
    ax.set_title('Overall confidence (registered voters only)')

    # Only display confidence levels in the legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Remove duplicates
    ax.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1.35, 1), title="Confidence Levels")

    # Adjust layout to avoid clipping of the legend
    plt.tight_layout()

    # Display the plot
    plt.gca().invert_yaxis()
    plt.show()



def plot_split_sample(all_dfs, q_codebook):

    for i, q_df in enumerate(all_dfs):

        # Data for regular, reverse, and random orders from all_dfs[0], dropping "deviation" column
        df = q_df.drop(columns=['deviation'])

        # Orders to plot
        orders = df.columns

        # Set up the plot for horizontal bars
        fig, ax = plt.subplots(figsize=(12, 3))

        # Y positions for the three bars
        y_pos = np.arange(len(orders))

        # Function to plot stacked bars
        def plot_stacked_bars(df):
            # Extract data as percentages
            very_confident = df.loc["Very confident"] * 100
            somewhat_confident = df.loc["Somewhat confident"] * 100
            not_confident = df.loc["Not to confident"] * 100
            not_confident_at_all = df.loc["Not confident at all"] * 100
            no_opinion = df.loc["Don't know/ No opinion"] * 100

            # Initialize the bottom array for stacking
            bottom = np.zeros(len(orders))

            # Plot each confidence level on top of the previous one
            rects1 = ax.barh(y_pos, very_confident, height=0.5, color=colors["very_confident"], label='Very Confident')
            bottom += very_confident

            rects2 = ax.barh(y_pos, somewhat_confident, height=0.5, color=colors["somewhat_confident"], label='Somewhat Confident', left=bottom)
            bottom += somewhat_confident

            rects3 = ax.barh(y_pos, no_opinion, height=0.5, color=colors["no_opinion"], label='No Opinion', left=bottom)
            bottom += no_opinion

            rects4 = ax.barh(y_pos, not_confident, height=0.5, color=colors["not_confident"], label='Not Confident', left=bottom)
            bottom += not_confident

            rects5 = ax.barh(y_pos, not_confident_at_all, height=0.5, color=colors["not_confident_at_all"], label='Not Confident at All', left=bottom)

            # Add data labels with percentage formatting
            ax.bar_label(rects1, label_type='center',color="white", fmt='%.1f%%')
            ax.bar_label(rects2, label_type='center',color="white", fmt='%.1f%%')
            ax.bar_label(rects3, label_type='center', color="black",fmt='%.1f%%')
            ax.bar_label(rects4, label_type='center',color="white", fmt='%.1f%%')
            ax.bar_label(rects5, label_type='center',color="white", fmt='%.1f%%')

        # Now, directly plot the DataFrame
        plot_stacked_bars(df)

        # Customizations
        ax.set_yticks(y_pos)
        ax.set_yticklabels(orders)
        ax.set_xlabel('Percentage')
        ax.set_title(q_codebook[f"BPC{20+i}a"])

        # Only display confidence levels in the legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))  # Remove duplicates
        ax.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1.23, 1), title="Confidence Levels")

    # Adjust layout to avoid clipping of the legend
    plt.tight_layout()

    # Display the plot
    plt.show()