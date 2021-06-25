import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline
import numpy as np
import os


class Plot():

    def __init__(self, cam, phastcon, plot_path, subset_index):
        self.cam = cam[subset_index, :]
        self.phastcon = phastcon ## list, value is phastcon scores
        self.plot_path = plot_path
        
    def plot(self):

        for i in range(self.cam.shape[0]):
            x = np.linspace(0, 999, len(self.cam[i]))
            y = self.cam[i]
            spl = InterpolatedUnivariateSpline(x, y)
            plt.figure(i)
            plt.plot(x, y, 'ro', ms=5)
            xs = np.linspace(0, 999, 1000)
            plt.plot(xs, spl(xs), 'g', lw=3, alpha=0.7)

            x = np.linspace(0, 999, len(self.phastcon[i]))
            y = self.phastcon[i]
            spl = InterpolatedUnivariateSpline(x, y)
            plt.plot(xs, spl(xs), 'b', lw=3, alpha=0.7)
            
            plot_name = "cam_phastcon_"+str(i) + ".pdf"
            plt.savefig(os.path.join(self.plot_path, plot_name))