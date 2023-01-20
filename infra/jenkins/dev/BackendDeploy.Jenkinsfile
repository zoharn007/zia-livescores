properties([parameters([string('BACKEND_IMAGE_NAME')])])

pipeline {
    agent any

    environment {
        APP_ENV = "dev"
    }

//     parameters {
//         string(name: 'BOT_IMAGE_NAME')
//     }

    stages {
        stage('Backend Deploy') {
            steps {
                 aws eks --region eu-west-1 update-kubeconfig --name zia-eks
                 {
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
}