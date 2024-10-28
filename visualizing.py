import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.patheffects as pe
from matplotlib import font_manager
import seaborn as sns
import os
from matplotlib.ticker import FuncFormatter

colors = {
    "very_confident": "#2E4465",
    "somewhat_confident": "#3C608A",
    "no_opinion": "#D3D8D6",
    "not_confident": "#5E233B",   
    "not_confident_at_all": "#321420" 
}

import matplotlib
from matplotlib import font_manager

def setup_custom_fonts():
    """
    Registers custom fonts and sets the default font family for matplotlib charts.
    """
    fonts = [
        ('../fonts/StyreneA-Black.otf', 'StyreneABlack'),
        ('../fonts/StyreneA-Medium.otf', 'StyreneAMedium'),
        ('../fonts/StyreneA-Regular.otf', 'StyreneARegular')
    ]

    for font_path, font_name in fonts:
        fe = font_manager.FontEntry(fname=font_path, name=font_name)
        font_manager.fontManager.ttflist.insert(0, fe)  # Insert at the beginning of the list

    # Set the default font family to 'StyreneARegular' or another preferred font
    matplotlib.rcParams['font.family'] = 'StyreneARegular'

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


def plot_question(df, question, question_text, sort=True):
    # this should handle most of our plots
    # it could eventually be used to plot the confidence questions
    # current problems that could be fixed some day: bar/group spacing, colors.
    if sort:
        df = df.sort_values(by=df.columns[0],ascending=False)

    matrix = len(df.columns) > 1
    sums_to_1 = all(abs(df.sum(axis=1) - 1) < 0.1)
    legend = False
    stacked = False
    # tall = False
    if matrix:
        legend = True
        if sums_to_1:
            stacked = True

    if matrix and not stacked:
        height = len(df)
    else:
        height = len(df) * 0.5

    ax = df.plot(kind='barh', stacked=stacked, figsize=(10, height), title=f"{question}: {question_text}", legend=legend)
    ax.invert_yaxis()
    
    if stacked:
        ax.set_xlim([0, 1])
    
    if legend:
        ax.legend(bbox_to_anchor=(0, -.08), loc='upper left')

    for i, patch in enumerate(ax.patches):
        # Find the width and position of each bar segment
        width = patch.get_width()
        if stacked:
            x = patch.get_x() + width / 2
        else:
            xlim = ax.get_xlim()
            x = (xlim[1] - xlim[0]) * 0.05
        y = patch.get_y() + patch.get_height() / 2
        
        # Annotate the bar with the percentage (multiply by 100 and round for display)
        ax.annotate(f'{width * 100:.0f}%', (x, y), ha='center', va='center',
                    color='white',
                    path_effects=[pe.withStroke(linewidth=1, foreground="gray")])

    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))  # xmax=1 because your data is in proportion (0 to 1)

    plt.show()

    return ax

def dotplot2(df, file_name, start_tick_title, end_tick_title, xlabel,title=None,plot_type=None,x_axis_limit = 1):
    categories = df.index
    n = len(categories)

    fig, ax = plt.subplots(figsize=(10, n*.7))

    sns.set_style('ticks')

    setup_custom_fonts()

    delta = 0.2
    y = np.linspace(-delta, delta, n)
    # colors = ['blue', 'green', 'red']
    # colors = ['#3C608A', '#3C608A', '#3C608A']
    blue = '#3C608A'
    lightgray = '#d3d8d6'
    bpc_darkgray = '#333638'
    red = '#e43e47'
    lightblue = '#3687e7'
    mustard = '#D4AD50'
    purple = '#5E233B'

    color1 = red if start_tick_title == "Republicans" else purple 
    color2 = lightblue if end_tick_title == "Democrats" else blue


    x_label_offset = 0.015 * x_axis_limit
    y_label_offset = -0.13

    ms = 5 # markersize

    ylabel_fontsize = 12
    xlabel_fontsize = 12
    data_label_fontsize = 11
    xtick_label_fontsize = 11
    title_fontsize = 13
    head_width=0.035
    head_length=0.01

    for j, category in enumerate(categories):

        start = df[df.columns[0]].loc[category]
        end = df[df.columns[1]].loc[category]

        if plot_type:
            # lines (not arrow)
            ax.plot([start, end], [y[j], y[j]], color=lightgray, zorder=2, linewidth=4)
        else:
            # arrows
            ax.arrow(start, y[j], end - start-.01, 0, 
                    head_width=head_width, head_length=head_length, fc=color1, ec=color1,
                    width=.01,
                    overhang=0, length_includes_head=True, zorder=100)
            
        # Add starting dot
        ax.plot(start, y[j], 'o', color=color1, zorder=100, markersize=ms)

        # Add end dot
        ax.plot(end, y[j], 'o', color=color2, zorder=100, markersize=ms, clip_on=False)

        percent_marker = '%' if j == 0 else ''
        start_label = f'{round(start * 100)}{percent_marker}'
        end_label = f'{round(end * 100)}{percent_marker}'

        sign = 1 if start < end else -1

        ax.text(start - x_label_offset*sign, y[j], start_label, ha='right' if start < end else 'left', va='center', color=bpc_darkgray, fontsize=data_label_fontsize)
        ax.text(end + x_label_offset*sign, y[j], end_label, ha='left' if start < end else 'right', va='center', color=bpc_darkgray, fontsize=data_label_fontsize)


        if j == 0:
            # ax.text(start - h_label_offset, y[j], "'22", ha='right', va='center', color='black')
            # ax.text(end + h_label_offset, y[j], "'24", ha='left', va='center', color='black')
            offset = (-.06 * x_axis_limit) if x_axis_limit!= 1 else 0
            ax.text(start + (offset*sign), y[j]+ y_label_offset, start_tick_title, ha='center', va='center', color=color1, fontsize=data_label_fontsize, fontname='StyreneAMedium')
            ax.text(end + (-1*offset*sign), y[j]+ y_label_offset, end_tick_title, ha='center', va='center', color=color2, fontsize=data_label_fontsize, fontname='StyreneAMedium')
            
            ax.plot([start, start], [y[j]+y_label_offset*.3, y[j]+y_label_offset*.7], color=color1, zorder=0)
            ax.plot([end, end], [y[j]+y_label_offset*.3, y[j]+y_label_offset*.7], color=color2, zorder=0)


    # # Setting the y-axis labels
    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=ylabel_fontsize, fontname='StyreneAMedium', color=bpc_darkgray)

    # ax.set_yticklabels(['All jurisdictions', 'County-equivalents', '20 most populous\ncounties'],
    #                 fontname='StyreneAMedium', color=darkgray, fontsize=11.5)
    ax.set_ylim([delta*1.5, -delta*2])
    ax.grid(False)


    # # Setting the x-axis label
    ax.set_xlabel(xlabel, fontsize=xlabel_fontsize, fontname='StyreneAMedium')
    # ax.set_xticks(np.linspace(0, 1, 11))
    # ax.set_xticklabels([f'{i}%' for i in range(0, 101, 10)], fontsize=label_fontsize)

    if x_axis_limit and x_axis_limit != 1:
          ax.set_xlim([0, x_axis_limit])
          ax.set_xticks(np.arange(0.1, x_axis_limit + 0.1, 0.1))
          ax.set_xticklabels([f'{int(tick * 100)}%' for tick in np.arange(0.1, x_axis_limit + 0.1, 0.1)], fontsize=xtick_label_fontsize)
    else:
        ax.set_xlim([0, 1])
        ax.set_xticks(np.linspace(0, 1, 5))
        ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'], fontsize=xtick_label_fontsize)
    # ax.set_xticks(np.linspace(0, 1, 2))
    # ax.set_xticklabels(["0%", "100%"])
    sns.despine(left=True)

    # Remove y-axis
    # ax.yaxis.set_visible(False)
    ax.tick_params(axis='y', length=0)
    
    
    ax.spines['bottom'].set_color(bpc_darkgray)
    ax.spines['bottom'].set_linewidth(1)
    ax.tick_params(axis='x', color=bpc_darkgray, width=1)

    # # Remove grid lines
    ax.grid(False)

    # # Remove the background
    ax.set_facecolor('white')

    # # Display the plot
    # plt.title(title, fontname='StyreneABlack', fontsize=title_fontsize)

    plt.savefig(f'{file_name}', dpi=300, bbox_inches='tight')

    plt.show()