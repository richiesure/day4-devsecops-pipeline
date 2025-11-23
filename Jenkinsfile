pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "devsecops-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo '📦 Installing Python dependencies...'
                sh '''
                    python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo '🧪 Running unit tests with coverage...'
                sh '''
                    python3 -m pytest tests/ -v --junitxml=test-results.xml --cov=. --cov-report=xml --cov-report=html
                    echo "✅ All tests passed!"
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh """
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    echo "✅ Docker image built: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                """
            }
        }
        
        stage('Security Scan') {
            steps {
                echo '🔒 Running Trivy security scan...'
                sh """
                    echo "Pulling Trivy scanner..."
                    docker pull aquasec/trivy:latest || true
                    echo "Scanning image for vulnerabilities..."
                    docker run --rm aquasec/trivy:latest image ${DOCKER_IMAGE}:${DOCKER_TAG} || echo "Security scan completed with warnings"
                """
            }
        }
        
        stage('Deploy') {
            steps {
                echo '🚀 Deploying application...'
                sh """
                    # Stop and remove old container if exists
                    docker rm -f ${DOCKER_IMAGE} || true
                    
                    # Run new container
                    docker run -d \
                      --name ${DOCKER_IMAGE} \
                      -p 5000:5000 \
                      ${DOCKER_IMAGE}:${DOCKER_TAG}
                    
                    # Wait for app to start
                    sleep 5
                    
                    # Verify deployment
                    docker ps | grep ${DOCKER_IMAGE}
                    
                    echo "✅ Application deployed successfully!"
                    echo "🌐 Access the application at: http://13.40.17.105:5000"
                """
            }
        }
        
        stage('Smoke Test') {
            steps {
                echo '✅ Running smoke tests...'
                sh '''
                    echo "Testing application endpoints..."
                    curl -f http://localhost:5000/ || exit 1
                    curl -f http://localhost:5000/health || exit 1
                    curl -f http://localhost:5000/api/users || exit 1
                    echo "✅ All smoke tests passed!"
                '''
            }
        }
    }
    
    post {
        success {
            echo ''
            echo '✅ =========================================='
            echo '✅    PIPELINE COMPLETED SUCCESSFULLY!     '
            echo '✅ =========================================='
            echo '✅ Application URL: http://13.40.17.105:5000'
            echo '✅ =========================================='
            echo ''
        }
        failure {
            echo ''
            echo '❌ =========================================='
            echo '❌         PIPELINE FAILED!                 '
            echo '❌ =========================================='
            echo ''
        }
        always {
            echo '📊 Pipeline execution completed.'
        }
    }
}
