pipeline {
    agent any

    environment {
        APP_ENV = "dev"
    }

    parameters {
        string(name: 'BACKEND_IMAGE_NAME')
    }

    stages {
        stage('Example Build') {
            steps {
                echo 'Hello, Maven'
            }
        }
        stage('Example Test') {
            steps {
                echo 'Hello, JDK'
            }
        }
    }
}