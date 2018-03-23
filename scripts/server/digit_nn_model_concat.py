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

# def feature_sum(xs):
	# return [str(sum(x)) for x in xs]

def query_agent_function(xs): 
	# xs is a list of x; type(x): numpy.ndarray
	import requests, json, time, sys, numpy as np
	headers = {"Content-type": "application/json"}
	clipper_url = "192.168.56.101" # default: "localhost"
	app_name = "digit"
	results = []
	for x in xs:
		data_input = json.dumps({"input": list(x)})
		results.append(requests.post("http://"+clipper_url+":1337/"+app_name+"/predict", headers=headers, data=data_input).json()['output'])
	return results


#################################################
#################################################
#################################################

from clipper_admin.deployers import python as python_deployer

python_deployer.deploy_python_closure(
	clipper_conn, 
	name="query-agent-model", 
	input_type="doubles", 
	func=query_agent_function,
	version=9)

clipper_conn.link_model_to_app(app_name="query_agent", model_name="query-agent-model")

# Debugging
clipper_conn.set_model_version(name="query-agent-model", version="3") 

import requests, json, time, sys, numpy as np
headers = {"Content-type": "application/json"}
clipper_url = "192.168.56.101" # default: "localhost"
app_name = "query_agent"
# data_input = json.dumps({"input": list(np.random.random(input_size))})
data_input = json.dumps({"input": list( np.random.randint(0, 16, 64).astype(float))})
print requests.post("http://"+clipper_url+":1337/"+app_name+"/predict", headers=headers, data=data_input).json()
