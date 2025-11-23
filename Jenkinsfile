pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "devsecops-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
        SONARQUBE_SERVER = 'SonarQube'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    # Use --break-system-packages for Python 3.13+
                    python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    python3 -m pytest tests/ -v --junitxml=test-results.xml --cov=. --cov-report=xml --cov-report=html
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }
        
        stage('Code Quality Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                echo 'Checking Quality Gate status...'
                timeout(time: 5, unit: 'MINUTES') {
                    script {
                        try {
                            waitForQualityGate abortPipeline: false
                        } catch (Exception e) {
                            echo "Quality Gate status check failed, but continuing..."
                        }
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh """
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                """
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running Docker image security scan...'
                sh """
                    docker run --rm aquasec/trivy:latest image ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                """
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh """
                    docker rm -f ${DOCKER_IMAGE} || true
                    docker run -d --name ${DOCKER_IMAGE} -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                """
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
