# Author: Qasim Shahid
# Here are some common commands that you will need when setting up your EC2 instances. 
# Do not execute this file on its own, rather copy and paste the commands that you need.

# Updating everything 
sudo apt-get update
sudo apt-get upgrade

# Install docker on your EC2 instance (Ubuntu)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install kubectl on your EC2 instance (Ubuntu)
sudo snap install kubectl --classic

# Deploy rancher
sudo docker run --privileged -d --restart=unless-stopped -p 80:80 -p 443:443 rancher/rancher


# For Jenkins, you will need Java
sudo apt update
sudo apt install maven # install maven for pipeline
sudo apt install fontconfig openjdk-17-jre
sudo apt install openjdk-17-jdk # needed

sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins

# You need to get these plugins: 
# - Kubernetes CLI
# - Github
# - Docker CLI

sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins

# To get the password for Jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword

# For issues with docker build on jenkins
sudo usermod -a -G docker jenkins
sudo systemctl restart jenkins

# IMPORTANT - MAKE SURE JENKINS INSTANCE HAS JAVA 17 SET AS THE DEFAULT JAVA VERSION
# You can check the default java version using the following command:
update-java-alternatives --list

# If you have multiple versions of Java installed, you can set the default version using the following command:
# This will set Java 17 as the default version. Make sure to replace the path with the correct one for your system. This is what the path should be if you installed openjdk-17-jdk
sudo update-java-alternatives --set /usr/lib/jvm/java-1.17.0-openjdk-amd64


