pipeline {
    agent {
        docker {
        label 'jenkins-general-docker'
        image '352708296901.dkr.ecr.eu-west-1.amazonaws.com/zoharn-jenkins-agent:1'
        args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        APP_ENV = "dev"
    }

    parameters {
        string(name: 'BACKEND_IMAGE_NAME')
    }

    stages {
        stage('Connect to EKS') {
            steps {
                echo 'Connect to EKS'
                sh 'aws eks --region eu-west-1 update-kubeconfig --name zia-eks'
            }
        }
        stage('Deploy to EKS') {
            steps {
                echo 'Deploy to EKS'
                sh '''
                K8S_CONFIGS=infra/k8s
                # replace placeholders in YAML k8s files
                bash common/replaceInFile.sh $K8S_CONFIGS/backend.yaml APP_ENV $APP_ENV
                bash common/replaceInFile.sh $K8S_CONFIGS/backend.yaml BACKEND_IMAGE $BACKEND_IMAGE_NAME
                # apply the configurations to k8s cluster
                kubectl apply -f $K8S_CONFIGS/backend.yaml
                '''
            }
        }
    }
}