pipeline {
    agent {
      node {
        label "master"
      } 
    }

    stages {
      stage('Getting Updates') {
        steps {
          git branch: 'main',
              credentialsId: 'b09fb582-bfa5-4fba-8e28-22b35f468fb2', url: 'https://github.com/Wr-036-DevOps/Ak-image-downloader-lambda.git'
        }
      }

      stage('Testing') {
        steps {
          sh '/usr/local/bin/test/go test -v terraform_infr_test.go -timeout 30m'
        }
      }

      stage('Terraform Init & Plan') {
        steps {
          sh '/usr/local/bin/terraform init'
          sh '/usr/local/bin/terraform plan'
        }      
      }

      stage('Approve Deployment') {
        steps {
          script {
            def userInput = input(id: 'confirm', message: 'Apply Terraform?', parameters: [ [$class: 'BooleanParameterDefinition', defaultValue: false, description: 'Apply terraform', name: 'confirm'] ])
          }
        }
      }

      stage('Terraform Apply') {
        steps {
          sh '/usr/local/bin/terraform apply -auto-approve'
        }
      }
    } 
  }

