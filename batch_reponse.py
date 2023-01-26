import pandas as pd
import json


class BatchResponse:
    def __init__(self, rfw_id, bench_type, metric, batch_unit, batch_id, batch_size, data_type, data_analytics):
        self.rfw_id = rfw_id
        self.bench_type = bench_type
        self.metric = metric
        self.batch_id = int(batch_id)
        self.batch_size = int(batch_size)
        self.batch_unit = int(batch_unit)
        self.data_type = data_type
        self.data_analytics = data_analytics
        self.csv_data = pd.read_csv(
            "./data/" + bench_type + '-'+data_type + ".csv")

    def send_json_results(self):
        (data_samples, data_samples_sort, last_batch_id) = self.create_data_samples()
        number_of_samples = self._number_of_samples()
        sorted_data_samples = sorted(data_samples_sort)

        if self.data_analytics.split("p")[0] == "min":
            position_in_sorted_data = 0
        elif self.data_analytics.split("p")[0] == "max":
            position_in_sorted_data = len(sorted_data_samples)-1
        elif self.data_analytics.split("p")[0] == "avg":
            position_in_sorted_data = len(sorted_data_samples)/2
        elif self.data_analytics.split("p")[0] == "std":
            d = {'Score1': sorted_data_samples}
            df = pd.DataFrame(d)
            position_in_sorted_data = round(df['Score1'].std())
        else:
            position_in_sorted_data = round(number_of_samples *
                                            (int(self.data_analytics.split("p")[0])/100))

        print({
            "rfw_id": self.rfw_id,
            "last_batch_id": last_batch_id,
            "data_samples": data_samples,
            "data_analytics": sorted_data_samples[position_in_sorted_data]
        })
        return {
            "rfw_id": self.rfw_id,
            "last_batch_id": last_batch_id,
            "data_samples": data_samples,
            "data_analytics": sorted_data_samples[position_in_sorted_data]
        }

    def create_data_samples(self):
        batches = []
        data_samples_sort = []
        column = self._get_column_from_csv()
        last_batch_id = self.batch_id
        for index in range(0, self.batch_size):
            batch = column[last_batch_id *
                           self.batch_unit: (last_batch_id + 1) * self.batch_unit].to_dict()
            batches.append(batch)
            data_samples_sort.extend(column[last_batch_id *
                                            self.batch_unit: (last_batch_id + 1) * self.batch_unit])
            last_batch_id += 1

        return batches, data_samples_sort, (last_batch_id - 1)

    def binary_result(self):
        (data_samples, data_samples_sort, last_batch_id) = self.create_data_samples()
        number_of_samples = self._number_of_samples()
        sorted_data_samples = sorted(data_samples_sort)

        if self.data_analytics.split("p")[0] == "min":
            position_in_sorted_data = 0
        elif self.data_analytics.split("p")[0] == "max":
            position_in_sorted_data = len(sorted_data_samples)-1
        elif self.data_analytics.split("p")[0] == "avg":
            position_in_sorted_data = len(sorted_data_samples)/2
        elif self.data_analytics.split("p")[0] == "std":
            d = {'Score1': sorted_data_samples}
            df = pd.DataFrame(d)
            position_in_sorted_data = round(df['Score1'].std())
        else:
            position_in_sorted_data = round(number_of_samples *
                                            (int(self.data_analytics.split("p")[0])/100))
        print({
            "rfw_id": self.rfw_id,
            "last_batch_id": last_batch_id,
            "data_samples": data_samples,
            "data_analytics": sorted_data_samples[position_in_sorted_data]
        })
        return {
            "rfw_id": self.rfw_id,
            "last_batch_id": last_batch_id,
            "data_samples": data_samples,
            "data_analytics": sorted_data_samples[position_in_sorted_data]
        }

    # private methods

    def _get_column_from_csv(self):
        data_column = self.csv_data[self.metric]
        return data_column

    def _number_of_samples(self):
        return self.batch_size * self.batch_unit
