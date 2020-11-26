from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
import blockChain

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # print(request.method )
    if request.method == 'POST':
        block = {
            'data': {
                'name': request.form['file_name'],
                'size': request.form['file_size'],
                'file_type': request.form['file_type'],
                'file_hash': request.form['file_hash'],
                'key': request.form['file_key'],
            },
            'creator': request.form['creator'],
            'signature': request.form['signature'],
            'block_type': request.form['type'],
        }
        if len(block['data']['name']) < 1:
            return redirect(url_for('index'))
        try:
            make_proof = request.form['make_proof']
        except Exception:
            make_proof = False
        blockChain.write_block(block, make_proof)
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def integrity():
    results = blockChain.check_blocks_integrity()
    if request.method == 'POST':
        return render_template('index.html', results=results)
    return render_template('index.html')


@app.route('/mining', methods=['POST'])
def mining():
    if request.method == 'POST':
        max_index = int(blockChain.get_next_block())

        for i in range(2, max_index):
            blockChain.get_POW(i)
        return render_template('index.html', querry=max_index)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
