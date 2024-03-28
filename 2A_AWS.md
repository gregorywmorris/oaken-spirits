# AWS

**Note:** Assumes aws-cli and terraform are set up on the host system. To run on AWS console import `manin.tf`, `variable.tf` only.

1. cd `oaken-spirits/src/production/aws`
1. Edit `provider.tf`**profile** with the profile in `.aws/config` file
1. Terraform (each run will create a new public/private/key pair)
    - `terraform init`
    - `terraform plan`
    - `terraform apply`
1. Export private key
    - `terraform output private_key_pem > oaken-pair.pem`
    - `chmod 600 ~/.ssh/oaken-pair.pem`
