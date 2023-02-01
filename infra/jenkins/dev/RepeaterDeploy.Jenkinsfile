pipeline {
    agent {
            docker {
            label 'jenkins-general-docker'
            image '352708296901.dkr.ecr.eu-west-1.amazonaws.com/ariel-jenkins-agent2:4'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    environment {
        APP_ENV = "dev"
//          on jenkins
        WORKSPACE2 = "/var/lib/jenkins/workspace/zia-dev/RepeaterDeploy"
//         on jenkins agent
        WORKSPACE = "/home/ec2-user/workspace/zia-dev/RepeaterDeploy"
    }

    parameters {
        string(name: 'REPEATER_IMAGE_NAME')
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
                withCredentials([
                    string(credentialsId: 'apikey', variable: 'APIKEY'),
                    string(credentialsId: 'apisecret', variable: 'APISECRET'),
                ]) {
                    echo 'Deploy to EKS'
                    sh '''
                    K8S_CONFIGS=$WORKSPACE/infra/k8s
                    # replace placeholders in YAML k8s files
                    bash common/replaceInFile.sh $K8S_CONFIGS/repeater.yaml APP_ENV $APP_ENV
                    bash common/replaceInFile.sh $K8S_CONFIGS/repeater.yaml REPEATER_IMAGE $REPEATER_IMAGE_NAME
                    bash common/replaceInFile.sh $K8S_CONFIGS/repeater.yaml APIKEY $(echo -n $APIKEY | base64)
                    bash common/replaceInFile.sh $K8S_CONFIGS/repeater.yaml APISECRET $(echo -n $APISECRET | base64)
                    # apply the configurations to k8s cluster
                    pwd
                    /usr/local/bin/kubectl apply -f $K8S_CONFIGS/repeater.yaml
                    '''
                    }
            }
        }
    }
}