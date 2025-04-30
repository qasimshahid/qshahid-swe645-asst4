// # Qasim Shahid
// SWE 645 - Assignment 3
// Jenkinsfile for CI/CD pipeline
// This Jenkinsfile automates the build, test, and deployment process for a Spring Boot application using Docker and Kubernetes.

pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'qshahid/pythonsurvey'
        REGISTRY_CREDENTIAL = 'dockerhub_credentials'
        GIT_REPO_URL = 'https://github.com/qasimshahid/qshahid-swe645-asst3.git'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${env.GIT_REPO_URL}"
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
                script {
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
