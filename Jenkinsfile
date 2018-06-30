env.AWS_ACCESS_KEY_ID=env.ACCESS_KEY
env.AWS_SECRET_ACCESS_KEY=env.SECRET_KEY
env.AWS_DEFAULT_REGION=env.REGION

node {
    stage('Preparation') { // for display purposes
        git 'https://github.com/PeteTheAutomator/AMIBuild.git'
    }
    stage('Setup CodeBuild Environment') {
        dir('terraform') {
            sh 'terraform init'
            sh 'terraform apply -auto-approve'
        }
   }
   stage('Build') {
       sh './build.py -p AMIBuild-Testing'
   }
}
