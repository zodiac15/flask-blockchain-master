from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
import blockChain
import resources
from flask_restful import Api
from flask_apscheduler import APScheduler


app = Flask(__name__)
api = Api(app)
scheduler = APScheduler()

scheduler.api_enabled = True
scheduler.init_app(app)




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
                'salt': request.form['salt'],
                'nonce': request.form['nonce'],
                'tag': request.form['tag'],
            },
            'creator': request.form['creator'],
            'block_type': request.form['type'],
        }
        if len(block['data']['file_hash']) < 1:
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


@scheduler.task('interval', id='do_job_1', seconds=60, misfire_grace_time=900)
def scheduled_integrity_check():
    with scheduler.app.app_context():
        results = blockChain.check_blocks_integrity()
        with open("integrity_errors.txt", 'a') as f:
            for block in results:
                if block['result'] == 'error':
                    f.write("Block " + block["block"] + " corrupted.\n")
                    app.logger.info("Block " + block["block"] + " corrupted.")


@scheduler.task('interval', id='do_job_1', seconds=600, misfire_grace_time=60)
def scheduled_block_miner():
    with scheduler.app.app_context():
        max_index = int(blockChain.get_next_block())

        for i in range(2, max_index):
            blockChain.get_POW(i)
            app.logger.info('Mined block# %d', i)


api.add_resource(resources.AddBlock, '/api/addblock')
api.add_resource(resources.FetchBlock, '/api/fetch')

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)
