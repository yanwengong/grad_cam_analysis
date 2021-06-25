import sys
import os
from utils import Utils2
from data import Data
from phastcon_bed_to_array import Phastcon
from plot_cam_phastcon import Plot

if __name__== '__main__':
    # 1\ Parses the command line arguments and returns as a simple namespace.
    config = Utils2.read_json(sys.argv[1])
    print("create the output folder")
    if not os.path.exists(config.plot_path):
        os.makedirs(config.plot_path)
    if not os.path.exists(config.temp_bed_path):
        os.makedirs(config.temp_bed_path)

    # 2\ Read and pre-process the data
    data = Data(config.input_data_path, config.label_path,
                           config.bed_path, config.cluster)

    cam, label, bed = data.read_data()
    cam, bed = data.process_data(label, cam, bed)

    # 3\ Generate the bed file of cam important region
    phastcon = Phastcon(config.phastcon_path, bed, config.temp_bed_path)
    subset_index, phastcon_bed_array = phastcon.generate_matching_phastcon_array()

    # 4\ Plot
    plot = Plot(cam, phastcon_bed_array, config.plot_path, subset_index)
    plot.plot()


