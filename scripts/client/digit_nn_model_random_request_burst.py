# request_burst
import requests, json, time, sys, numpy as np

query_times = 3000 # # of requests
# interval = 0.01

if len(sys.argv) >= 3:
	query_times = int(sys.argv[1])
	interval = float(sys.argv[2])
elif len(sys.argv) >= 2:
	query_times = int(sys.argv[1])

headers = {"Content-type": "application/json"}
clipper_url = "192.168.56.101" # default: "localhost"

latency_sum = 0
for i in range(query_times):
	print "\t%4d" % i,
	start = time.time()
	requests.post("http://"+clipper_url+":1337/digit/predict", 
		headers=headers, 
		data=json.dumps({"input": list( np.random.randint(0, 16, 64).astype(float).reshape(1,64) )})).json()
	latency = time.time()-start
	print latency,
	latency_sum += latency
	# time.sleep(interval)

print "Average Latency", latency_sum/query_times
