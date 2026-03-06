pipeline {
    agent any

    parameters {
        choice(
            name: 'BROWSERS',
            choices: ['all', 'chrome', 'firefox', 'edge'],
            description: 'Select browser(s) for tests. "all" runs Chrome, Firefox and Edge in parallel.'
        )
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
                script {
                    if (params.BROWSERS == 'all') {
                        // Run all three browsers in parallel — matches conftest.py params=["chrome","firefox","edge"]
                        parallel(
                            Chrome: {
                                bat "venv\\Scripts\\activate.bat && pytest -k chrome --junitxml=test-results/results-chrome.xml -v"
                            },
                            Firefox: {
                                bat "venv\\Scripts\\activate.bat && pytest -k firefox --junitxml=test-results/results-firefox.xml -v"
                            },
                            Edge: {
                                bat "venv\\Scripts\\activate.bat && pytest -k edge --junitxml=test-results/results-edge.xml -v"
                            }
                        )
                    } else {
                        // Run only the selected browser
                        bat "venv\\Scripts\\activate.bat && pytest -k ${params.BROWSERS} --junitxml=test-results/results-${params.BROWSERS}.xml -v"
                    }
                }
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
                    Browser(s): ${BROWSERS}
                ''',
                compressLog: true,
                subject: "Build '${env.JOB_NAME}' (#${env.BUILD_NUMBER}) ${currentBuild.currentResult}",
                to: 'avitaltests@gmail.com'
            )
        }
    }
}