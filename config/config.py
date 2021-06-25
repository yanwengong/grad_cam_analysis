class Config:
    def __init__(self,
                 input_data_path,
                 label_path,
                 bed_path,
                 max_index_path,
                 cluster,
                 cutoff_method,
                 threshold,
                 percentile,
                 method,
                 result_path):
        self.input_data_path = input_data_path
        self.label_path = label_path
        self.bed_path = bed_path
        self.max_index_path = max_index_path
        self.cluster = cluster
        self.cutoff_method = cutoff_method
        self.threshold =threshold
        self.percentile = percentile
        self.method = method
        self.result_path = result_path




