from flask import Flask, render_template, jsonify, request
from strategies import strategies
import requests

app = Flask(__name__)


@app.route('/get-strategy', methods=['POST'])
def get_strategy():
    data = request.json

    url = 'https://api.quantumnumbers.anu.edu.au'
    key = data.get('apiKey')
    app.logger.info(f"Key:{key}")
    # current strategy is this: generate one int for each strategy
    # maximum int = strategy to choose

    r = requests.get(url, headers={'x-api-key': key}, params={
        'length': len(strategies),
        'type': 'uint16',
    })

    if r.status_code == 200:
        result = r.json()['data']
        biggest = max(result)
        if result.count(biggest) == 1:
            return jsonify({'strategy': strategies[result.index(biggest)]})
        else:
            return jsonify({'strategy': 'Uncertain reading. Possibilities:\n' + '\n'.join(
                strategies[i] for i, x in enumerate(result) if x == biggest)})
    else:
        return jsonify({'error': 'API request failed'}), r.status_code


@app.route('/')
def index():
    # return index.html template
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
