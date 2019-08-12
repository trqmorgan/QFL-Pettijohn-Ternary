import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.path import Path
import matplotlib.patches as patches


def data_prep (data, top, left, right):
    if type(top) == str:
        top = data[top]
        left = data[left]
        right = data[right]
    else:
        top = top
        left = left
        right = right

    stacked_data = np.vstack((top, left, right))
    summed_rows = np.sum(stacked_data[0:], axis=0)
    stacked_data = np.vstack((stacked_data, summed_rows))
    T = (stacked_data[0] / stacked_data[3] * 100)
    L = (stacked_data[1] / stacked_data[3] * 100)
    y = T / 100
    x = (1 - L / 100) - (y / 2)
    return x, y


def field_boundaries(scheme):
    if scheme == 'Pettijohn_1977':
        c1 = ['Quartz arenite', (0.5, 0.9), (0.525, 0.95), (0.5, 1), (0.475, 0.95), (0.5, 0.9)]
        c2 = ['Sublitharenite', (0.5, 0.5), (0.625, 0.75), (0.525, 0.95), (0.5, 0.9), (0.5, 0.5)]
        c3 = ['Lithic arenite', (1, 0), (0.625, 0.75), (0.5, 0.5), (0.5, 0.0), (1, 0)]
        c4 = ['Arkosic arenite', (0, 0), (0.375, 0.75), (0.5, 0.5), (0.5, 0.0), (0, 0)]
        c5 = ['Subarkose', (0.5, 0.5), (0.375, 0.75), (0.475, 0.95), (0.5, 0.9), (0.5, 0.5)]
        classifications = [c1, c2, c3, c4, c5]
        # label, x, y, rotation
        l1 = ["Quartz arenite", 0.62, 0.95, 0]
        l2 = ["Sublitharenite", 0.7, 0.8, 0]
        l3 = ["Lithic arenite", 0.75, 0.05, 0]
        l4 = ["Subarkose", 0.3, 0.8, 0]
        l5 = ["Arkosic arenite", 0.25, 0.05, 0]
        labels = [l1, l2, l3, l4, l5]
    elif scheme == 'Dickinson_1983':
        c1 = ['basement uplift', (0, 0), (0.15, 0), (0.341992, 0.4985), (0.266412, 0.532842), (0, 0)]
        c2 = ['transitional continental', (0.341992, 0.4985), (0.266412, 0.532842), (0.403822, 0.807654), (0.45, 0.779), (0.341992, 0.4985)]
        c3 = ['craton interior', (0.45, 0.779), (0.403822, 0.807654), (0.5, 1), (0.52, 0.96), (0.45, 0.779)]
        c4 = ['recycled orogen', (0.886, 0.228), (0.341992, 0.4985), (0.52, 0.96), (0.886, 0.228)]
        c5 = ['dissected arcs', (0.341992, 0.4985), (0.701343, 0.319926), (0.215664, 0.170566),
              (0.341992, 0.4985)]
        c6 = ['transitional arc', (0.701343, 0.319926), (0.863323, 0.239235), (0.5, 0), (0.15, 0),
              (0.215664, 0.170566),
              (0.701343, 0.319926)]
        c7 = ['undissected arc', (0.863323, 0.239235), (0.886, 0.228), (1, 0), (0.5, 0), (0.863323, 0.2392359)]
        classifications = [c1, c2, c3, c4, c5, c6, c7]
        l1 = ["basement uplift", 0.165, 0.2, 58]
        l2 = ["transitional\n continental", 0.365, 0.65, 60]
        l3 = ["craton interior", 0.38, 0.92, 0]
        l4 = ["recycled orogen", 0.54, 0.62, 0]
        l5 = ["dissected arcs", 0.41, 0.35, 0]
        l6 = ["transitional arc", 0.45, 0.15, 0]
        l7 = ["undissected arc", 0.8, 0.05, 0]
        labels = [l1, l2, l3, l4, l5, l6, l7]
    elif scheme == 'blank':
        c1 = ['triangle', (0, 0), (0.5, 1), (1, 0), (0, 0)]
        classifications = [c1]
        labels = []

    return classifications, labels


def plot_qfl(data, top, left, right, matrix, plottype, toplab, leftlab, rightlab, color, size,):
    list_valid_types = ['Pettijohn_1977', 'Dickinson_1983', 'blank']
    if plottype not in list_valid_types:
        raise ValueError("Plot type not recognised, valid types are Pettijohn_1977 and Dickinson_1983")

    x, y = data_prep(data, top, left, right)
    fig, ax = plt.subplots()
    classifications, labs = field_boundaries(plottype)

    for lab in labs:
        ax.text(lab[1], lab[2], lab[0], ha="center", va="center", rotation=lab[3], size=8)

    ax.scatter(x, y, color=color, s=size, edgecolor='k', zorder=10)
    ax.set_frame_on(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    # label the apexes of the triangle
    ax.text(-0.02, -0.04, str(leftlab), ha="center", va="center", rotation=0, size=12)
    ax.text(1.02, -0.04, str(rightlab), ha="center", va="center", rotation=0, size=12)
    ax.text(0.5, 1.05, str(toplab), ha="center", va="center", rotation=0, size=12, zorder=0)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)

    # add the fields for each petrograpic classification
    for i in range(len(classifications)):
        polygon = classifications[i][1:]
        path = Path(polygon)
        # check if every polygon in the loop contains points and color green if true
        index = path.contains_points(np.column_stack((x, y)))
        if plottype != 'blank':
            if sum(index) > 0:
                ax.add_patch(patches.PathPatch(path, alpha=0.1, facecolor='green', lw=0, zorder=0))
        patch = patches.PathPatch(path, color=None, facecolor=None, fill=False, lw=1.5, zorder=1)
        ax.add_patch(patch)
    if plottype != 'blank':
        final_data = data.copy()
        for i in range(len(classifications)):
            polygon = classifications[i][1:]
            path = Path(polygon)
            # check if points are within each polygon
            # the radius argument allows samples plotting on boundary to be classified
            index = path.contains_points(np.column_stack((x, y)), radius=-0.01)
            index1 = path.contains_points(np.column_stack((x, y)), radius=0.01)
            for j in range(len(index)):
                if index[j] or index1[j]:
                    final_data.loc[j, "Pettijohn"] = classifications[i][
                        0]  # add the classification to the column Pettijohn in the datatable
                    if matrix is not None:
                        if matrix[j] > 15 and matrix[j] < 75:  # change the classification if maxtix > 15% and less <75%
                            if classifications[i][0] == 'Sublith Arenite' or classifications[i][0] == 'Lith Arenite':
                                final_data.loc[j, "Pettijohn"] = 'Lithic Wacke'
                            elif classifications[i][0] == 'Sub Arkose' or classifications[i][0] == 'Arkosic Arenite':
                                final_data.loc[j, "Pettijohn"] = 'Arkosic Wacke'
                            elif classifications[i][0] == 'Quartz Arenite':
                                final_data.loc[j, "Pettijohn"] = 'Quartz Wacke'
                        elif matrix[j] > 75:
                            final_data.loc[j, "Pettijohn"] = 'Mudrock'
                else:
                    pass
        final_data = final_data.set_index('Classification')
        return final_data, fig
    return None, fig


if __name__ == "__main__":
    data = pd.read_csv('data.csv')
    print(data.columns.values)
    data_pct = data.set_index('Classification')
    # convert counts to percent
    data_pct = data_pct.div(data_pct.sum(axis=1), axis=0) * 100
    # sum quartz types
    quartz = data_pct['Qm'] + data_pct['Qmu'] + data_pct['Qp']
    fsp = data_pct['Plag'] + data_pct['Afsp']
    lithic = data_pct['Lf']
    # the clay matrix can be None if not present
    matrix = data_pct['PM+Cem']
    # for QFL top = quzrtz, left = feldspar, right = lithic
    # plot type options are 'Dickinson_1983', 'Pettijohn_1977' or 'blank'
    # ToDo add more plot types
    classified_data, plot = plot_qfl(data, top=quartz, left=fsp, right=lithic, matrix=matrix,  plottype='Pettijohn_1977', toplab='Q', leftlab='F', rightlab='L', color='r', size=15,)
    plt.show()
    print(classified_data)

