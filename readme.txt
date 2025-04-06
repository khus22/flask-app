📘 Deploying MySQL in a Private EC2 Instance from Scratch (AWS)

This document is a step-by-step guide to help you set up MySQL in a private EC2 instance using a bastion host (public EC2). This is perfect if you want to recreate the setup from scratch in the future.

🛠️ Architecture Overview

Public Subnet:

Bastion Host (Jump Box) with public IP

NAT Gateway

Private Subnet:

MySQL EC2 instance

1. 🧱 Create VPC and Subnets

Create a new VPC (e.g., vpc-devops-project)

Create two subnets:

public-subnet-a (e.g., 10.0.1.0/24)

private-subnet-a (e.g., 10.0.2.0/24)

2. 📡 Internet Gateway and Route Tables

Internet Gateway:

Attach an Internet Gateway to your VPC.

Modify the route table for the public subnet to route 0.0.0.0/0 via the IGW.

NAT Gateway:

Create an Elastic IP.

Launch a NAT Gateway in the public subnet using that Elastic IP.

Modify the route table of the private subnet:

Route 0.0.0.0/0 through the NAT Gateway.

3. 🚀 Launch EC2 Instances

Public EC2 (Bastion Host):

AMI: Amazon Linux 2

Subnet: Public

Auto-assign Public IP: Enabled

Security Group:

Allow SSH (Port 22) from your IP

Private EC2 (MySQL DB):

AMI: Amazon Linux 2

Subnet: Private

Auto-assign Public IP: Disabled

Security Group:

Allow SSH from Bastion Host's security group

Allow MySQL (Port 3306) from relevant source (e.g., app server in future)

4. 🔐 SSH Access via Bastion Host

From Local Machine to Bastion:

ssh -i "my-ssh-key-devop.pem" ec2-user@13.48.58.242

From Bastion to Private EC2:

ssh -i "my-ssh-key-devop.pem" ec2-user@172.31.1.156

Replace with your actual private EC2 internal IP address.

5. 🐬 Install MySQL in Private EC2 (Amazon Linux)

Amazon Linux 2 does not have MySQL by default. Use the MySQL community repo to install:

Step-by-Step Installation:

# Step 1: Download MySQL repo package
wget https://dev.mysql.com/get/mysql80-community-release-el7-5.noarch.rpm

# Step 2: Install the repo
sudo rpm -ivh mysql80-community-release-el7-5.noarch.rpm

# Step 3: Verify MySQL repo is enabled
yum repolist enabled | grep mysql

# Step 4: Install MySQL Server
sudo yum install -y mysql-server

# Step 5: Start MySQL service
sudo systemctl start mysqld

# Step 6: Enable MySQL to start on boot
sudo systemctl enable mysqld

Check MySQL Status:

sudo systemctl status mysqld

6. 🔐 Create Database and User for Flask App

Generic Steps:

Login to MySQL:

mysql -u root -p

Then run:

CREATE DATABASE dbname;
CREATE USER 'dbuser'@'%' IDENTIFIED BY 'Password';
GRANT ALL PRIVILEGES ON flaskappdb.* TO 'flaskuser'@'%';
FLUSH PRIVILEGES;

7. 🧹 Integrate with Flask App (Hosted in Public EC2)

The app.py was already created in the public EC2 instance.

After database and user creation, tables were initialized from the public EC2 instance, not directly from private EC2.

This was done by connecting to the private MySQL database using the flaskuser credentials from the public EC2 where the Flask app is hosted.

Make sure the Flask app's app.py is updated with proper MySQL connection string:

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbuser:Passworddb@<PRIVATE_EC2_PRIVATE_IP>:3306/flaskappdb'

Create the Tables from Flask App:

To create the table in your database, you can use Flask-SQLAlchemy's create_all() method, which will create all tables defined by your models (in this case, the Task model).


Open the Flask shell Set the FLASK_APP environment variable:

If your application is in app.py, run the following command in your terminal:


export FLASK_APP=app.py
Activate the Flask shell: Now that the FLASK_APP variable is set, you can run:

flask shell

Import your db and Task model.

Call the create_all() method to create the table in the database.

Here are the steps:

from app import db
db.create_all()
This will create the necessary table (task) in your database based on the Task model.

Verify the Table:
After running the above command, you can verify if the table has been created by checking your database directly using MySQL commands, or by querying for tasks from the Flask shell:


tasks = Task.query.all()
print(tasks)





