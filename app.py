from flask import Flask, render_template, jsonify, request
from strategies import strategies
from maxims import maxims
import requests

app = Flask(__name__)

USE_REAL_API = True

@app.route('/get-strategy', methods=['POST'])
def get_strategy():
    data = request.json

    if USE_REAL_API:
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
    else:
        # for testing, just return a random strategy
        import random
        return jsonify({'strategy': random.choice(strategies)[0]})


@app.route('/oblique')
def oblique():
    # return oblique_strategies.html template
    wait_time = 30

    return render_template('oblique_strategies.html', wait_time=wait_time, show_title_icon=True)


@app.route('/delphi')
def delphi():
    return render_template('delphi.html', entrance=maxims[:3], maxims=enumerate(maxims[3:]), show_title_icon=True)


@app.route('/')
def index():
    return render_template('index.html', show_title_icon=True)


if __name__ == '__main__':
    app.run()
