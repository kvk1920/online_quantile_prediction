import argparse
from . import commons, metrics
import matplotlib.pyplot as plt
import numpy as np


colors = [
    'red',
    'green',
    'blue',
    'magenta',
    'indigo',
    'orange',
]


def show_quantiles(argv):
    assert len(argv) in (3, 4), 'usage: visualize quantiles <data> <result> <output> <layout(optional)>'
    data = np.loadtxt(commons.INPUT_PATH / f'{argv[0]}.csv', delimiter=',')
    results = np.loadtxt(commons.OUTPUT_PATH / f'{argv[1]}.csv', delimiter=',')
    plt.figure(figsize=(16, 16))
    for i, q in enumerate(commons.quantiles):
        y = data[:, -1]
        pred_y = results[:, i]
        is_less = y < pred_y
        q_error = is_less.cumsum() / (1 + np.arange(len(y)))
        plt.plot(q_error, label=f'q = {q}')
        plt.axhline(q, c='r', ls='--')
    if 4 == len(argv):
        prev_border = 0
        layout = np.loadtxt(commons.INPUT_PATH / f'{argv[3]}.csv', delimiter=',')
        for t, l in zip(layout[0], layout[1]):
            plt.axvspan(prev_border, prev_border + l - 1, alpha=.5, color=colors[int(t)])
            prev_border += l
    plt.title('quantiles')
    plt.xlabel('time')
    plt.legend()
    plt.savefig(commons.IMAGES_PATH / f'{argv[2]}.png')


def show_crps(argv):
    assert len(argv) in (3, 4), 'usage: visualize crps <data> <result> <output> <layout(optional)>'
    data = np.loadtxt(commons.INPUT_PATH / f'{argv[0]}.csv', delimiter=',')
    results = np.loadtxt(commons.OUTPUT_PATH / f'{argv[1]}.csv', delimiter=',')
    plt.figure(figsize=(16, 16))
    crps_value = np.zeros(len(data))
    for i in range(len(data)):
        crps_value[i] = metrics.crps(results[i], data[i, -1])
    plt.plot(crps_value.cumsum() / (1 + np.arange(len(data))))
    print('mean crps:', crps_value.mean())
    plt.xlabel('time')
    plt.ylabel('crps accumulated mean')
    if 4 == len(argv):
        prev_border = 0
        layout = np.loadtxt(commons.INPUT_PATH / f'{argv[3]}.csv', delimiter=',')
        for t, l in zip(layout[0], layout[1]):
            plt.axvspan(prev_border, prev_border + l - 1, alpha=.5, color=colors[int(t)])
            prev_border += l
    plt.title('crps')
    plt.legend()
    plt.savefig(commons.IMAGES_PATH / f'{argv[2]}.png')
