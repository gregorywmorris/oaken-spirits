# AWS

**Note:** Assumes aws-cli and terraform are set up on the host system.

1. Open your CLI
1. `cd oaken-spirits/src/production/aws` <- continue to work from this directory.
1. Edit `provider.tf`**profile** with the profile in your `.aws/config` file.
1. Terraform (each run will create a new public/private key pair).
    - `terraform init`
    - `terraform plan`
    - `terraform apply`
1. Export private key
    - `terraform output private_key_pem > oaken-pair.pem` <- note where this key is stored (oaken-spirits/src/production/aws).
    - `chmod 600 ~/.ssh/oaken-pair.pem`
1. SSH into each EC2, except MySQL instance.
    - In a new command window, `cd oaken-spirits/src/production/aws`
    - select EC2 instance.
    - Connect (upper right).
    - SSH, copy and run command.
1. Import application files
    - `mkdir app`
    - `cd app`
    - Import

        [!NOTE]
        These are from my repository, you could also get them from the forked repository.
        - Application application, `wget` based on the VM instance you are logged into.
            - ${\color{red}mysql-api.py}$: `wget https://raw.githubusercontent.com/gregorywmorris/oaken-spirits/main/src/production/aws/aws-app/mysql-api/mysql-api.py`
            - **shipping.py**: `wget https://raw.githubusercontent.com/gregorywmorris/oaken-spirits/main/src/production/aws/aws-app/shipping/shipping.py`
            - **accounting.py**: `wget https://raw.githubusercontent.com/gregorywmorris/oaken-spirits/main/src/production/aws/aws-app/accounting/accounting.py`
        - Service file, `wget` based on the VM instance you are logged into.
            - **oaken-mysql-api.service**: `wget https://raw.githubusercontent.com/gregorywmorris/oaken-spirits/main/src/production/aws/aws-app/mysql-api/oaken-mysql-api.service`
            - **oaken-shipping.service**: `wget https://raw.githubusercontent.com/gregorywmorris/oaken-spirits/main/src/production/aws/aws-app/shipping/oaken-shippping.service`
            - **oaken-accounting.service**: `wget https://raw.githubusercontent.com/gregorywmorris/oaken-spirits/main/src/production/aws/aws-app/accounting/oaken-accounting.service`
    - set up service
        - Replace `<insert-your-service-file.service>` with service file name for given instance.
        - Copy: `sudo cp <insert-your-service-file.service> /etc/systemd/system/`
        - Enable: `sudo systemctl enable <insert-your-service-file.service>`
        - Start: `sudo systemctl start <insert-your-service-file.service>`
        - Verify: `sudo systemctl status <insert-your-service-file.service>`

