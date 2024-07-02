import pandas as pd
import matplotlib.pyplot as plt
import sys


if __name__ == '__main__':

    # process comamnd line arguments
    if len(sys.argv) < 3:
        input_file = './eva-data.json'
        output_file = './eva-data.csv'
        print(f'Using default input and output filenames')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print(f'Using custom input and output filenames')

    graph_file = './cumulative_eva_graph.png'

    eva_df = pd.read_json(input_file, convert_dates=['date'])
    # convert the eva number to a numerical type
    eva_df['eva'] = eva_df['eva'].astype(float)

    #drop entries with missing data
    eva_df.dropna(axis=0, inplace=True)

    # ensure the data is sorted by date
    eva_df.sort_values('date', inplace=True)

    eva_df.to_csv(output_file, index=False)

    # calculate the number of hours as a decimal from the hours:minutes data in the json file
    eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
    eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()


    plt.plot(eva_df.date,eva_df.cumulative_time, 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()
