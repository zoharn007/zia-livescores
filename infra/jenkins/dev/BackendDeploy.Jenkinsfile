pipeline {
    agent any

    environment {
        APP_ENV = "dev"
    }

    parameters {
        string(name: 'BACKEND_IMAGE_NAME')
    }

    stages {
        stage('Backend Deploy') {
            steps {
                   {
                    sh '''
                    aws eks --region eu-west-1 update-kubeconfig --name zia-eks
                    '''
                }
            }
        }
    }
}