pipeline {
    agent {
            docker {
            label 'jenkins-general-docker'
            image '352708296901.dkr.ecr.eu-west-1.amazonaws.com/ariel-jenkins-agent2:4'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    environment {
        REGISTRY_URL = "352708296901.dkr.ecr.eu-west-1.amazonaws.com"
        IMAGE_TAG = "0.0.$BUILD_NUMBER"
        IMAGE_NAME = "zia-backend"
//          on jenkins
        WORKSPACE2 = "/var/lib/jenkins/workspace/zia-prod/PullRequests"
//         on jenkins agent
        WORKSPACE = "/home/ec2-user/workspace/zia-prod/PullRequests"
        SNKY_BACKEND_BUILD_TEST = '/home/ec2-user/workspace/zia-prod/PullRequests/services/BackendBuild'
        SNKY_REPEATER_BUILD_TEST = '/home/ec2-user/workspace/zia-prod/PullRequests/services/RepeaterBuild'
    }
    stages {
        stage('Check Backend Build') {
            steps {
                withCredentials([string(credentialsId: 'Snyx', variable: 'Snyx')]){
                sh '''
                 snyk auth $Snyx
                 aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin $REGISTRY_URL
                 snyk container test 352708296901.dkr.ecr.eu-west-1.amazonaws.com/zia-backend:26commit001 --severity-threshold=critical
                '''
                }
                catch(eror) {
                    failure {
                        sh '''
                        echo 'Snyk test failed'
                        '''
                    }
                }
            }
        }
    }
}



pipeline {
    agent {
        docker {
            label 'jenkins-general-docker'
            image '352708296901.dkr.ecr.eu-west-1.amazonaws.com/ariel-jenkins-agent2:4'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    environment {
        REGISTRY_URL = "352708296901.dkr.ecr.eu-west-1.amazonaws.com"
        IMAGE_TAG = "0.0.$BUILD_NUMBER"
        IMAGE_NAME = "zia-backend"
        WORKSPACE2 = "/var/lib/jenkins/workspace/zia-prod/PullRequests"
        WORKSPACE = "/home/ec2-user/workspace/zia-prod/PullRequests"
        SNKY_BACKEND_BUILD_TEST = '/home/ec2-user/workspace/zia-prod/PullRequests/services/BackendBuild'
        SNKY_REPEATER_BUILD_TEST = '/home/ec2-user/workspace/zia-prod/PullRequests/services/RepeaterBuild'
    }
    stages {
        stage('Check Backend Build') {
            steps {
                withCredentials([string(credentialsId: 'Snyx', variable: 'Snyx')]){
                sh '''
                 snyk auth $Snyx
                 aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin $REGISTRY_URL
                 snyk container test 352708296901.dkr.ecr.eu-west-1.amazonaws.com/zia-backend:26commit001 --severity-threshold=critical
                '''
                }
                script {
                    def snykResult = sh script: 'snyk container test 352708296901.dkr.ecr.eu-west-1.amazonaws.com/zia-backend:26commit001 --severity-threshold=critical', returnStatus: true
                    if (snykResult == 0) {
                        echo 'Snyk test passed'
                    } else {
                        echo 'Snyk test failed'
                        currentBuild.result = 'FAILURE'
                        error('Snyk test failed')
                    }
                }
            }
        }
    }
}
