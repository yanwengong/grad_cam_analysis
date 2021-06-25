import sys
import os
from utils import Utils
from data import Data
from important_cam_region_to_bed import RegionToBed


if __name__== '__main__':
    # 1\ Parses the command line arguments and returns as a simple namespace.
    config = Utils.read_json(sys.argv[1])
    print("create the output folder")
    if not os.path.exists(config.result_path):
        os.makedirs(config.result_path)



    for i in config.cluster:
        print("------------- process cluster" + str(i))
        # 2\ Read and pre-process the data
        data = Data(config.input_data_path, config.label_path,
                    config.bed_path, config.max_index_path,
                    i)

        cam, label, bed = data.read_data()
        cam, bed = data.process_data(label, cam, bed)

        # 3\ Generate the bed file of cam important region
        cam_df, non_cam_bed_df, bed_df = RegionToBed(cam,
                                                     bed,
                                                     config.threshold,
                                                     config.percentile,
                                                     config.method,
                                                     config.cutoff_method).get_bed()
        # TODO remove the self.threshold input in the future
        if config.cutoff_method == "threshold":
            cutoff = "_threshold_" + str(config.threshold)
        elif config.cutoff_method == "percentile":
            cutoff = "_percentile_" + str(config.percentile)
        method = "_method_" + str(config.method)
        file_name = 'cluster'+str(i)+ cutoff+ method + '_cam_import.bed'
        cam_df.to_csv(os.path.join(config.result_path, file_name),
                      sep='\t', header=False, index=False)
        file_name = 'cluster' + str(i) + cutoff + method + '_non_cam_import.bed'
        non_cam_bed_df.to_csv(os.path.join(config.result_path, file_name),
                      sep='\t', header=False, index=False)

        bed_file_name = 'cluster' + str(i) + '.bed'

        bed_df.to_csv(os.path.join(config.result_path, bed_file_name),
                      sep='\t', header=False, index=False)

