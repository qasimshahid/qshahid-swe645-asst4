// Jenkinsfile: CI/CD pipeline configuration for building, testing, and deploying the Python Survey application.
// # Qasim Shahid
// SWE 645 - Assignment 4
// Jenkinsfile for CI/CD pipeline
// This Jenkinsfile automates the build, test, and deployment process for a Python FastAPI application using Docker and Kubernetes.
// It includes stages for checking out the code, preparing secrets, building the Docker image, pushing it to Docker Hub, and deploying it to a Kubernetes cluster.
// The pipeline uses Jenkins credentials to manage sensitive information such as Docker Hub credentials and Kubernetes configuration.
// The pipeline is designed to be triggered on changes to the main branch of the GitHub repository.

pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'qshahid/pythonsurvey'
        REGISTRY_CREDENTIAL = 'dockerhub_credentials'
        GIT_REPO_URL = 'https://github.com/qasimshahid/qshahid-swe645-asst4.git'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${env.GIT_REPO_URL}"
            }
        }

        stage('Prepare Secrets') {
            steps {
                script { // Load secrets from Jenkins credentials, the file in the git repo is not used, it's just an an example. Jenkins will use the secret file you provide instead.
                    withCredentials([file(credentialsId: 'db_secret_file', variable: 'DB_SECRET')]) {
                        sh 'cp $DB_SECRET ./db_secret.json'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}", "pythonsurvey")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', REGISTRY_CREDENTIAL) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script { // Load Kubernetes config from Jenkins credentials, get the kubeconfig file from Rancher and upload it to Jenkins credentials.
                    withKubeConfig([credentialsId: 'kubeconfig_credentials']) {
                        sh 'kubectl apply -f pythonsurvey/deployment.yaml'
                        sh 'kubectl apply -f pythonsurvey/service.yaml'
                        sh 'kubectl rollout restart deployment/pythonsurvey-deployment'
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
