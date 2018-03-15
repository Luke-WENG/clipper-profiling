from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.deployers.python import deploy_python_closure
import numpy as np
import sklearn

clipper_conn = ClipperConnection(DockerContainerManager())

clipper_conn.start_clipper()
# Connect to an already-running Clipper cluster
clipper_conn.connect()

clipper_conn.register_application(
    name="center-world", 
    input_type="doubles", 
    default_output="-1.0", 
    slo_micros=10000000)

# Note that this function accesses the trained model via closure capture,
# rather than having the model passed in as an explicit argument.
def centered_predict(inputs):
    means = np.mean(xs, axis=0)
    centered_xs = xs - means
    model = sklearn.linear_model.LogisticRegression()
    model.fit(centered_xs, ys)
    # model.predict returns a list of predictions
    preds = model.predict(centered_xs)
    return [str(p) for p in preds]

deploy_python_closure(
    clipper_conn,
    name="example",
    version=1,
    input_type="doubles",
    func=centered_predict)

clipper_conn.link_model_to_app(app_name="center-world", model_name="example")
