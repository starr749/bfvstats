from collections import OrderedDict
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot
import json, sys


def read_json():
    with open('stats.json') as json_file:
        json_data = json.load(json_file)
    return json_data


def normalize(data_list, normal_max=1):
    normal_list = []
    for x in data_list:
        normal_list.append((((x - min(data_list))) / (max(data_list) - min(data_list))) * normal_max)
    return normal_list


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
        score_min.append(float(stats['Score/min']))
        kd.append(float(stats['K/D']))
        kills_min.append(float(stats['Kills/min']))
        win_percent.append(float(stats['Win %'].strip('%')) / 100)

    print(dates, score_min, kd, kills_min, win_percent)

    # check if we want to normalize everything 0-100 is most interesting
    if len(sys.argv) > 1 and sys.argv[1] == 'normalize':
        score_min_normal = normalize(score_min, 100)
        kd = normalize(kd, 100)
        kills_min = normalize(kills_min, 100)
        win_percent = normalize(win_percent, 100)

    # If we're not normalizing everything,
    # We want to normalize the data score/min data to fit between 1 and 0
    else:
        score_min_normal = normalize(score_min)

    score_trace = go.Scatter(
        x=dates,
        y=score_min_normal,
        mode='lines',
        name='Score / Min (Normalized)'
    )

    kd_trace = go.Scatter(
        x=dates,
        y=kd,
        mode='lines',
        name='K/D'
    )

    kills_trace = go.Scatter(
        x=dates,
        y=kills_min,
        mode='lines',
        name='Kills / Min'
    )

    win_trace = go.Scatter(
        x=dates,
        y=win_percent,
        mode='lines',
        name='Win %'
    )

    graph_data = [score_trace, kd_trace, kills_trace, win_trace]

    plot(graph_data, filename='bfv-stat.html')


if __name__ == "__main__":
    main()
