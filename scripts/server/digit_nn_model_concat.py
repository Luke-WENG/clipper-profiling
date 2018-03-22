# digit_nn_model_concat.py
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())

# clipper_conn.start_clipper()
clipper_conn.connect()

clipper_conn.register_application(
	name="query_agent", 
	input_type="doubles", 
	default_output="-1.0", 
	slo_micros=10000000) # 10,000,000 micros == 10 sec

clipper_conn.get_all_apps()

#################################################
############## Define Own Function ##############
#################################################
import requests, json, time, sys, numpy as np
headers = {"Content-type": "application/json"}
clipper_url = "192.168.56.101" # default: "localhost"
app_name = "digit"

def query_agent_function(xs):
	data_input = json.dumps({"input": xs})
	return requests.post("http://"+clipper_url+":1337/"+app_name+"/predict", headers=headers, data=data_input).json()['output']

#################################################
#################################################
#################################################

from clipper_admin.deployers import python as python_deployer

python_deployer.deploy_python_closure(
	clipper_conn, 
	name="query_agent_model", 
	version=1, 
	input_type="doubles", 
	func=clf_predict)

clipper_conn.link_model_to_app(app_name="query_agent", model_name="query_agent_model")
