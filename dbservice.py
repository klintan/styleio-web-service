from flask import Flask,request,Response,make_response,current_app
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import or_
from sqlalchemy import or_
import numpy
import os
from datetime import timedelta
from functools import update_wrapper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/wallpapers?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'
db = SQLAlchemy(app)

def crossdomain(origin=None, methods=None, headers=None,
	            max_age=21600, attach_to_all=True,
	            automatic_options=True):
	if methods is not None:
	   methods = ', '.join(sorted(x.upper() for x in methods))
	if headers is not None and not isinstance(headers, basestring):
	   headers = ', '.join(x.upper() for x in headers)
	if not isinstance(origin, basestring):
	   origin = ', '.join(origin)
	if isinstance(max_age, timedelta):
	   max_age = max_age.total_seconds()

	def get_methods():
	    if methods is not None:
	        return methods

	    options_resp = current_app.make_default_options_response()
	    return options_resp.headers['allow']

	def decorator(f):
	    def wrapped_function(*args, **kwargs):
	        if automatic_options and request.method == 'OPTIONS':
	            resp = current_app.make_default_options_response()
	        else:
	            resp = make_response(f(*args, **kwargs))
	        if not attach_to_all and request.method != 'OPTIONS':
	            return resp

	        h = resp.headers

	        h['Access-Control-Allow-Origin'] = origin
	        h['Access-Control-Allow-Methods'] = get_methods()
	        h['Access-Control-Max-Age'] = str(max_age)
	        if headers is not None:
	            h['Access-Control-Allow-Headers'] = headers
	        return resp

	    f.provide_automatic_options = False
	    return update_wrapper(wrapped_function, f)
	return decorator
	
def any_response(data):
	ALLOWED = ['http://styleio.se']
	response = make_response(data)
	origin = request.headers['Origin']
	if origin in ALLOWED:
		response.headers['Access-Control-Allow-Origin'] = origin
	return response

class Wallpapers(db.Model):
	__tablename__ = 'wallpaper'
	id = db.Column(db.Integer, primary_key=True)
	image = db.Column(db.String(120), unique=True)
	name = db.Column(db.String(120), unique=True)
	search = db.Column(db.String(120), unique=True)
	
	def __init__(self, collection, manufacturer, articleno, name, image):
		self.image = image
		self.name = name
		self.search = search
		
class Floors(db.Model):
		__tablename__ = 'floors'
		id = db.Column(db.Integer, primary_key=True)
		image = db.Column(db.String(120), unique=True)
		name = db.Column(db.String(120), unique=True)
		search = db.Column(db.String(120), unique=True)

		def __init__(self, collection, manufacturer, articleno, name, image):
			self.image = image
			self.name = name
			self.search = search
		
@app.route('/', methods=['POST'])
@crossdomain('*')
def dbquery():
	query = request.form.get('img')
	db = request.form.get('db')
	print query
	print os.path.basename(query)
	
	results = []
	#results = Wallpapers.query.filter(or_(Wallpapers.name == query, Wallpapers.collection == query)).all()
	#results0 = Wallpapers.query(Wallpapers.collection).all()
	#peter = Wallpapers.query.filter_by(collection='Tik').all()
	#results = Wallpapers.query.filter(or_(Wallpapers.name.like('%'+query+'%'),Wallpapers.collection.like('%'+query+'%'),Wallpapers.manufacturer.like('%'+query+'%'),Wallpapers.articleno.like('%'+query+'%'))).all()
	#results.append(Wallpapers.query.filter(Wallpapers.collection.like('%'+query+'%')).all())
	#results.append(Wallpapers.query.filter(Wallpapers.manufacturer.like('%'+query+'%')).all())
	#results.append(Wallpapers.query.filter(Wallpapers.articleno.like('%'+query+'%')).all())
	#results.append(Wallpapers.query.filter(Wallpapers.name.like('%'+query+'%')).all())
	
	results = Wallpapers.query.filter_by(image=os.path.basename(query)).all()
	#results1 = Wallpapers.query.get(1)
	#results2 = Wallpapers.query.all()
	#print results2
	#print peter
	#print "susan"
	#print susan
	#print query1
	#debugging = Wallpapers.get_debug_queries()
	#print numpy.shape(results)
	#print type(results)
	#print len(results)

	#print results1.query.filter_by(collection=query).all
	#print col_res
	#print man_res
	#print art_res
	#print nam_res

	print results
	return results[0].search
	
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=7777)