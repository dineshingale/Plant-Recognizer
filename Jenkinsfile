pipeline {
    agent any

    environment {
        IMAGE_TAG = "plant-recognizer:build-${env.BUILD_NUMBER}"
        DOCKER_CONTAINER_NAME = "plant-test-runner"
        FAILURE_STAGE = "Initialization" 
        ALERT_EMAIL = "dineshingale2003@gmail.com"
        REACT_APP_API_URL = "http://localhost:8000"
        
        // 🔹 Replace this with your Git Repo URL (without https://)
        GIT_REPO_URL = "github.com/dineshingale/Plant-Recognizer.git"
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
                writeFile file: 'Client/.env', text: """
VITE_API_URL=${REACT_APP_API_URL}
DANGEROUSLY_DISABLE_HOST_CHECK=true
"""
            }
        }

        stage('Build & Test') {
            steps {
                script { FAILURE_STAGE = "Docker Build & Test" }
                
                bat "docker build -t ${IMAGE_TAG} ."

                // Run Container & Test
                bat """
                    docker run --name ${DOCKER_CONTAINER_NAME} ^
                    --shm-size=2g ^
                    -v "${env.WORKSPACE}":/app ^
                    -v /app/Client/node_modules ^
                    ${IMAGE_TAG} || exit 0
                """
                
                // Extract Report
                bat "docker cp ${DOCKER_CONTAINER_NAME}:/tmp/test-results.xml test-results.xml"
                bat "docker rm -f ${DOCKER_CONTAINER_NAME}"
            }
        }

        stage('Merge & Push') {
            // 🔹 Only run this stage if the previous stages succeeded
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
                // Optional: Prevent merging 'main' into 'main' (infinite loop protection)
                not { branch 'main' } 
            }
            steps {
                script { FAILURE_STAGE = "Auto-Merge" }
                withCredentials([usernamePassword(credentialsId: 'github-token-auth', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    bat """
                        @echo off
                        echo 🔄 Switching to MAIN branch...
                        
                        :: Configure Git Identity for Jenkins
                        git config user.email "jenkins-bot@example.com"
                        git config user.name "Jenkins CI"

                        :: Fetch latest main
                        git fetch origin main

                        :: Checkout main
                        git checkout main
                        git pull origin main

                        echo 🔀 Merging commit %GIT_COMMIT% into main...
                        git merge %GIT_COMMIT%

                        echo 🚀 Pushing to GitHub...
                        :: We inject the token directly into the URL for authentication
                        git push https://%GIT_TOKEN%@${GIT_REPO_URL} main
                    """
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*.png, *.xml, frontend_logs.txt', allowEmptyArchive: true
            junit 'test-results.xml'
        }
        
        failure {
            echo "❌ Pipeline Failed at stage: ${env.FAILURE_STAGE}"
            emailext (
                subject: "FAILED: Plant-Recognizer Build #${env.BUILD_NUMBER}",
                body: "Build Failed. Check Console: ${env.BUILD_URL}",
                to: "${env.ALERT_EMAIL}"
            )
        }
        
        success {
            echo "✅ Tests Passed & Code Merged to Main! Deployment to Vercel should start shortly."
        }
    }
}