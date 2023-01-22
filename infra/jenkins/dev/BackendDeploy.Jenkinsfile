pipeline {
    agent any

    environment {
        APP_ENV = "dev"
    }

    parameters {
        string(name: 'BACKEND_IMAGE_NAME')
    }

    stages {
        stage('Connect to EKS') {
            steps {
                withCredentials([
                    file(credentialsId: 'kubeconfig2', variable: 'KUBECONFIG')
                ]) {
                    echo 'Connect to EKS'
                    sh 'aws eks --region eu-west-1 update-kubeconfig2 --name zia-eks'
                    sh '''
                    # replace placeholders in YAML k8s files
                    K8S_CONFIGS=/var/lib/jenkins/workspace/zia_dev/BackendDeploy/infra/k8s
                    bash common/replaceInFile.sh $K8S_CONFIGS/backend.yaml APP_ENV $APP_ENV
                    bash common/replaceInFile.sh $K8S_CONFIGS/backend.yaml BACKEND_IMAGE $BACKEND_IMAGE_NAME
                    # apply the configurations to k8s cluster
                    pwd
                    /var/lib/jenkins/logs/kubectl apply --kubeconfig ${KUBECONFIG} -f $K8S_CONFIGS/backend.yaml
                    '''
                }
            }
        }
    }
}