pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            echo 'Build step'
          }
        }
        stage('Build 2') {
          steps {
            echo 'Inside Build 2'
          }
        }
      }
    }
    stage('Testing') {
      parallel {
        stage('Unit tests') {
          steps {
            echo 'Unit tests'
          }
        }
        stage('Integration tests') {
          steps {
            echo 'Integration tests'
          }
        }
      }
    }
    stage('Dev') {
      steps {
        echo 'deploy Dev'
      }
    }
    stage('Staging') {
      steps {
        echo 'deploy Staging'
      }
    }
  }
}