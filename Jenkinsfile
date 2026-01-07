pipeline {
    agent any

    environment {
        // Global variables
        IMAGE_TAG = "plant-recognizer:build-${env.BUILD_NUMBER}"
        // Define as String to avoid Groovy styling warnings
        FAILURE_STAGE = "Initialization" 
        
        // Vercel Hook
        VERCEL_HOOK = "https://api.vercel.com/v1/integrations/deploy/prj_9VOoRKBHJtAtG3lTEPhsVUdIyjMf/UTSLCpjhHf"
        ALERT_EMAIL = "dineshingale2003@gmail.com"
        
        // For Usage in Jenkins Pipeline only (Docker Environment)
        // We override this to localhost because we are running the backend INSIDE the container now.
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
                // Note: Vite requires VITE_ prefix for client-side exposure
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

                // 2. Run Container (Mounting Project + Anonymous Volume for node_modules)
                // We use -v %CD%:/app to mount current code, 
                // BUT -v /app/Client/node_modules prevents local node_modules from conflicting
                bat """
                    docker run --rm ^
                    --shm-size=2g ^
                    -v "%CD%":/app ^
                    -v /app/Client/node_modules ^
                    ${IMAGE_TAG}
                """
            }
        }

        stage('Deploy') {
            steps {
                script { FAILURE_STAGE = "Deployment Trigger" }
                echo 'Tests Passed - Triggering Vercel Deployment...'
                
                // Using PowerShell to trigger webhook
                powershell """
                    \$response = Invoke-RestMethod -Uri '${VERCEL_HOOK}' -Method Post
                    Write-Output "Deployment Triggered: \$response"
                """
            }
        }
    }

    post {
        always {
            // Archive Test Artifacts (Screenshots, XML Validation)
            archiveArtifacts artifacts: '*.png, *.xml, frontend_logs.txt', allowEmptyArchive: true
            junit 'test-results.xml'
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
            echo "✅ Pipeline Succeeded!"
        }
    }
}
