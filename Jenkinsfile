pipeline {
agent any

```
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

    stage('Run Automated Tests') {
        steps {
            sh '''
                echo "Creating Python virtual environment..."

                python3 -m venv .venv

                echo "Installing dependencies..."

                .venv/bin/pip install --upgrade pip
                .venv/bin/pip install -r app/requirements.txt

                echo "Running automated tests..."

                .venv/bin/pytest -v

                echo "All automated tests passed!"
            '''
        }
    }

    stage('Build Docker Image') {
        steps {
            sh '''
                echo "Building Docker image..."

                docker build \
                -t ${IMAGE_NAME}:${GIT_COMMIT_SHORT} .

                echo "Docker image built successfully!"
            '''
        }
    }

    stage('Push Docker Image') {
        steps {
            sh '''
                echo "Pushing Docker image..."

                docker push ${IMAGE_NAME}:${GIT_COMMIT_SHORT}

                echo "Docker image pushed successfully!"
            '''
        }
    }

    stage('Deploy and Health Check') {
        steps {
            script {
                try {
                    sh '''
                        echo "Deploying image: ${IMAGE_NAME}:${GIT_COMMIT_SHORT}"

                        kubectl set image deployment/production-cicd-app \
                        production-cicd-app=${IMAGE_NAME}:${GIT_COMMIT_SHORT}

                        echo "Waiting for Kubernetes rollout..."

                        kubectl rollout status deployment/production-cicd-app \
                        --timeout=120s

                        echo "Checking application health..."

                        kubectl port-forward svc/production-cicd-service 5001:5000 \
                        >/tmp/port-forward.log 2>&1 &

                        PORT_FORWARD_PID=$!

                        sleep 3

                        curl --fail http://localhost:5001/health

                        kill $PORT_FORWARD_PID

                        echo "Application health check passed!"
                    '''
                } catch (Exception e) {

                    echo "Deployment or health check failed!"
                    echo "Rolling back Kubernetes deployment..."

                    sh '''
                        kubectl rollout undo deployment/production-cicd-app

                        echo "Waiting for rollback to complete..."

                        kubectl rollout status deployment/production-cicd-app \
                        --timeout=120s

                        echo "Rollback completed."
                    '''

                    error("Deployment failed. Kubernetes rollback executed.")
                }
            }
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
        echo "Production CI/CD Pipeline completed successfully!"
    }

    failure {
        echo "Production CI/CD Pipeline failed!"
    }

    always {
        echo "Pipeline execution completed."
    }
}
```

}
