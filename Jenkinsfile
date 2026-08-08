pipeline {
    agent any

    environment {
        IMAGE_NAME = "sarathbare/production-cicd-pipeline"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Get Git Commit') {
            steps {
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()

                    echo "Git Commit: ${env.GIT_COMMIT_SHORT}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                    -t ${IMAGE_NAME}:${GIT_COMMIT_SHORT} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}:${GIT_COMMIT_SHORT}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl set image deployment/production-cicd-app \
                    production-cicd-app=${IMAGE_NAME}:${GIT_COMMIT_SHORT}
                '''
            }
        }

        stage('Wait for Rollout') {
            steps {
                sh '''
                    kubectl rollout status deployment/production-cicd-app
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "Deployed Image:"
                    kubectl get deployment production-cicd-app \
                    -o jsonpath='{.spec.template.spec.containers[0].image}'
                    echo ""

                    echo "Pods:"
                    kubectl get pods -l app=production-cicd-app

                    echo "Service:"
                    kubectl get svc production-cicd-service
                '''
            }
        }
    }

    post {
        success {
            echo 'Production CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'Production CI/CD Pipeline failed!'
        }
    }
}
