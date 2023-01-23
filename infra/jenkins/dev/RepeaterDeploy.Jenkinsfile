pipeline {
    agent any
    environment {
        APP_ENV = "dev"
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
                ]) {
                    echo 'Deploy to EKS'
                    sh '''
                    K8S_CONFIGS=/var/lib/jenkins/workspace/zia_dev/RepeaterDeploy/infra/k8s
                    # replace placeholders in YAML k8s files
                    bash common/replaceInFile.sh $K8S_CONFIGS/repeater.yaml APP_ENV $APP_ENV
                    bash common/replaceInFile.sh $K8S_CONFIGS/repeater.yaml REPEATER_IMAGE $REPEATER_IMAGE_NAME
                    bash common/replaceInFile.sh $K8S_CONFIGS/repeater.yaml APIKEY $(echo -n $APIKEY | base64)
                    # apply the configurations to k8s cluster
                    pwd
                    /var/lib/jenkins/logs/kubectl apply -f $K8S_CONFIGS/repeater.yaml
                    '''
                    }
            }
        }
    }
}