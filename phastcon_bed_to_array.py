import pybedtools
import numpy as np
import pandas as pd
import os

class Phastcon():
    def __init__(self, phastcon_path, bed, temp_bed_path):
        """

        :param phastcon_path: path to the phastCons100way_hg19 data
        :param bed: bed file in np.array format
        :param bed_path: temp path to save one bed file per peak
        """
        self.phastcon = pybedtools.BedTool(phastcon_path)
        self.bed = bed
        self.bed_path = temp_bed_path

    def generate_matching_phastcon_array(self):
        phastcon_bed_list = []
        #subset_index = self._subset(self.bed, 100)
        subset_index = [i for i in range(0,60)]
        self.bed = self.bed[subset_index]
        print("---------------check subset bed------------")
        # (n, 3)
        print(self.bed.shape)
        print(self.bed)

        for i in range(self.bed.shape[0]):
            bed = np.asarray(self.bed[i, :])
            bed = np.expand_dims(bed, axis=0)
            print(bed.shape)
            bed_df = pd.DataFrame(bed, columns=['chr', 'start', 'end'])
            bed_file_name = "peak_" +str(i) +".bed"
            bed_df.to_csv(os.path.join(self.bed_path, bed_file_name),
                          sep='\t', header=False, index=False)
            phastcon_bed_file_name = "phastcon_peak_" +str(i) +".bed"
            self.phastcon.intersect(os.path.join(self.bed_path, bed_file_name)).\
                saveas(os.path.join(self.bed_path, phastcon_bed_file_name))
            phastcon_bed = pd.read_csv(os.path.join(self.bed_path, phastcon_bed_file_name),
                                       delimiter = '\t', header = None).iloc[:,4]

            print("---------------check phastcon bed------------")
            print(len(phastcon_bed))
            print(phastcon_bed)

            phastcon_bed_list.append(phastcon_bed)


        print("---------------check final phastcon------------")

        print(len(phastcon_bed_list))
        print(phastcon_bed_list)
        return subset_index, phastcon_bed_list


    def _subset(self, data, size):
        np.random.seed(202101190)
        index = np.random.choice(data.shape[0], size=size, replace=False)
        return index