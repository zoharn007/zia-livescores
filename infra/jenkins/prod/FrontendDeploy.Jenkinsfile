pipeline {
    agent {
        docker {
            label 'jenkins-general-docker'
            image '352708296901.dkr.ecr.eu-west-1.amazonaws.com/ariel-jenkins-agent2:4'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        APP_ENV = "prod"
//          on jenkins
        WORKSPACE2 = "/var/lib/jenkins/workspace/zia-prod/FrontendDeploy"
//         on jenkins agent
        WORKSPACE = "/home/ec2-user/workspace/zia-prod/FrontendDeploy"
    }

    parameters {
        string(name: 'FRONTEND_IMAGE_NAME')
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
                K8S_CONFIGS=$WORKSPACE/infra/k8s

                # replace placeholders in YAML k8s files
                bash common/replaceInFile.sh $K8S_CONFIGS/frontend.yaml APP_ENV $APP_ENV

                # apply the configurations to k8s cluster

                bash common/replaceInFile.sh $K8S_CONFIGS/frontend.yaml FRONTEND_IMAGE $FRONTEND_IMAGE_NAME
                /usr/local/bin/kubectl apply -f $K8S_CONFIGS/frontend.yaml
                '''
            }
        }
    }
}