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

            post {
                // Always publish test results and archive artifacts
                always {
                    junit '**/test-results/*.xml'
                    archiveArtifacts artifacts: 'test-results/*.xml', fingerprint: true
                }
                // Optional email notification if there are changes
                changed {
                    emailext attachLog: true,
                             body: 'Please go to ${BUILD_URL} and verify the build',
                             compressLog: true,
                             subject: 'Job \'${JOB_NAME}\' (${BUILD_NUMBER}) is waiting for input',
                             to: 'avitaltests@gmail.com'
                }
            }
        }
    }
}
