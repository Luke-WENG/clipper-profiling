# clipper_start
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())

clipper_conn.start_clipper()
clipper_conn.connect()

clipper_conn.register_application(
	name="breast-cancer", 
	input_type="doubles", 
	default_output="-1.0", 
	slo_micros=100000)

clipper_conn.get_all_apps()

#################################################
######### Define Own Prediction Function ########
#################################################

import sklearn
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

model_path = "../../models/sklearn/" 
model_name = "nn_model.sav"
clf = joblib.load(model_path + model_name)

def feature_sum(xs):
	if type(xs) is np.array:
		if xs.shape[1] == 10: # legal input
			preds = clf.predict(xs)
			return [str(p) for p in preds]
		else:
			return -1 # illegal input
	else:
		return -1 # illegal input

#################################################
#################################################
#################################################

from clipper_admin.deployers import python as python_deployer

python_deployer.deploy_python_closure(clipper_conn, 
	name="nn-model", 
	version=1, 
	input_type="doubles", 
	func=feature_sum)

clipper_conn.link_model_to_app(app_name="breast-cancer", model_name="nn-model")

# clipper_conn.stop_all()