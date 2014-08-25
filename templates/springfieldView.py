from flask import request, jsonify, render_template
from springfieldModel import SpringfieldModel

import flask.views
import json



class SpringfieldFirstload(flask.views.MethodView):
    def get(self):
        return render_template('index.html')

class SpringfieldView(flask.views.MethodView):
	def get(self, start_date, end_date, has_retrieved):
		allData=SpringfieldModel.get_data(start_date, end_date, has_retrieved)
		return jsonify({
			'success': True,
			'allData': allData,
			})