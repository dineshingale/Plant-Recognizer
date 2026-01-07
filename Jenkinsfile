pipeline {
    agent any

    environment {
        // Global variables
        IMAGE_TAG = "plant-recognizer:build-${env.BUILD_NUMBER}"
        DOCKER_CONTAINER_NAME = "plant-test-runner"
        
        // Define as String to avoid Groovy styling warnings
        FAILURE_STAGE = "Initialization" 
        
        // ALERT EMAIL
        ALERT_EMAIL = "dineshingale2003@gmail.com"
        
        // Backend runs locally inside the container (localhost inside Docker)
        REACT_APP_API_URL = "http://localhost:8000"
    }

    stages {
        stage('Checkout') {
            steps {
                script { FAILURE_STAGE = "Git Checkout" }
                checkout scm
            }
        }

        stage('Configuration') {
            steps {
                script { FAILURE_STAGE = "Environment Setup" }
                echo 'Creating .env file for Docker container...'
                
                // Injecting Environment Variables for Vite
                // We point the API to localhost because both Frontend and Backend share the container network
                writeFile file: 'Client/.env', text: """
VITE_API_URL=${REACT_APP_API_URL}
DANGEROUSLY_DISABLE_HOST_CHECK=true
"""
            }
        }

        stage('Build & Test') {
            steps {
                script { FAILURE_STAGE = "Docker Build & Test" }
                
                // 1. Build Docker Image
                bat "docker build -t ${IMAGE_TAG} ."

                // 2. Run Container (Named, No --rm)
                // We use || exit 0 to ensure the pipeline continues even if tests fail (so we can extract the report)
                // We mount ${env.WORKSPACE} to /app so we can map files back if needed, but rely on docker cp for extraction
                bat """
                    docker run --name ${DOCKER_CONTAINER_NAME} ^
                    --shm-size=2g ^
                    -v "${env.WORKSPACE}":/app ^
                    -v /app/Client/node_modules ^
                    ${IMAGE_TAG} || exit 0
                """
                
                // 3. Extract Test Results (Bypassing Windows Permission Issues)
                // This copies the file from the Linux container to the Windows host
                bat "docker cp ${DOCKER_CONTAINER_NAME}:/tmp/test-results.xml test-results.xml"
                
                // 4. Cleanup Container
                bat "docker rm -f ${DOCKER_CONTAINER_NAME}"
            }
        }

        // ❌ DEPLOY STAGE REMOVED
        // Deployment is now handled automatically by Vercel when you merge this PR to 'main'.
    }

    post {
        always {
            // Read the XML report we extracted in step 3
            junit 'test-results.xml'
            
            // Archive Test Artifacts (Screenshots, XML, logs)
            archiveArtifacts artifacts: '*.png, *.xml, frontend_logs.txt', allowEmptyArchive: true
        }
        
        failure {
            echo "❌ Pipeline Failed at stage: ${env.FAILURE_STAGE}"
            emailext (
                subject: "FAILED: Plant-Recognizer Build #${env.BUILD_NUMBER}",
                body: """
<html>
<body>
    <h2 style="color:red;">❌ Build Failed</h2>
    <p><b>Stage:</b> ${env.FAILURE_STAGE}</p>
    <p><b>Check Console:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
    <p>See attached screenshots/logs for details.</p>
</body>
</html>
""",
                to: "${env.ALERT_EMAIL}",
                mimeType: 'text/html',
                attachLog: true
            )
        }
        
        success {
            echo "✅ Integration Tests Passed! You are safe to merge this Pull Request."
        }
    }
}