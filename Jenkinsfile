def getRepo(String branch) {
    def finalBranch = branch.replace('origin/', '')
    def repo
    switch(finalBranch) {
      case 'master':
              repo = 'maven-releases'
              break
          case 'homologacao':
              repo = 'maven-homologacao'
              break
          default:
              repo = 'maven-desenv'
    }
    return repo
}

def getInventory(String branch) {
  return branch.endsWith('homologacao') ? 'Homologacao' : 'Desenvolvimento'
}

pipeline {
    agent any

    environment {
        VERSION = readJSON('./metadata.json')
        REPOSITORY = getRepo("${GIT_BRANCH}")
        INVENTORY = getInventory("${GIT_BRANCH}")
        ROCKET_TOKEN = 'us9nRmnbwdgkENRYX/8WzbpdHarMaooQt8QgjQ4qup8jfacSvzyteQvTMT5XiPWkPe'
    }

    stages {
        stage('Build') {
            steps {
                rocketSend message: "Build iniciada", attachments: [[title: "#${env.BUILD_NUMBER}", titleLink: "${env.BUILD_URL}", text: "${env.JOB_NAME} - ${GIT_BRANCH}"]], rawMessage: true, webhookToken: "${ROCKET_TOKEN}"
                echo "${VERSION}"
            }
        }
    }

    post {
        success {
            rocketSend message: "Build Finalizada", attachments: [[title: "#${env.BUILD_NUMBER}", titleLink: "${env.BUILD_URL}", text: "${env.JOB_NAME} - ${GIT_BRANCH}", color: "green"]], rawMessage: true, webhookToken: "${ROCKET_TOKEN}"
        }

        failure {
            rocketSend message: "Falha na build", attachments: [[title: "#${env.BUILD_NUMBER}", titleLink: "${env.BUILD_URL}", text: "${env.JOB_NAME} - ${GIT_BRANCH}", color: "red"]], rawMessage: true, webhookToken: "${ROCKET_TOKEN}"
        }
    }
}