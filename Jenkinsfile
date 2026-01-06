pipeline {
    agent any

    environment {
        // Define environment variables
        NODE_VERSION = '20'
        PYTHON_VERSION = '3.10'
    }

    triggers {
        pollSCM('H/2 * * * *') // Poll every 2 minutes for changes
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test with Docker') {
            steps {
                script {
                    bat 'docker-compose -f docker-compose.ci.yml up --build --exit-code-from test-runner'
                }
            }
        }
    }

    post {
        always {
            // Bring down containers
            bat 'docker-compose -f docker-compose.ci.yml down'
            
            // Archive results (will need to extract them from docker volume if strictly isolated, 
            // but since we volume mount .:/app, the XML depends on file permissions. 
            // Assuming host mount works on Windows Docker Desktop).
            junit 'test-results.xml'
        }
        success {
            echo 'Pipeline executed successfully!'
            // mail to: 'your-email@example.com',
            //      subject: "Build Success: ${currentBuild.fullDisplayName}",
            //      body: "Good news, the build passed!"
        }
        failure {
            echo 'Pipeline failed.'
             // mail to: 'your-email@example.com',
             //      subject: "Build Failed: ${currentBuild.fullDisplayName}",
             //      body: "Something went wrong. Check logs at ${env.BUILD_URL}"
        }
    }
}
