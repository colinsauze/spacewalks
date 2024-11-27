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


# main code

# https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open("eva-data.json", "r")
output_file = open("eva-data.csv", "w")
graph_file = "myplot.png"

# read the data from the JSON file
eva_data = read_json_to_dataframe(input_file)

# convert and export to CSV for further analysis
write_dataframe_to_csv(eva_data, output_file)


# Calculate cumulative time spent in space over years
eva_data["duration_hours"] = (
    eva_data["duration"].str.split(":").apply(
        lambda x: int(x[0]) + int(x[1]) / 60)
)
eva_data["cumulative_time"] = eva_data["duration_hours"].cumsum()

# Plot the cumulative time
plt.plot(eva_data["date"], eva_data["cumulative_time"], "ko-")
plt.xlabel("Year")
plt.ylabel("Total time spent in space to date (hours)")
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
