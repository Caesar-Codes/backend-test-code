pipeline {
    agent any

    environment {
        EC2_IP = credentials('EC2_IP')
        EC2_USER = credentials('EC2_USER')
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
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

        stage('Build Backend') {
            steps {
                dir('server') {
                    sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                        pip3 install -r requirements.txt
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sshagent(['EC2_SSH_KEY']) {
                    sh """
                        # Copy frontend build files
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} 'sudo mkdir -p /usr/share/nginx/html'
                        scp -o StrictHostKeyChecking=no -r client/build/* ${EC2_USER}@${EC2_IP}:/usr/share/nginx/html/
                        
                        # Copy backend files
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} 'mkdir -p ~/backend-test-code/server'
                        scp -o StrictHostKeyChecking=no -r server/* ${EC2_USER}@${EC2_IP}:~/backend-test-code/server/
                        
                        # Execute commands on remote server
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} '
                            cd ~/backend-test-code/server
                            python3 -m venv venv
                            source venv/bin/activate
                            pip3 install -r requirements.txt
                            sudo systemctl restart backend
                            sudo systemctl restart nginx
                        '
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Application deployed successfully.'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
    }
}
