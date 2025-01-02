pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/AvitalZemnucha/sakila-e2e-testing.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install dependencies using pip
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Run tests using pytest and generate JUnit report
                bat 'pytest --junitxml=test-results/results.xml'
            }
        }
    }

    post {
        always {
            // Publish test results and archive artifacts
            junit '**/test-results/*.xml'
            archiveArtifacts artifacts: 'test-results/*.xml', fingerprint: true
        }
        changed {
            // Send email notification if build status changes
            emailext(
                attachLog: true,
                body: '''
                    Please check the Jenkins build:
                    Build URL: ${BUILD_URL}
                    Build Status: ${BUILD_STATUS}
                ''',
                compressLog: true,
                subject: 'Build \'${JOB_NAME}\' (#${BUILD_NUMBER}) Status Changed',
                to: 'avitaltests@gmail.com'
            )
        }
    }
}
