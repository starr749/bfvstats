from collections import OrderedDict
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot
import json

def read_json():
    with open('stats.json') as json_file:
        json_data = json.load(json_file)
    return json_data


def main():
    dates = []
    score_min = []
    kd = []
    kills_min = []
    win_percent = []

    json_data = read_json()
    json_data = OrderedDict(sorted(json_data.items(), key=lambda t: datetime.strptime(t[0], '%m/%d/%Y')))

    for date, stats in json_data.items():
        dates.append(date)
        score_min.append(float(stats['Score/min']) / 300)  # Dividing by 300 to get the number small
        kd.append(stats['K/D'])
        kills_min.append(stats['Kills/min'])
        win_percent.append(float(stats['Win %'].strip('%')) / 100)

    print(dates, score_min, kd, kills_min, win_percent)

    score_trace = go.Scatter(
        x = dates,
        y = score_min,
        mode = 'lines',
        name = 'Score / Min ( / 300)'
    )

    kd_trace = go.Scatter(
        x = dates,
        y = kd,
        mode = 'lines',
        name = 'K/D'
    )

    kills_trace = go.Scatter(
        x = dates,
        y = kills_min,
        mode = 'lines',
        name = 'Kills / Min'
    )

    win_trace = go.Scatter(
        x = dates,
        y = win_percent,
        mode = 'lines',
        name = 'Win %'
    )

    graph_data = [score_trace, kd_trace, kills_trace, win_trace]

    plot(graph_data, filename='bfv-stat')

if __name__ == "__main__":
    main()
