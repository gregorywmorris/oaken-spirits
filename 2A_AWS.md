# AWS

**Note:** Assumes aws-cli and terraform are set up on the host system. To run on AWS console import `manin.tf`, `variable.tf` only.

1. cd `oaken-spirits/src/production/aws` <- continue to work from this directory.
1. Edit `provider.tf`**profile** with the profile in `.aws/config` file
1. Terraform (each run will create a new public/private/key pair).
    - `terraform init`
    - `terraform plan`
    - `terraform apply`
1. Export private key
    - `terraform output private_key_pem > oaken-pair.pem`
    - `chmod 600 ~/.ssh/oaken-pair.pem`
1. SSH into each EC2, except MySQL instance.
    - select EC2 instance.
    - Connect (upper right).
    - SSH, copy and run command.
1. Import application files
    - `mkdir app`
    - `cd app`
    - Import
        - Application, `wget` based on the server you are logged into.
            - Mysql-api: `wget`
            - Shipping: `wget`
            - Accounting: `wget`
        - Service, `wget` based on the server you are logged into.
            - Mysql-api: `wget`
            - Shipping: `wget`
            - Accounting: `wget`
    - set up service
        - Copy: `sudo cp <insert-your-service-file.service> /etc/systemd/system/`
        - Enable: `sudo systemctl enable your-service-file.service`
        - Start: `sudo systemctl start your-service-file.service`
        - Verify: `sudo systemctl status your-service-file.service`

