import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def errorPlotOverEpochs(epochsErrors):
    floatErrors = [float(e) for e in epochsErrors]
    epochs = range(1, len(floatErrors) + 1)
    plt.figure()
    plt.plot(epochs, floatErrors, linestyle='-')
    plt.xlabel("Epoch")
    plt.ylabel("Error")
    plt.title("Training Error vs. Epoch")
    plt.grid(True)
    plt.savefig("error_plot.png")
    plt.close()
