// Jenkinsfile
pipeline {
    agent any

    environment {
        EC2_IP = credentials('44.223.21.213')
        EC2_USER = credentials('EC2_USER')    // Should be 'ec2-user' for Amazon Linux
        SSH_KEY = credentials('-----BEGIN RSA PRIVATE KEY-----
MIIEpgIBAAKCAQEAwNWCQdBeVG+j04GGG42eYVGS1f+N1dFhLksUF3C3OiV4SSGQ
Jsnwycmt49StUGxpzZFIlmoa/MmBMC/M3uPCCJKJjUEa9XTsEOgTLYrCIsJoivm6
JPlAVF4+1SZjEB5XRpQQTyUdBCsv2MDNUsyURGjkkys+slEy/SyvXmI515ZbB7CU
5SHB8bjCCflmkNIo5U/uDHB+5/v34m4HSRuLSDs0sPkhbCYBzWl2bT0qObOAiCQj
4hIvWj9GTvXh9yxUQiHJvrhLgveyUDr1q2rqvoovJ2LibFGuPYEpa9k4zmatxT5d
M1Xo2Bdn4ilgQ8e1hY7ZPGCjUhvry8W9VAgaVQIDAQABAoIBAQCbuA8PDLAQKXM3
aoIcn/lFB3W3AD7Oat26X4CjCS+9ceK307WvzSV4HjghIm6u4k1yZp8icB7JAgQk
IIWlfHEFMSiI/AlELB4x7OcHwOTS4wE/MTkDgJBVUSIWSIB41LeP1CNzdjn/Usy5
kcB8253jvHzQ53wizXWKg1o+sr2Y/HbxTFfpjSL0cniAP5RlzJj1eXmLXOqBtAaO
bA+9im8da+t99vbkwnA89wEaNyL+lJc/ZUG8FAUtEBcZ6SEQlu2iF7tL2sQCSQjH
mRTTDL8yyKpfPYUQgfi52Z92blnTW6hdpe7PcFMNkZhzXEhm3z9kKXhwJS88zqHp
EeNaRiXlAoGBAPH6JwQDcwpVMPZBh+3sx4rAgUahwWRi8w6+d1a3d2xN4Fcg4dyD
Wnemu8LAzS1QTw9hM7uTZNjXrY9VGmNBbvIg5MkfC1UAMeZLmKEUL6+PRWE76R0W
UbhK7b6S0OoX+gBbdL40F0lZDwAYjqv3CimxYF+KlEtLiTUc/ncSaP8vAoGBAMwC
S1bHBjwKvBTtihqkZQWLNETvxxx/+3ATyjI7f8VfweEW+XaC8iU+q4FjwJWppQn9
Jd9g7dnEetV7/LFhkUHU5oGcMA1aF2j/SiaZDV+IpE9DOmbeq54ulazCah6c24TJ
73wOWIOnWkylZ2Rqz2xcWsz7y4FSLyt+RtC2EL27AoGBAKaqujzVc2NmkjbLpCiI
slgrh99ygpX2YZuCLQiZjbQXX7Ijf+42uxU2zpSx36CadBoPxWYpe4iv5WeYInjD
FPvJFExDCbceT0BkSViJYt71O8BhV4slWFwrn91nmmXi5dthIuPvVSq8IMzcHUjs
+x8EgXDNLp8+A9+FfO/eylsZAoGBAKQ6vJeRBI3VPm/CgcjMyp5Z36wXMrzYsnsZ
E0644zTqz1L6gbxL0c710m8I9IIG3VtbNN/MUe1a5F9zvoq1NpA+aYmxSGWXPv1B
dln4H/HmOA+u2Rby7kkay1cV8wPN1lHhli7SBaOGV4UYKlGGQpDDED2v/bWPiXWD
5FIkHvn9AoGBAKUsLXYUS4Nxt8t53CVcVqyfJx99DtbZRuocKo8E1NKXc8/5Ut9V
m/Y5Kl7KlRyZ0VWR7ESuPJGZIaQbMA/e5y8FqMhXddTlxM1H1xTjhqQK7KwQ9VHZ
d1Wqi2074LzBKmXvTaRH+DL8GBGCcMm4MJQc8gcgv3FtRd1UqQR4kEu8
-----END RSA PRIVATE KEY-----
')
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
                script {
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
