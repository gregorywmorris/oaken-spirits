# Configure the AWS Provider
provider "aws" {
  region                   = "us-east-1"
  profile                  = "eb-cli" # The profile within AWS CLI config file
}

