pipeline {
    agent {
        docker {
        label 'jenkins-general-docker'
        image '352708296901.dkr.ecr.eu-west-1.amazonaws.com/zoharn-jenkins-agent:1'
        args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    options {
    buildDiscarder(logRotator(daysToKeepStr: '30'))
    disableConcurrentBuilds()
    timestamps()
    }

    environment {
    REGISTRY_URL = "352708296901.dkr.ecr.eu-west-1.amazonaws.com"
    IMAGE_TAG = "0.0.$BUILD_NUMBER"
    IMAGE_NAME = "zia-backend"
    WORKSPACE = "/home/ec2-user/workspace/zia-dev/BackendBuild/"
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin $REGISTRY_URL
                cd $WORKSPACE
                docker build -t $IMAGE_NAME:$IMAGE_TAG . -f services/backend/Dockerfile
                '''
            }
        }

        stage('Snyx Check') {
            steps {
                withCredentials([string(credentialsId: 'Snyx', variable: 'SNYK_TOKEN')]) {
                    sh 'snyk container test $IMAGE_NAME:$IMAGE_TAG --severity-threshold=critical --file=/home/ec2-user/workspace/zia-dev/BackendBuild/services/backend/Dockerfile'
                }
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