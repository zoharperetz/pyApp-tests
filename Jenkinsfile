@NonCPS
def getParentBuild() {
  return currentBuild.rawBuild.getParent()
}

pipeline {
    agent {
      label 'build-agent' 
   }
   options {
      disableResume()
   }
    environment{
        REPO_NAME='python-app'
        ECR_URI='872444258103.dkr.ecr.us-east-1.amazonaws.com'
        VERSION_TAG=""

    }
    stages{
      stage('get version') {
        steps {
          script{            
            status_code=sh(script: 'git tag --contains HEAD', returnStatus: true)
            if (status_code == 0){
            
               VERSION_TAG=sh(script: 'git tag --contains HEAD', returnStdout: true).trim()
               echo "${VERSION_TAG}"

             }
             else{
               VERSION_TAG=${BUILD_NUMBER}
               echo "${VERSION_TAG}"
             }
           }
        }
     }
      stage('build & tests') {
         when {
            branch "development"
         }
         steps {
             sh 'docker build -t "${ECR_URI}/${REPO_NAME}" .'
             sh 'docker run -dit -p 5000:5000 --name weather-app "${ECR_URI}/${REPO_NAME}"'
             sh 'docker exec -dit weather-app bash python3 testApp.py'
             sh 'python3 testSelenium.py'
             sh "docker tag \"${ECR_URI}/${REPO_NAME}\" \"${ECR_URI}/${REPO_NAME}:${VERSION_TAG}\""

            
          
         }
      }
      
     stage('push to ECR') {
        when {
            branch "development"
        }
        steps {
           sh"""aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_URI}
           docker push "${ECR_URI}/${REPO_NAME}:${VERSION_TAG}"
           """
             
       }
    }
     stage('update version') {
        when {
            branch "development"
        }
        steps {
          script{
           dir('eks') {
             echo "${VERSION_TAG}"
             //sh(script: "sed -i 's/VERSION_TAG/\${VERSION_TAG}/g' weatherapp.yaml")
             sh "sed -i 's/VERSION_TAG/${VERSION_TAG}/g' weatherapp.yaml"
             //configFile = readFile('weatherapp.yaml')
             //updatedAppFile = configFile.replaceAll('VERSION_TAG', "${VERSION_TAG}")
             //writeFile(file: 'weatherapp.yaml', text: updatedAppFile)
             sh "cat weatherapp.yaml"
             
             
             }
         }
        }
     }
      stage('push changes') {
        when {
            branch "pre-prod"
        }
        steps {
          script{
             withCredentials([gitUsernamePassword(credentialsId: 'github-token', gitToolName: 'Default')]) {
                   //currentBuild.rawBuild.pipeline.disableResume()
                   sh 'git stash'
                   sh 'git checkout development'
                   sh 'git stash pop'
                   sh 'git add .'
                   sh 'git commit -m "Commit message from jenkins"'
                   sh 'git push origin development'
                   
                   //def parentBuild = currentBuild.rawBuild.getParent()
                   //parentBuild.pipeline.disableResume()
                   //sh 'git checkout pre-prod'
                   //sh 'git merge development'
                   //sh 'git tag "${VERSION_TAG}"'
                   //sh 'git push --tags' 
                   //sh 'git push origin pre-prod'
                   
            }
           }
        }
      }
      stage('Disable Jenkins pipeline') {
        when {
            branch "pre-prod"
        }
        steps{
          script{
             def parentBuild = getParentBuild()
             parentBuild.pipeline.disableResume()
           }
         }
     }
      stage('deploy to prod repo') {
          when {
            branch "development"
          }
          steps {
             withCredentials([gitUsernamePassword(credentialsId: 'github-token', gitToolName: 'Default')]) {
                sh 'git remote add prod-repo https://github.com/zoharperetz/prod.git'
                sh 'git fetch prod-repo'
                sh 'git stash'
                sh 'git checkout --track origin/development'
                sh 'git stash pop'
                sh 'git add .'
                sh 'git commit -m "Commit message from jenkins"'
                sh 'git push prod-repo development:main'
             }
         }
      }
       
   }
   post {        
      
        always {
            // Clean workspace here
            cleanWs()
            sh(script: 'docker rm -vf $(docker ps -a -q)')
            sh"""docker system prune --force
            """
        }
        
    }
    
}
