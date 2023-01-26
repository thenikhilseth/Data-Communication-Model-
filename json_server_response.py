from flask import Flask, request, json
from batch_reponse import BatchResponse

app = Flask(__name__)


@app.route('/get_batches', methods=['GET'])
def get_batches():
    rfw_id = request.json['rfw_id']
    bench_type = request.json['bench_type']
    metric = request.json['metric']
    batch_unit = request.json['batch_unit']
    batch_id = request.json['batch_id']
    batch_size = request.json['batch_size']
    data_type = request.json['data_type']
    data_analytics = request.json['data_analytics']
    batch_object = BatchResponse(
        rfw_id, bench_type, metric, batch_unit, batch_id, batch_size, data_type, data_analytics)
    result = batch_object.send_json_results()

    if result is not None:
        return json.dumps(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000)
