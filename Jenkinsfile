pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Select browser for tests')
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/AvitalZemnucha/sakila-e2e-testing.git', branch: 'main'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate.bat && python -m pip install --upgrade pip'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat "venv\\Scripts\\activate.bat && pytest --browser=${params.BROWSER} --junitxml=test-results/results.xml"
            }
        }
    }

    post {
        always {
            junit '**/test-results/*.xml'
            archiveArtifacts artifacts: 'test-results/*.xml', fingerprint: true
        }
        success {
            echo 'All tests passed successfully!'
        }
        failure {
            echo 'Some tests failed. Please check the results.'
        }
        changed {
            emailext(
                attachLog: true,
                body: '''
                    Please check the Jenkins build:
                    Build URL: ${BUILD_URL}
                    Build Status: ${currentBuild.currentResult}
                ''',
                compressLog: true,
                subject: "Build '${env.JOB_NAME}' (#${env.BUILD_NUMBER}) ${currentBuild.currentResult}",
                to: 'avitaltests@gmail.com'
            )
        }
    }
}
