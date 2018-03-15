# Clipper install and test
## https://github.com/ucbrise/clipper

sudo pip install git+https://github.com/ucbrise/clipper.git@develop#subdirectory=clipper_admin

# sudo here otherwise it may fail to connect to Docker
sudo python

#########################################
# From here all codes are typed in python
# "## " means the output for reference
#########################################
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())

# Start Clipper. Running this command for the first time will
# download several Docker containers, so it may take some time.
clipper_conn.start_clipper()
## 17-08-30:15:48:41 INFO     [docker_container_manager.py:95] Starting managed Redis instance in Docker
## 17-08-30:15:48:43 INFO     [clipper_admin.py:105] Clipper still initializing.
## 17-08-30:15:48:44 INFO     [clipper_admin.py:107] Clipper is running

# Register an application called "hello_world". This will create
# a prediction REST endpoint at http://localhost:1337/hello_world/predict
clipper_conn.register_application(name="hello-world", input_type="doubles", default_output="-1.0", slo_micros=100000)
## 17-08-30:15:51:42 INFO     [clipper_admin.py:182] Application hello-world was successfully registered

# Inspect Clipper to see the registered apps
clipper_conn.get_all_apps()
## [u'hello_world']

# Define a simple model that just returns the sum of each feature vector.
# Note that the prediction function takes a list of feature vectors as
# input and returns a list of strings.
def feature_sum(xs):
	return [str(sum(x)) for x in xs]

# Import the python deployer package
from clipper_admin.deployers import python as python_deployer

# Deploy the "feature_sum" function as a model. Notice that the application and model
# must have the same input type.
python_deployer.deploy_python_closure(clipper_conn, name="sum-model", version=1, input_type="doubles", func=feature_sum)
## 17-08-30:15:59:56 INFO     [deployer_utils.py:50] Anaconda environment found. Verifying packages.
## 17-08-30:16:00:04 INFO     [deployer_utils.py:150] Fetching package metadata .........
## Solving package specifications: .
## 
## 17-08-30:16:00:04 INFO     [deployer_utils.py:151]
## 17-08-30:16:00:04 INFO     [deployer_utils.py:59] Supplied environment details
## 17-08-30:16:00:04 INFO     [deployer_utils.py:71] Supplied local modules
## 17-08-30:16:00:04 INFO     [deployer_utils.py:77] Serialized and supplied predict function
## 17-08-30:16:00:04 INFO     [python.py:127] Python closure saved
## 17-08-30:16:00:04 INFO     [clipper_admin.py:375] Building model Docker image with model data from /tmp/python_func_serializations/sum-model
## 17-08-30:16:00:05 INFO     [clipper_admin.py:378] Pushing model Docker image to sum-model:1
## 17-08-30:16:00:07 INFO     [docker_container_manager.py:204] Found 0 replicas for sum-model:1. Adding 1
## 17-08-30:16:00:07 INFO     [clipper_admin.py:519] Successfully registered model sum-model:1
## 17-08-30:16:00:07 INFO     [clipper_admin.py:447] Done deploying model sum-model:1.

# Tell Clipper to route requests for the "hello-world" application to the "sum-model"
clipper_conn.link_model_to_app(app_name="hello-world", model_name="sum-model")
## 17-08-30:16:08:50 INFO     [clipper_admin.py:224] Model sum-model is now linked to application hello-world

# Your application is now ready to serve predictions

#########################################
# To here, the application is now ready
# launched at <localhost-ip-address>:1337
# Code below performs the querying,
# can be from another client in the network
#########################################

# With cURL:
curl -X POST --header "Content-Type:application/json" -d '{"input": [1.1, 2.2, 3.3]}' 127.0.0.1:1337/hello-world/predict

# From a Python REPL:
import requests, json, numpy as np
headers = {"Content-type": "application/json"}
requests.post("http://localhost:1337/hello-world/predict", headers=headers, data=json.dumps({"input": list(np.random.random(10))})).json()


#########################################
# From here all codes are typed in python
# "## " means the output for reference
#########################################
# Clean up
# If you closed the Python REPL you were using to start Clipper,
# you will need to start a new Python REPL and create another connection to the Clipper cluster.
# If you still have the Python REPL session active from earlier, you can re-use your existing ClipperConnection object.

# If you have still have the Python REPL from earlier, skip
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())
clipper_conn.connect()

# Stop all Clipper docker containers
clipper_conn.stop_all()
## 17-08-30:16:15:38 INFO     [clipper_admin.py:1141] Stopped all Clipper cluster and all model containers

