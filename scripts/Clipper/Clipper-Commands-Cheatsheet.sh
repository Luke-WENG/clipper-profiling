# Clipper-Commands-Cheatsheet
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())

# clipper_conn.start_clipper()
clipper_conn.connect()


#################################################
################ Model Update ###################
#################################################
# Define new Function from Model.sav
import sklearn
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

version_postfix="15x2k"
model_path = "../../models/sklearn/" 
model_name = "dig_nn_model_"+version_postfix+".sav"
clf = joblib.load(model_path + model_name)

def clf_predict(xs):
	return clf.predict(xs)


# Deploy Python Function to Model+Version
from clipper_admin.deployers import python as python_deployer
python_deployer.deploy_python_closure(
	clipper_conn, 
	name="digit-nn-model", 
	version=version_postfix,
	input_type="doubles", 
	func=clf_predict)


# Change Version of Function for Certain Model
model_name="digit-nn-model"
model_version=version_postfix
clipper_conn.set_model_version(name=model_name, version=model_version) 
# clipper_conn.set_model_version(name="wordcount", version="1") # (name=<model_name>, version=<name_in_string>)


#################################################
################### Request #####################
#################################################
import requests, json, time, sys, numpy as np
headers = {"Content-type": "application/json"}
clipper_url = "192.168.56.101" # default: "localhost"
app_name = "digit"
# data_input = json.dumps({"input": list(np.random.random(input_size))})
data_input = json.dumps({"input": list( np.random.randint(0, 16, 64).astype(float))})
print requests.post("http://"+clipper_url+":1337/"+app_name+"/predict", headers=headers, data=data_input).json()

## Repeat until output == 1:
request_output = 0
request_id = 0
while request_output != 1:
	data_input = json.dumps({"input": list( np.random.randint(0, 16, 64).astype(float) )})
	request_id += 1
	request_output = requests.post("http://"+clipper_url+":1337/"+app_name+"/predict", headers=headers, data=data_input).json()['output']
	print '%4d' % request_id, request_output

