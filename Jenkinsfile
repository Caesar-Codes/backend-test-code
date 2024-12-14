pipeline {
    agent any
    
    environment {
        PROJECT_DIR = '/home/ec2-user/backend-test-code'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Clean workspace
                cleanWs()
                // Checkout from your repository
                git branch: 'main', url: 'https://github.com/Caesar-Codes/backend-test-code.git'
            }
        }
        
        stage('Build Frontend') {
            steps {
                dir('client') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
        
        stage('Deploy Frontend') {
            steps {
                sh 'sudo cp -r client/build/* /usr/share/nginx/html/'
            }
        }
        
        stage('Deploy Backend') {
            steps {
                dir('server') {
                    sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install -r requirements.txt
                        sudo systemctl restart backend
                    '''
                }
            }
        }
        
        stage('Restart Services') {
            steps {
                sh '''
                    sudo systemctl restart nginx
                    sudo systemctl restart backend
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}