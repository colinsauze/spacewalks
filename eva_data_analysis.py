import sys
import matplotlib.pyplot as plt
import pandas as pd


def read_json_to_dataframe(input_file):
    """
    Read the data from a JSON file into a Pandas dataframe.
    Clean the data by removing any incomplete rows and sort by date

    Args:
        input_file (str): The path to the JSON file.

    Returns:
        eva_df (pd.DataFrame): The cleaned and sorted data as a dataframe
    """

    # Read the data from a JSON file into a Pandas dataframe
    eva_df = pd.read_json(input_file, convert_dates=["date"])
    eva_df["eva"] = eva_df["eva"].astype(float)

    # Clean the data by removing any incomplete rows and sort by date
    eva_df.dropna(axis=0, inplace=True)
    eva_df.sort_values("date", inplace=True)
    return eva_df


def write_dataframe_to_csv(df, output_file):
    """
    Write the dataframe to a CSV file.

    Args:
        df (pd.DataFrame): The input dataframe.
        output_file (str): The path to the output CSV file.

    Returns:
        None
    """
    print(f"Saving to CSV file {output_file}")
    df.to_csv(output_file, index=False)

def plot_cumulative_time_in_space(df, graph_file):
    """
    Plot the cumulative time spent in space over years

    Convert the duration column from strings to number of hours
    Calculate cumulative sum of durations
    Generate a plot of cumulative time spent in space over years and
    save it to the specified location

    Args:
        df (pd.DataFrame): The input dataframe.
        graph_file (str): The path to the output graph file.

    Returns:
        None
    """
    df = add_duration_hours_variable(df)

    df["cumulative_time"] = df["duration_hours"].cumsum()

    # Plot the cumulative time
    plt.plot(df["date"], df["cumulative_time"], "ko-")
    plt.xlabel("Year")
    plt.ylabel("Total time spent in space to date (hours)")
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()

def text_to_duration(duration):
    """
    Convert a text format duration "HH:MM" to duration in hours

    Args:
       duration (str): The duration in HH:MM
    
    Returns:
       duration_hours (float): The duration in hours
    """
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/60
    return duration_hours


def add_duration_hours_variable(df):
    """
    Add duration in hours (duration_hours) variable to the dataset

    Args:
        df (pd.DataFame): The input dataframe

    Returns:
        df_copy (pd.DataFrame): A copy of the df_ with the new duration_hours variable added
    """
    df_copy = df.copy()
    df_copy['duration_hours'] = df_copy["duration"].apply(text_to_duration)
    return df_copy

if __name__ == "__main__":

    if len(sys.argv) < 3:
        # less than 3 command line arguments, assuming we use default file names
        # https://data.nasa.gov/resource/eva.json (with modifications)
        input_file = open("eva-data.json", "r")
        output_file = open("eva-data.csv", "w")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    graph_file = "cumulative_eva_graph.png"

    # read the data from the JSON file
    eva_data = read_json_to_dataframe(input_file)

    # convert and export to CSV for further analysis
    write_dataframe_to_csv(eva_data, output_file)

    plot_cumulative_time_in_space(eva_data, graph_file)
