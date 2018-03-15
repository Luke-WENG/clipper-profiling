# request_burst
import requests, json, time, sys, numpy as np

def dataset_load(dataset_number):
    dataset_path = '../../datasets/'
    dataset_name = ['breast-cancer.npz', 'diabetes.npz', 'digit.npz', 'iris.npz', 'wine.npz']
    
    number = dataset_number % 5
    print "dataset:   "+dataset_name[number]
    
    with np.load(dataset_path + dataset_name[number]) as data:
        [train_X, train_Y, test_X, test_Y] = [data['train_X'], data['train_Y'], data['test_X'], data['test_Y']]
    
    print "datashape: trainset:", train_X.shape, ", testset:", test_X.shape
    return [train_X, train_Y, test_X, test_Y]
    
query_times = 1500
interval = 0.01
if len(sys.argv) >= 3:
	query_times = int(sys.argv[1])
	interval = float(sys.argv[2])
elif len(sys.argv) >= 2:
	query_times = int(sys.argv[1])

[train_X, train_Y, test_X, test_Y] = dataset_load(0)
length = train_X.shape[0]

headers = {"Content-type": "application/json"}
clipper_url = "192.168.56.101" # default: "localhost"

latency_sum = 0
for i in range(query_times):
	print "request: %4d" % i,
	start = time.time()
	print requests.post("http://"+clipper_url+":1337/breast-cancer/predict", 
		headers=headers, 
		data=json.dumps({"input": list(train_X[i % length])})).json()
	latency = time.time()-start
	print "latency: ", latency
	latency_sum += latency
	time.sleep(interval)

	if i == length - 1:
		print "Average Latency Before Loop Back:", latency_sum/query_times
		latency_sum = 0

print "Average Latency After Loop Back:", latency_sum/(query_times-length)
