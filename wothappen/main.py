from flask import Flask, request, abort
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def test():
    json_file =request.json
    data = json_file['resource']

    print('data posted from firehose: ', data)
    return 'post firehose all', 200

if __name__ == "__main__":
    app.run(port=4041, debug=True)