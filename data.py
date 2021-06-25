import numpy as np
import pandas as pd
import os

class Data():

    def __init__(self, input_data_path, label_path, bed_path, max_index_path, cluster):
        self.input_data_path = input_data_path
        self.cluster = cluster
        self.bed_path = bed_path
        self.max_index_path = max_index_path
        self.label_path = label_path


    def read_data(self):
        """
        function to read in all the data
        :return: forward gram_cam score for selected cluster
        :return: one-hot encoding label
        :return: peak bed file
        """
        forward_file_name = "cluster_" + str(self.cluster) + "_forward_cam.csv"
        forward_path = os.path.join(self.input_data_path, forward_file_name)
        forward_cam = pd.read_csv(forward_path, sep=',', header=None)

        reverse_file_name = "cluster_" + str(self.cluster) + "_complement_cam.csv"
        reverse_path = os.path.join(self.input_data_path, reverse_file_name)
        reverse_cam = pd.read_csv(reverse_path, sep=',', header=None) # TODO reverse the strand
        # print("---------- check reverse the reverse strand --------------")
        # print(reverse_cam)
        reverse_cam = reverse_cam[reverse_cam.columns[::-1]]
        # print(reverse_cam)

        print("---------- check forward and reverse combination --------------")
        print(forward_cam)
        print(reverse_cam)
        # combine the forward and reverse strand based on the max index
        forward_max_index_file_name = "forward_cluster_" + str(self.cluster) + "_index.npy"
        forward_max_index = np.load(os.path.join(self.max_index_path, forward_max_index_file_name))

        reverse_max_index_file_name = "reverse_cluster_" + str(self.cluster) + "_index.npy"
        reverse_max_index = np.load(os.path.join(self.max_index_path, reverse_max_index_file_name))

        forward_max_index = np.squeeze(forward_max_index)
        reverse_max_index = np.squeeze(reverse_max_index)

        print("---------- check loaded forward and reverse index  --------------")
        print(forward_max_index)
        print(reverse_max_index)

        print("---------- check forward and reverse combination after shape them --------------")

        forward_cam = forward_cam.iloc[forward_max_index]
        reverse_cam = reverse_cam.iloc[reverse_max_index]

        print(forward_cam)
        print(reverse_cam)

        combined_cam = pd.concat([forward_cam, reverse_cam])
        combined_cam = combined_cam.sort_index()

        print("---------- check combined forward and reverse --------------")
        print(combined_cam)


        label = pd.read_csv(self.label_path, delimiter=",", header=None)

        bed = pd.read_csv(self.bed_path, delimiter='\t', header=None)

        print("---------- check loaded file --------------")
        print(forward_cam.shape)
        print(reverse_cam.shape)
        print(label.shape)
        print(bed.shape)
        print(combined_cam.shape)

        return combined_cam, label, bed

    def process_data(self, label, combined_cam, bed):
        """

        :param label:
        :param cam:
        :param bed:
        :return cam: np.array cam corresponding to selected cell cluster
        :return bed: np.array bed file
        """
        cluster_pos_label_index = self._find_cluster_pos_index(label, self.cluster)
        combined_cam = np.squeeze(combined_cam.values[[cluster_pos_label_index], :], axis=0)
        bed = np.squeeze(bed.values[[cluster_pos_label_index], :], axis=0)

        print("---------- check cam and bed file --------------")
        print(combined_cam.shape)
        print(bed.shape)
        print(combined_cam)
        print(bed)

        return combined_cam, bed

    def _find_cluster_pos_index(self, label, cell_cluster):
        """

        :param label: pd.dataframe, one-hot encoding label
        :param cell_cluster: int, selected cell cluster
        :return: list of index, where the peak is accessible for selected cell cluster
        """

        cluster_pos_label_index = []
        for i, j in enumerate(list(label.iloc[:, cell_cluster])):
            if j == 1:
                cluster_pos_label_index.append(i)
        return cluster_pos_label_index