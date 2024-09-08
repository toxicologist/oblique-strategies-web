from dis import show_code

from flask import Flask, render_template, jsonify, request
from strategies import strategies
from maxims import maxims
from proverbios import proverbios_text
from tao import get_tao
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
import requests
import random

app = Flask(__name__)
USE_REAL_API = True


### SQLAlchemy stuff ###
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats.db'
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Stat(db.Model):
    page: Mapped[str] = mapped_column(primary_key=True)
    viewcount: Mapped[int] = mapped_column()

    def __repr__(self):
        return self.page

with app.app_context():
    db.create_all()

def add_page_view(page):
    q = db.session.execute(db.select(Stat).filter_by(page=page)).scalars()
    first = q.first()
    if first:
        p = first
        p.viewcount += 1
    else:
        p = Stat(page=page, viewcount=1)
    db.session.add(p)
    print(p.viewcount)
    db.session.commit()

def get_views():
    q = db.session.execute(db.select(Stat)).scalars().all()
    return ['%s: %s' % (s.page, s.viewcount) for s in q]

### END SQLAlchemy stuff ###


@app.route('/get-strategy', methods=['POST'])
def get_strategy():
    add_page_view('/get-strategy')
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
    add_page_view('/oblique')
    # return oblique_strategies.html template
    wait_time = 30

    return render_template('oblique_strategies.html', wait_time=wait_time, show_title_icon=True)


@app.route('/delphi')
def delphi():
    add_page_view('/delphi')
    return render_template('delphi.html', entrance=maxims[:3], maxims=enumerate(maxims[3:]), show_title_icon=True)


@app.route('/proverbios')
def proverbios():
    add_page_view('/proverbios')
    return render_template('proverbios.html', proverbios=proverbios_text, show_title_icon=True)


@app.route('/tao')
def tao_te_ching():
    add_page_view('/tao')
    return render_template('tao.html', tao=get_tao(), show_title_icon=True)


@app.route('/tao-random')
def random_tao():
    add_page_view('/tao-random')
    tao = get_tao()
    i = random.randint(0, len(tao) - 1)
    verse = tao[i]
    return render_template('tao_random.html', verse=verse, i=i+1, show_title_icon=True)


@app.route('/')
def index():
    add_page_view('/')
    return render_template('index.html', show_title_icon=True)


if __name__ == '__main__':
    app.run()
