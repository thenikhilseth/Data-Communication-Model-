import batch_pb2
import requests


batch_request = batch_pb2.Request()

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

batch_request.rfw_id = rfw_id
batch_request.bench_type = bench_type
batch_request.metric = metric
batch_request.batch_id = batch_id
batch_request.batch_unit = batch_unit
batch_request.batch_size = batch_size
batch_request.data_type = data_type
batch_request.data_analytics = data_analytics

res = requests.get("http://3.82.117.157:5000/get_batches?", headers={'Content-Type': 'application/protobuf'},
                   data=batch_request.SerializeToString())

batch_response = batch_pb2.Response.FromString(res.content)
print(batch_response)
