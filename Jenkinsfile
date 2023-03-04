pipeline {
    agent {
  label 'build-agent'
}
    environment{
        repo_name='python-app'
        ecr_uri='872444258103.dkr.ecr.us-east-1.amazonaws.com'



    }
    stages {
       stage('hello') {
           steps{
              echo "hello"
             
           }
       }
       stage('build') {
          when {
            branch "development"
          }
          steps {
             echo 'from dev'
             sh"""docker build -t "${ecr_uri}/${repo_name}":"$(git rev-parse HEAD)-${BUILD_NUMBER}"
             aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ecr_uri}
             docker push "${ecr_uri}/${repo_name}":"$(git rev-parse HEAD)-${BUILD_NUMBER}"
             """
          
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
    
}
