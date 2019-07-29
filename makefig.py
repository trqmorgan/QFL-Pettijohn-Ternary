import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.path import Path
import matplotlib.patches as patches


def data_prep (data, quartz, feldspar, lithic):
    if type(quartz) == str:
        top = data[quartz]
        left = data[feldspar]
        right = data[lithic]
    else:
        top = quartz
        left = feldspar
        right = lithic

    stacked_data = np.vstack((top, left, right))
    summed_rows = np.sum(stacked_data[0:], axis=0)
    stacked_data = np.vstack((stacked_data, summed_rows))
    Q = (stacked_data[0] / stacked_data[3] * 100)
    F = (stacked_data[1] / stacked_data[3] * 100)
    y = Q / 100
    x = (1 - F / 100) - (y / 2)
    return x, y


def plot_qfl(data, quartz, feldspar, lithic, matrix, color, size):

    x, y = data_prep(data, quartz, feldspar, lithic)
    matrix = data[matrix]
    c1 = ['Quartz arenite', (0.5, 0.9),(0.525, 0.95), (0.5, 1), (0.475, 0.95), (0.5, 0.9)]
    c2 = ['Sublitharenite', (0.5, 0.5),(0.625, 0.75), (0.525, 0.95), (0.5, 0.9), (0.5, 0.5)]
    c3 = ['Lithic arenite', (1, 0),(0.625, 0.75), (0.5, 0.5), (0.5, 0.0), (1, 0)]
    c4 = ['Arkosic arenite', (0, 0),(0.375, 0.75), (0.5, 0.5), (0.5, 0.0), (0, 0)]
    c5 = ['Subarkose', (0.5, 0.5),(0.375, 0.75), (0.475, 0.95), (0.5, 0.9), (0.5, 0.5)]

    fig, ax = plt.subplots()
    ax.text(0.62, 0.95, "Quartz arenite", ha="center", va="center", rotation=0, size=8)
    ax.text(0.7, 0.8, "Sublitharenitee", ha="center", va="center", rotation=0, size=8)
    ax.text(0.75, 0.05, 'Lithic arenite', ha="center", va="center", rotation=0, size=8)
    ax.text(0.3, 0.8, "Subarkose", ha="center", va="center", rotation=0, size=8)
    ax.text(0.25, 0.05, 'Arkosic arenite', ha="center", va="center", rotation=0, size=8)
    ax.scatter(x, y, color=color, s=size, edgecolor='k', zorder=10)
    classifications = [c1, c2, c3, c4, c5]

    for i in range(len(classifications)):
        polygon = classifications[i][1:]
        path = Path(polygon)
        index = path.contains_points(np.column_stack((x, y)))
        if sum(index) > 0:
            ax.add_patch(patches.PathPatch(path, alpha=0.1, facecolor='green', lw=0, zorder=0))
        patch = patches.PathPatch(path, color=None, facecolor=None, fill=False, lw=1.5, zorder=1)
        ax.add_patch(patch)

    for i in range(len(classifications)):
        polygon = classifications[i][1:]
        path = Path(polygon)
        index = path.contains_points(np.column_stack((x, y)))

        for j in range(len(index)):
            if index[j] == True:
                data.loc[j, "Pettijohn"] = classifications[i][0]
                if matrix[j] > 15 and  matrix[j] < 75:
                    if classifications[i][0] == 'Sublith Arenite' or classifications[i][0] == 'Lith Arenite':
                        data.loc[j, "Pettijohn"] = 'Lithic Wacke'
                    elif classifications[i][0] == 'Sub Arkose' or classifications[i][0] == 'Arkosic Arenite':
                        data.loc[j, "Pettijohn"] = 'Arkpsic Wacke'
                    elif classifications[i][0] == 'Quartz Arenite':
                         data.loc[j, "Pettijohn"] = 'Quartz Wacke'
                elif matrix[j] > 75:
                    data.loc[j, "Pettijohn"] = 'Mudrock'
            else:
                pass

    ax.set_frame_on(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.text(-0.02, -0.04, "Feldspar", ha="center", va="center", rotation=0, size=12)
    ax.text(1.02, -0.04, "Lithics", ha="center", va="center", rotation=0, size=12)
    ax.text(0.5, 1.007, "Quartz", ha="center", va="center", rotation=0, size=12)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return data, fig


if __name__ == "__main__":
    data = pd.read_csv('data.csv')
    print(data.columns.values)
    Q = data['Qm']+data['Qmu']+data['Qp']
    F = data['Plag']+data['Afsp']
    L = data['Lf']
    classified_data, plot = plot_qfl(data, quartz=Q, feldspar=F, lithic=L, matrix='PM+Cem', color='r', size=15)
    plt.show()

