pipeline {
    agent {
  label 'build-agent'
}
    environment{
        REPO_NAME='python-app'
        ECR_URI='872444258103.dkr.ecr.us-east-1.amazonaws.com'
        VERSION_TAG=""

    }
    stages{
    
      stage('build & tests') {
         when {
            branch "development"
         }
         steps {
             sh """docker build -t "${ECR_URI}/${REPO_NAME}" .
             docker run -dit -p 5000:5000 --name weather-app "${ECR_URI}/${REPO_NAME}"
             docker exec -dit weather-app bash python3 testApp.py
             python3 testSelenium.py
             """
          
         }
      }
      stage('versioning') {
        when {
           branch "development"
        }
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
             docker tag "${ECR_URI}/${REPO_NAME}" "${ECR_URI}/${REPO_NAME}:${VERSION_TAG}"

           }
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
       
       stage('staging-tests') {
          when {
            branch "pre-prod"
          }
          steps {
             sh"""kubectl run weather-app --image="${ECR_URI}/${REPO_NAME}:${VERSION_TAG}" --namespace=staging
             """

          }
            
      }
      stage('deploy') {
          when {
            branch "main"
          }
          steps {
             echo "hello from main"
          
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
