pipeline {
    agent {
        docker {
        label 'jenkins-general-docker'
        image '352708296901.dkr.ecr.eu-west-1.amazonaws.com/zoharn-jenkins-agent:1'
        args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Unittest Bot') {
            steps {
                echo 'testing bot...'
            }
        }
        stage('Unittest Worker') {
            steps {
                echo 'testing worker...'
            }
        }
        stage('Linting test') {
            steps {
              echo 'code linting'
            }
        }
    }
}