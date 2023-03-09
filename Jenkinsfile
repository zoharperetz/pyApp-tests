pipeline {
    agent {
  label 'build-agent'
}
    environment{
        repo_name='python-app'
        ecr_uri='872444258103.dkr.ecr.us-east-1.amazonaws.com'
        release_version=sh(script: "git tag --points-at ${env.GIT_COMMIT}", returnStdout: true).trim()



    }
    stages {
       stage('build+tests') {
          when {
            branch "development"
          }
          steps {
             echo 'from dev'
             sh """docker build -t "${ecr_uri}/${repo_name}":"${BUILD_NUMBER}" .
             docker run -dit --name pyApp "${ecr_uri}/${repo_name}":"${BUILD_NUMBER}" 
             docker exec -dit pyApp bash python3 testApp.py
             python3 testSelenium.py
             echo "${release_version}"
             """
          
          }
       }
       stage('push-to-ECR') {
          when {
            branch "development"
          }
          steps {
             sh """aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ecr_uri}
             docker push "${ecr_uri}/${repo_name}":"${BUILD_NUMBER}"
             """
          
          }
       }
       
       stage('staging-tests') {
          when {
            branch "pre-prod"
          }
          steps {
             echo 'from pre'
          
          }
       }
       stage('main') {
          when {
            branch "main"
          }
          steps {
             echo 'from main'
          
          }
       }
       
    }
    post {
          always { 
            script{
               docker stop $(docker ps -aq)
               docker rm $(docker ps -aq)
            }
            
            
        } 
    
 }
}
