# tutorial-tensorflow-install-and-test.sh
# https://www.tensorflow.org/serving/setup
# https://www.tensorflow.org/install/install

# Install Bazel
sudo apt-get update && sudo apt-get install -y openjdk-8-jdk

echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -

sudo apt-get update && sudo apt-get install -y bazel && sudo apt-get upgrade -y bazel

# Install Essential Packages
sudo apt-get update && sudo apt-get install -y \
        build-essential \
        curl \
        libcurl3-dev \
        git \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python-dev \
        python-numpy \
        python-pip \
        software-properties-common \
        swig \
        zip \
        zlib1g-dev \

pip install --upgrade pip

# Pip Install packages
pip install tensorflow \
		tensorflow-serving-api \
		scikit-learn \
        scipy \
        requests \
        psutil


# Install Docker
sudo apt-get remove docker docker-engine docker.io
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88

# To check whether it is like
##
## pub   4096R/0EBFCD88 2017-02-22
##       Key fingerprint = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
## uid                  Docker Release (CE deb) <docker@docker.com>
## sub   4096R/F273FCD8 2017-02-22
##

sudo add-apt-repository \
	"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
	$(lsb_release -cs) \
	stable"
sudo apt-get update
sudo apt-get install -y docker-ce

# DONE
# To install other versions of Docker
## apt-cache madison docker-ce
## sudo apt-get install docker-ce=17.12.0~ce-0~ubuntu

sudo docker run hello-world

# To run docker without sudo
sudo groupadd docker
sudo usermod -aG docker $USER
logout
# then login

# Install Clipper
sudo pip install git+https://github.com/ucbrise/clipper.git@develop#subdirectory=clipper_admin


