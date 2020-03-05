import os
from flask import Flask, render_template

from web.server.api.expense_details import expense_details_handler

app = Flask(__name__, static_folder="../client/build/static", template_folder="../client/build")


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/api/expense_details', methods=['GET'])
def expense_details():
    return expense_details_handler()


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
