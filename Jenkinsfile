pipeline {
    agent any

    environment {
        // Define environment variables
        NODE_VERSION = '20'
        PYTHON_VERSION = '3.10'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Setup & Check') {
            steps {
                script {
                    // Windows-specific python setup, adjust if running on Linux Jenkins agents
                    bat 'python -m pip install --upgrade pip'
                    bat 'pip install -r requirements.txt'
                    bat 'python -m compileall server.py'
                }
            }
        }

        stage('Frontend Setup & Build') {
            steps {
                dir('Client') {
                    script {
                        bat 'npm ci'
                        bat 'npm run lint'
                        bat 'npm run build'
                    }
                }
            }
        }

        stage('E2E Tests (Python/Selenium)') {
            steps {
                script {
                    // Start the frontend server in the background and run tests
                    // Note: In a real Jenkins env, you might use strict start-server-and-test or parallel stages
                    // For simplicity in this script, we assume a parallel execution strategy or background job
                    
                    parallel(
                        "Start Server": {
                            dir('Client') {
                                // Start preview server in background
                                bat 'start /B npm run preview' 
                                sleep 5 // Give it time to boot
                            }
                        },
                        "Run Tests": {
                            sleep 10 // Wait for server to definitely be up
                            bat 'pytest tests/test_e2e.py --junitxml=test-results.xml'
                        }
                    )
                }
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
            archiveArtifacts artifacts: 'Client/dist/**/*', fingerprint: true
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
