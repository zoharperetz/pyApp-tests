pipeline {
    agent {
  label 'build-agent'
}
    environment{
        repo_name='weatherapp'
        ecr_uri='872444258103.dkr.ecr.us-east-1.amazonaws.com'
    }
    stages {
       stage('hello') {
           steps{
              echo "hello"
             
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
       stage('pre') {
          when {
            branch "pre-prod"
          }
          steps {
             echo 'from preprod'
          
          }
       }
       
    }
    
}
