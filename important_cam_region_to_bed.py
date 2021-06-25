import numpy as np
import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline

class RegionToBed():

    def __init__(self, forward_cam, bed, threshold, percentile, method, cutoff_method):
        self.forward_cam = forward_cam #np.array
        self.bed = bed #np.array
        self.threshold = float(threshold)
        self.percentile = float(percentile)
        self.method = int(method)
        self.cam_length = len(forward_cam[0])
        self.cutoff_method = cutoff_method

    def get_bed(self):
        """

        :return: df: pd data frame bed format, contain important cam region
        :return: bed_df: pd data frame bed format, contain all the bed regions that are accessible to selected cell clusters
        """

        fold = (1000)/(self.forward_cam.shape[1]-1.0)

        arr = np.empty((0, 2), int)

        # TODO remove the self.threshold input in the future
        if self.cutoff_method == "percentile":
            threshold = np.percentile(self.forward_cam, self.percentile)
        elif self.cutoff_method == "threshold":
            threshold = self.threshold

        print("----------------- selected threshold ---------------")
        print(threshold)

        if self.method == 1:

            # Method I: select the max one region per peak
            for i in range(self.forward_cam.shape[0]):
                peak = self.forward_cam[i]

                bed_left= self.bed[i,1]

                if max(peak) > threshold:
                    peak_index = np.argmax(peak)
                    left = peak_index
                    right = peak_index
                    while peak[left] > threshold:
                        if left <= 0:
                            break
                        left -= 1
                    while peak[right] > threshold:
                        if right >= 52:
                            break
                        right += 1

                    left = int(left * fold) + bed_left
                    right = int(right * fold) + bed_left

                else:
                    left = 0
                    right = 1

                    # index = np.squeeze(np.where(peak > self.cam_threshold),0)*fold

                left = int(left)
                right = int(right)
                arr = np.append(arr, np.array([[left, right]]), axis=0)

            print(arr.shape)
            print(arr)
            df = pd.DataFrame(arr, columns=['chr', 'start', 'end'])

            df['chr'] = self.bed[:, 0]
            df = df[['chr', 'start', 'end']]


        # Method II: select the none or many region per peak, purely depending on the cutoff
        if self.method == 2:

            index_array = np.argwhere(self.forward_cam > threshold)

            ## organize the index array
            new_index_array = np.empty((0, 3), int)
            i = 0
            while i < len(index_array) - 1:
                index = index_array[i][0]
                start = index_array[i][1]

                while index_array[i][1] == index_array[i + 1][1] - 1:
                    i += 1
                    if i == len(index_array) - 1:
                        break

                end = index_array[i][1]
                new_index_array = np.append(new_index_array, np.array([[index, start, end]]), axis=0)
                i += 1

            print("-------------- new_index_array --------------")
            print(new_index_array.shape)
            print(new_index_array)


            ## generate the new bed
            arr = np.empty((0, 3), int)
            for i in new_index_array:
                bed_index = i[0]
                chr = self.bed[bed_index, 0]
                #print(self.bed[bed_index, 1])
                left = int(self.bed[bed_index, 1] + i[1] * fold)

                right = int(self.bed[bed_index, 1] + i[2] * fold)
                arr = np.append(arr, np.array([[chr, left, right]]), axis=0)

            print(arr.shape)
            print(arr)
            df = pd.DataFrame(arr, columns=['chr', 'start', 'end'])

        if self.method == 3:
            print("---------------- method 3 threshold -----------------")
            print(threshold)

            # new_forward_cam = []
            # for i in self.forward_cam:
            #     x = np.linspace(0, 999, len(i))
            #     y = i
            #     spl = InterpolatedUnivariateSpline(x, y)
            #     new_y = spl(x)
            #     new_forward_cam.append(new_y)
            #
            # self.forward_cam = np.asarray(new_forward_cam)

            # 0514 added, filter out peaks, when max grad cam less than 0.005
            grad_cam_max_requirement = 0.005
            max_array = np.amax(self.forward_cam , axis=1)
            pass_index = np.squeeze(np.argwhere(max_array > grad_cam_max_requirement))
            fail_index = np.squeeze(np.argwhere(max_array <= grad_cam_max_requirement))
            print("----------------- length of pass and failed peak max requirement ----------")
            print(pass_index.shape[0])
            print(fail_index.shape[0])

            print("------------ length of forward_cam before and after peak max requirement ------")

            print(self.forward_cam.shape[0])
            self.forward_cam = self.forward_cam[pass_index]
            print(self.forward_cam.shape[0])

            # 0514 added, ends


            cam_index_array = np.argwhere(self.forward_cam > threshold)
            non_cam_index_array = np.argwhere(self.forward_cam == 0)

            ## organize the index array
            cam_index_array = self._get_new_index_array(cam_index_array, "cam")
            non_cam_index_array = self._get_new_index_array(non_cam_index_array, "non_cam")

            print("-------------- new_index_array --------------")
            print(cam_index_array.shape)
            print(cam_index_array)

            print(non_cam_index_array.shape)
            print(non_cam_index_array)

            ## generate the new bed
            cam_bed_df = self._generate_bed_from_index_array(cam_index_array, fold)
            non_cam_bed_df = self._generate_bed_from_index_array(non_cam_index_array, fold)
            #df = df[['chr', 'start', 'end']]

        bed_df = pd.DataFrame(self.bed, columns=['chr', 'start', 'end'])
        return cam_bed_df, non_cam_bed_df, bed_df


    # function to merge the index array
    def _get_new_index_array(self, index_array, step):
        new_index_array = np.empty((0, 3), int)
        i = 0
        while i < len(index_array) - 1:
            index = index_array[i][0]
            start = index_array[i][1]

            while index_array[i][1] == index_array[i + 1][1] - 1:
                i += 1
                if i == len(index_array) - 1:
                    break

            end = index_array[i][1]
            if step == "cam":
                if start -1 > 0:
                    start -= 1
                if end + 1 < self.cam_length - 1:
                    end += 1
            new_index_array = np.append(new_index_array, np.array([[index, start, end]]), axis=0)
            i += 1
        return new_index_array

    def _generate_bed_from_index_array(self, index_array, fold):
        arr = np.empty((0, 3), int)
        for i in index_array:
            bed_index = i[0]
            chr = self.bed[bed_index, 0]
            # print(self.bed[bed_index, 1])
            left = int(self.bed[bed_index, 1] + i[1] * fold)

            right = int(self.bed[bed_index, 1] + i[2] * fold)
            arr = np.append(arr, np.array([[chr, left, right]]), axis=0)

        print(arr.shape)
        print(arr)
        df = pd.DataFrame(arr, columns=['chr', 'start', 'end'])
        return df











