from flask import Flask, request
from batch_reponse import BatchResponse
import batch_pb2

app = Flask(__name__)


@app.route('/get_batches', methods=['GET'])
def get_batches():
    batch_request = batch_pb2.Request.FromString(request.data)
    batch_response = batch_pb2.Response()
    batch_object = BatchResponse(batch_request.rfw_id, batch_request.bench_type, batch_request.metric,
                                 batch_request.batch_unit, batch_request.batch_id, batch_request.batch_size, batch_request.data_type, batch_request.data_analytics)
    result = batch_object.binary_result()
    batch_response.rfw_id = result['rfw_id']
    batch_response.last_batch_id = result['last_batch_id']
    data_samples = result['data_samples']
    batch_response.data_analytics = result['data_analytics']

    for batch in data_samples:
        proto_batch = batch_pb2.Response.DATA_SAMPLES()
        samples_arr = []
        for i in range(0, len(batch)):
            samples_arr.append(batch[list(batch.keys())[i]])
        proto_batch.sample_data[:] = samples_arr
        batch_response.batch_data.append(proto_batch)

    print(batch_response)

    if batch_response is not None and batch_response.last_batch_id is not None:
        searlized_batch_res = batch_response.SerializeToString()
        return searlized_batch_res


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
