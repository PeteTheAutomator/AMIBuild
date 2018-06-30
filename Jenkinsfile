node {
    stage('Preparation') {
        git 'https://github.com/PeteTheAutomator/AMIBuild.git'
    }
    stage('Build') {
        sh './build.py -p AMIBuild-Testing'
    }
}
