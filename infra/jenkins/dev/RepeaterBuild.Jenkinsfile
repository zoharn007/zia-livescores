pipeline {
    agent any
    environment {
        REGISTRY_URL = "352708296901.dkr.ecr.eu-west-1.amazonaws.com"
        IMAGE_TAG = "0.0.$BUILD_NUMBER"
        IMAGE_NAME = "zia-repeater"
        WORKSPACE = "/var/lib/jenkins/workspace/zia_dev/RepeaterBuild"
        WORKSPACE2 = "/home/ec2-user/workspace/zia_dev/RepeaterBuild"
    }
    stages {
        stage('Build') {
            steps {
                withCredentials([
                    file(credentialsId: 'API2', variable: '.env')
                ]) {
                sh '''
                    pwd
                    cd $WORKSPACE
                    docker build -t $IMAGE_NAME:$IMAGE_TAG . -f services/repeater/Dockerfile
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
                build job: 'RepeaterDeploy', wait: false, parameters: [
                    string(name: 'REPEATER_IMAGE_NAME', value: "${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}")
                    ]
                }
            }
        }
    }
}