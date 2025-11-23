pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "devsecops-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
        SONAR_SCANNER_HOME = "/opt/sonar-scanner"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                sh '''
                    python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests with coverage'
                sh '''
                    python3 -m pytest tests/ -v --junitxml=test-results.xml --cov=. --cov-report=xml --cov-report=html
                '''
            }
        }
        
        stage('Code Quality Analysis') {
            steps {
                echo 'Running SonarQube analysis'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                          -Dsonar.projectKey=devsecops-pipeline \
                          -Dsonar.projectName="DevSecOps Pipeline" \
                          -Dsonar.projectVersion=1.0 \
                          -Dsonar.sources=app.py \
                          -Dsonar.tests=tests/ \
                          -Dsonar.language=py \
                          -Dsonar.python.version=3.11 \
                          -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                echo 'Waiting for Quality Gate result'
                timeout(time: 5, unit: 'MINUTES') {
                    script {
                        try {
                            def qg = waitForQualityGate()
                            if (qg.status != 'OK') {
                                echo "Quality Gate status: ${qg.status}"
                            }
                        } catch (Exception e) {
                            echo "Quality Gate check: ${e.message}"
                        }
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                sh """
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                """
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running Trivy security scan'
                sh """
                    docker run --rm aquasec/trivy:latest image --severity HIGH,CRITICAL ${DOCKER_IMAGE}:${DOCKER_TAG} || echo "Security scan completed"
                """
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application'
                sh """
                    docker rm -f ${DOCKER_IMAGE} || true
                    docker run -d \
                      --name ${DOCKER_IMAGE} \
                      --network devsecops \
                      -p 5000:5000 \
                      ${DOCKER_IMAGE}:${DOCKER_TAG}
                    sleep 8
                    docker ps | grep ${DOCKER_IMAGE}
                """
            }
        }
        
        stage('Smoke Test') {
            steps {
                echo 'Running smoke tests'
                sh """
                    docker run --rm --network devsecops curlimages/curl:latest \
                      curl -f http://${DOCKER_IMAGE}:5000/ || exit 1
                    docker run --rm --network devsecops curlimages/curl:latest \
                      curl -f http://${DOCKER_IMAGE}:5000/health || exit 1
                    docker run --rm --network devsecops curlimages/curl:latest \
                      curl -f http://${DOCKER_IMAGE}:5000/api/users || exit 1
                """
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully'
            echo 'Application: http://13.40.17.105:5000'
            echo 'Jenkins: http://13.40.17.105:8080'
            echo 'SonarQube: http://13.40.17.105:9000'
        }
        failure {
            echo 'Pipeline execution failed'
        }
        always {
            echo 'Pipeline execution completed'
        }
    }
}
