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
             sh """docker build -t "${ecr_uri}/${repo_name}":"${BUILD_NUMBER}" .
             aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ecr_uri}
             docker push "${ecr_uri}/${repo_name}":"${BUILD_NUMBER}"
             """
          
          }
       }
       stage('test') {
          when {
            branch "development"
          }
          steps {
             sh """docker run -dit --name pyApp "${ecr_uri}/${repo_name}":"${BUILD_NUMBER}" 
             docker exec -dit pyApp bash python3 testApp.py
             """
          
          }
       }
       
       stage('staging-tests') {
          when {
            branch "pre-prod"
          }
          steps {
             withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', passwordVariable: 'password', usernameVariable: 'username')]) {
             sh """docker login -u ${username} -p ${password}
             """
            }
            sh """docker-compose up -d
            docker-compose exec -T selenium python3 testSelenium.py
            """
          }
       }
       stage('main') {
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
            sh """docker rm -f \$(docker ps -aq)
            docker rmi -f \$(docker images -aq)
            """
            
        } 
    
 }
}
