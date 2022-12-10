pipeline {
    agent {
      node {
        label "master"
      } 
    }
    //Setting my default path
    environment {
        PATH = "/usr/local/bin:${env.PATH}"
    }
    //Ensuring go is installed 
    tools {go '1.19'}

      stage('Testing') {
        steps {
          sh '''
              cd ./test 
              go test -v terraform_infr_test.go -timeout 30m
            '''
        }
      }

      stage('Terraform Init & Plan') {
        steps {
          sh 'cd ..'    
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
      
      stage('Terraform Destroy') {
        steps {
            script {
                def userInput = input(id: 'confirm', message: 'Destroy Terraform?', parameters: [ [$class: 'BooleanParameterDefinition', defaultValue: true, description: 'Destory terraform', name: 'confirm destroy'] ])
                    if (userInput == true) {
                        sh '/usr/local/bin/terraform destroy -auto-approve'
                    }
                    else {
                        sh "echo 'Terraform destroy denied'"
                    }
                }
            }
        }
      
    } 
  }

