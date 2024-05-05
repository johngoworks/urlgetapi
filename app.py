from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/redirect')
@cross_origin()
def redirect():
  original_url = request.args.get('original_url')
  if not original_url:
    return jsonify({'error': 'Missing original_url parameter'}), 400

  redirected_url = get_redirect_url(original_url)
  return jsonify({'redirected_url': redirected_url})

def get_redirect_url(url):
  try:
    response = requests.get(url, allow_redirects=False)
    if response.status_code == 301 or response.status_code == 302:
      return response.headers['Location']
    else:
      return url
  except requests.RequestException as ex:
    return url

if __name__ == '__main__':
  app.run(debug=True)
