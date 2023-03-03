pipeline {
    agent {
  label 'build-agent'
}
    environment{
        repo_name='python-app'
        ecr_uri='872444258103.dkr.ecr.us-east-1.amazonaws.com'
        version_release = sh(script: "git describe --tags")


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
             echo "${version_release}"
             sh"""docker build -t "${ecr_uri}/${repo_name}":"${version_release}"
             aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ecr_uri}
             docker push "${ecr_uri}/${repo_name}":"${version_release}"
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
