properties([parameters([string('BACKEND_IMAGE_NAME')])])

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

//     parameters {
//         string(name: 'BOT_IMAGE_NAME')
//     }

    stages {
        stage('Backend Deploy') {
            steps {
                withCredentials([
                    file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')
                ]) {
                    sh '''
                    K8S_CONFIGS=infra/k8s

                    # replace placeholders in YAML k8s files
                    bash common/replaceInFile.sh $K8S_CONFIGS/backend.yaml APP_ENV $APP_ENV
                    bash common/replaceInFile.sh $K8S_CONFIGS/backend.yaml BACKEND_IMAGE $BACKEND_IMAGE_NAME

                    # apply the configurations to k8s cluster
                    kubectl apply --kubeconfig ${KUBECONFIG} -f $K8S_CONFIGS/backend.yaml
                    '''
                }
            }
        }
    }
}