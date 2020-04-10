import matplotlib.pyplot as plt
def plot_result(coords, visitedMatrix, path_to_save, name):
    X = [x[0] for x in coords]
    Y = [x[1] for x in coords]
    x_to_plot = []
    y_to_plot = []
    for i in range(len(visitedMatrix)):
        x_to_plot.append(X[visitedMatrix[i]])
        y_to_plot.append(Y[visitedMatrix[i]])

    x_to_plot.append(X[visitedMatrix[0]])
    y_to_plot.append(Y[visitedMatrix[0]])

    for i, txt in enumerate(visitedMatrix):
        plt.scatter(x_to_plot[i], y_to_plot[i])
        plt.text(x_to_plot[i], y_to_plot[i], str(txt), fontsize=9)
    plt.scatter(X, Y)
    plt.plot(x_to_plot, y_to_plot)
    plt.savefig(path_to_save)
    plt.show()