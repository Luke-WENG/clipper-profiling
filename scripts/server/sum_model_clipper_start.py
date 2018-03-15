# clipper_start
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())

clipper_conn.start_clipper()
clipper_conn.connect()

clipper_conn.register_application(
	name="hello-world", 
	input_type="doubles", 
	default_output="-1.0", 
	slo_micros=100000)

clipper_conn.get_all_apps()

def feature_sum(xs):
	return [str(sum(x)) for x in xs]

from clipper_admin.deployers import python as python_deployer

python_deployer.deploy_python_closure(
	clipper_conn, 
	name="sum-model", 
	version=1, 
	input_type="doubles", 
	func=feature_sum)

clipper_conn.link_model_to_app(app_name="hello-world", model_name="sum-model")

# clipper_conn.stop_all()