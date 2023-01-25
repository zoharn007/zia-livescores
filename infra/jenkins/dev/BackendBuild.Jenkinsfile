pipeline {
    agent any
    environment {
        REGISTRY_URL = "352708296901.dkr.ecr.eu-west-1.amazonaws.com"
        IMAGE_TAG = "0.0.$BUILD_NUMBER"
        IMAGE_NAME = "zia-backend"
//          on jenkins
        WORKSPACE = "/var/lib/jenkins/workspace/zia-dev/BackendBuild"
//         on jenkins agent
        WORKSPACE2 = "/home/ec2-user/workspace/zia-dev/BackendBuild"
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
        stage('Continue_Build') {
            steps {
                sh'''
                docker tag $IMAGE_NAME:$IMAGE_TAG $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG
                docker push $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG
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