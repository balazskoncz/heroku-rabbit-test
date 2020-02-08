from flask import Flask
import os

app = Flask(__name__, static_folder='static')

port = os.getenv('PORT', default=5000)
print('Starting server on port: {}'.format(port))

app.run(debug=False, port=port, host='0.0.0.0')