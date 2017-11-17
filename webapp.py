from flask import Flask,request
from dbservice import Wallpapers
import numpy
app = Flask(__name__)

@app.route('/', methods=['GET'])
def dbquery():
	query = request.form.get('query')
	results = Wallpapers.query.filter_by(collection=query).first()
	debugging = Wallpapers.get_debug_queries()
	print numpy.shape(results)
	print type(results)
	print len(results)
	print results
	return results[1].collection
if __name__ == '__main__':
    app.run(host=0.0.0.0)