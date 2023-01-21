pipeline {
    agent any
    environment {
    REGISTRY_URL = "352708296901.dkr.ecr.eu-west-1.amazonaws.com"
    IMAGE_TAG = "0.0.$BUILD_NUMBER"
    IMAGE_NAME = "zia-backend"
    WORKSPACE2 = "/var/lib/jenkins/workspace/zia_dev/BackendBuild"
    WORKSPACE = "/home/ec2-user/workspace/zia_dev/BackendBuild"
    }
    stages {
        stage('Build') {
            steps {
                sh '''
                    pwd
                    cd $WORKSPACE
                    docker build -t $IMAGE_NAME:$IMAGE_TAG . -f services/backend/Dockerfile
                '''
            }
        }
    }
}