<!DOCTYPE html>
<html>
<head>
    <title>Markdown Document with Background Color</title>
    <style>
        body {
            background-color: black; /* Specify your desired background color */
            color: offwhite;
        }
        .container { /* class="container" */
            margin: 0 auto;
            max-width: 800px;
            padding: 20px;
            background-color: black; /* Specify the background color of the content area */
        }
    </style>
</head>
<body>

# Set environment variables

## For AWS

1. Install and Configure SSM Agent (If Not Already Installed):

    - For Amazon Linux, Amazon Linux 2, or Ubuntu Server, the SSM Agent is already installed by default. You may need to check if it's running and properly configured.
1. Grant IAM Permissions:
    - Ensure that the EC2 instance has the necessary IAM permissions to access the Systems Manager Parameter Store. You can attach an IAM role to the EC2 instance with the required permissions.
1. Retrieve and Activate Environment Variables:
    - Use the AWS Command Line Interface (CLI) or SDK to retrieve the environment variables from Parameter Store and set them as system environment variables on the EC2 instance.
    - Here's an example of how you can retrieve and activate environment variables using the AWS CLI on a Linux-based EC2 instance:

```Bash
# Retrieve the environment variables from Parameter Store

aws ssm get-parameters --names "/path/to/parameter" --region your-region --with-decryption --query 'Parameters[*].{Value:Value}' --output text | while read -r line; do export "$line"; done

# Activate the environment variables

source ~/.bashrc  # or source ~/.bash_profile
```

Testing:

- After activating the environment variables, you can verify that they are set correctly by echoing their values or running your application that depends on them.

## For local Docker

Create docker.env (add to gitignore first) in folder with Dockerfiles. Add the list below with your information or use the default and just add your S3 log.

```Text
ENV KAFKA_SERVER=kafka
ENV SHIPPING_TOPIC=shipping
ENV SHIPPING_TOPIC=invoices

ENV MYSQL_HOST=mysql
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=mysql
ENV MYSQL_DATABASE=oaken

ENV SHIPPING_LOG_BUCKET=
ENV ACCOUNTING_LOG_BUCKET=
```
