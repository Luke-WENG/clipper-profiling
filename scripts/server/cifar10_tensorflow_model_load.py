# Prepare the Application
app_name = "cifar-binary-classifier"
# If the model (which we will later link to our application) doesn't
# return a prediction in time, predict label 0 (bird) by default default_output = "0"
clipper_conn.register_application(
	name=app_name,
    input_type="doubles",
    default_output=default_output,
    slo_micros=10000000)

# Train Logistic Regression Model
from sklearn import linear_model as lm
def train_sklearn_model(m, train_x, train_y):
	m.fit(train_x, train_y)
	return m
lr_model = train_sklearn_model(lm.LogisticRegression(), train_x, train_y)
print("Logistic Regression test score: %f" % lr_model.score(test_x, test_y))

# Deploy Logistic Regression Model
def sklearn_predict(images):
	preds = lr_model.predict(images)
	return [str(p) for p in preds]

print("Predicted labels: {}".format(sklearn_predict(test_x[0:3])))
print("Correct labels: {}".format(test_y[0:3]))

model_name = "cifar-model"
python_deployer.deploy_python_closure(
    clipper_conn,
    name="cifar-model",
    version="1",
    input_type="doubles",
    func=sklearn_predict
)
clipper_conn.link_model_to_app(app_name="cifar-binary-classifier", model_name="cifar-model")


#################################################
###### load Cifar10 model from TensorFlow #######
#################################################

import os
import tensorflow as tf
import numpy as np

tf_cifar_model_path = os.path.abspath("../../models/tensorflow/cifar10_model/model.ckpt-39072") # target to model.ckpt-39072.meta file
with tf_session.graph.as_default():
	saver = tf.train.import_meta_graph("%s.meta" % tf_cifar_model_path)
	saver.restore(tf_session, tf_cifar_model_path)

# Score it on the evaluation dataset
def tensorflow_score(session, test_x, test_y):
	logits = session.run('softmax_logits:0',
		feed_dict={'x:0': test_x})
	relevant_activations = logits[:, [cifar_utils.negative_class, cifar_utils.positive_class]]
	preds = np.argmax(relevant_activations, axis=1)
	return float(np.sum(preds == test_y)) / float(len(test_y))

print("TensorFlow ConvNet test score: %f" % tensorflow_score(tf_session, test_x, test_y))
