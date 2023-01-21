pipeline {
    agent any

    options {
    buildDiscarder(logRotator(daysToKeepStr: '30'))
    disableConcurrentBuilds()
    timestamps()
    }

    environment {
    REGISTRY_URL = "352708296901.dkr.ecr.eu-west-1.amazonaws.com"
    IMAGE_TAG = "0.0.$BUILD_NUMBER"
    IMAGE_NAME = "zia-backend"
    WORKSPACE = "/var/lib/jenkins/workspace/zia_dev/BackendBuild"
    WORKSPACE2 = "/home/ec2-user/workspace/zia_dev/BackendBuild"
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                cd $WORKSPACE
                pwd
                '''
            }
        }

        stage('Continue_Build') {
            steps {
                sh'''
                cd $WORKSPACE
                pwd
                '''
            }
            post {
                always {
                sh '''
                docker image prune -af --filter "until=24h"
                '''
                }
            }
        }

        stage('Trigger Deploy') {
            steps {
                build job: 'BackendDeploy', wait: false, parameters: [
                    string(name: 'BACKEND_IMAGE_NAME', value: "${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}")
                ]
            }
        }
    }
}