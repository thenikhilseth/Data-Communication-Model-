import requests

rfw_id = int(input('Please Enter Request For Workload (RFW) ID:'))
bench_type = input('Please type one of the following:\n 1. DVD\n 2. NDBench\n')
metric = input('Please type one of the metrics from the following:\n'
               '1. CPUUtilization_Average\n 2. NetworkIn_Average\n 3. NetworkOut_Average\n'
               ' 4. MemoryUtilization_Average\n')
batch_id = int(input(
    'Please Enter the Batch Id (from which batch you want the data to start from) in integer: '))
batch_unit = int(
    input('Please Enter the number of samples you want in one batch in integer: '))
batch_size = int(
    input('Please Enter the number of batches to be returned in integer: '))
data_type = input(
    'Please type one of the following:\n 1. testing\n 2. training\n')
data_analytics = input(
    'Please type percentile example: 10p, 50p, 95p, 99p, avg, std, max, min\n')

# rfw_id = 2
# bench_type = "DVD"
# metric = "CPUUtilization_Average"
# batch_id = 0
# batch_unit = 5
# batch_size = 2
# data_type = "testing"
# data_analytics = "10p"

res = requests.get("http://3.82.117.157:8000/get_batches?",
                   json={"rfw_id": rfw_id,
                         "bench_type": bench_type,
                         "metric": metric,
                         "batch_unit": batch_unit,
                         "batch_id": batch_id,
                         "batch_size": batch_size,
                         "data_type": data_type,
                         "data_analytics": data_analytics
                         }
                   )

if res.status_code == 200:
    print(" rfw_id: ", res.json()['rfw_id'])
    print(" last_batch_id: ", res.json()['last_batch_id'])
    print(" data_samples: ", res.json()['data_samples'])
    print(" data_analytics: ", res.json()['data_analytics'])
