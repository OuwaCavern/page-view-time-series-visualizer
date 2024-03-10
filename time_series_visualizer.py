import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"]).set_index("date")

# Clean data
df = df.drop(df[df["value"].quantile(0.025) > df["value"]].index)
df = df.drop(df[df["value"].quantile(0.975) < df["value"]].index)


def draw_line_plot():
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(20, 5), dpi=100)

    # Plot line plot
    df.plot(ax=ax, color="red")

    # Set labels and title
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image
    fig.savefig('line_plot.png')
    plt.close(fig)

    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_barbymonth = df_bar.resample("m").mean()
    months = ["January",  "February", "March","April", "May", "June", "July", "August", "September", "October", "November", "December"]
    df_barbymonth['months'] = pd.Categorical(df_barbymonth.index.strftime('%B'), categories=months, ordered=True)
    dfp = pd.pivot_table(data=df_barbymonth, index=pd.DatetimeIndex(data=df_barbymonth.index).strftime("%Y"), columns='months', values='value')
    
    # Create a new figure
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Draw bar plot
    dfp.plot(kind='bar', ax=ax)
    ax.set_ylabel('Average Page Views')
    ax.set_xlabel('Years')
    ax.legend(loc="upper left")
    
    # Save image
    fig.savefig('bar_plot.png')
    plt.close(fig)

    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Create a new figure
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # Draw box plots (using Seaborn)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box)
    axes[1] = plt.xlabel('Month')
    axes[1] = plt.xticks(ticks=plt.xticks()[0], labels=month_labels)
    axes[1] = plt.ylabel('Page Views')
    axes[1] = plt.title('Month-wise Box Plot (Seasonality)')
    
    # Save image
    fig.savefig('box_plot.png')
    plt.close(fig)

    return fig