# 📘 Flask Task Manager with MySQL in Private EC2 | AWS Deployment

This is a secure AWS-based project where a **Flask Task Manager app** (hosted in a public EC2) connects to a **MySQL database** in a **private EC2**. A bastion host enables private EC2 access. The app performs full **CRUD operations** and is deployed using **Gunicorn + Systemd**, with code pushed to GitHub via SSH.

---

## 📑 Table of Contents
- 📦 Application Code
- 📝 Project Details
- ⚙️ Setup Guide
- 🔒 Git SSH & Auto Deployment
- 📊 Monitoring with CloudWatch
- 👨‍💻 Developed By
---

## 📦 Application Code

The `Flask Task Manager` allows users to:
- Add Tasks
- Edit Tasks
- Mark Tasks Completed
- Delete Tasks

The app uses:
- `Flask`
- `SQLAlchemy`
- `MySQL`
- `Gunicorn` + `Systemd` (for deployment)

---

## 📝 Project Details

- ✅ **MySQL is installed on a private EC2 instance**
- ✅ **Flask app is hosted on a public EC2 instance**
- ✅ **Security is enforced via Bastion (jump box)**
- ✅ **MySQL accessed via internal IP only**
- ✅ **Tasks are stored in `flaskappdb` using `Task` model**
- ✅ **Gunicorn handles production deployment**
- ✅ **Source code is tracked with GitHub using SSH**
- ✅ **CloudWatch used for application and system monitoring**
- ✅ **Application is connected to GitHub via SSH and updates are deployed automatically using deploy.sh script**

---

## ⚙️ Setup Guide

### 1. VPC & Subnets
- VPC: `vpc-taskmanager`
- Public Subnet: `10.0.1.0/24`
- Private Subnet: `10.0.2.0/24`

### 2. IGW and NAT
- IGW attached to VPC
- NAT Gateway for private subnet internet access

### 3. EC2 Instances
- **Public EC2 (Flask + Bastion)**: Port 22, 8000 open
- **Private EC2 (MySQL)**: Port 3306 open to Flask SG

### 4. SSH Access
```bash
ssh -i my-key.pem ec2-user@<bastion-public-ip>
ssh -i my-key.pem ec2-user@<mysql-private-ip>  # From bastion
```

### 5. MySQL Setup In private Instances
```bash
sudo yum install -y mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

### 6. Create user and DB:

CREATE DATABASE flaskappdb;
CREATE USER 'flaskuser'@'%' IDENTIFIED BY 'Passworddb';
GRANT ALL PRIVILEGES ON flaskappdb.* TO 'flaskuser'@'%';
FLUSH PRIVILEGES;

### 7. Flask App Config
python

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:Passworddb@<private-ip>:3306/flaskappdb'

### 8. Deploy with Gunicorn
bash
```
pip install gunicorn
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

### 9. Deployment Script (Auto Pull + Restart)
Create deploy.sh:
bash
```
#!/bin/bash

LOG_FILE="/home/ec2-user/flask-app/logs/deploy.log"
{
    echo "------ DEPLOYMENT STARTED AT $(date) ------"
    cd /home/ec2-user/flask-app || { echo "ERROR: Cannot access project directory"; exit 1; }
    echo "Pulling the latest code from GitHub..."
    git pull origin main
    echo "Restarting Gunicorn..."
    sudo systemctl restart gunicorn
    echo "Gunicorn status:"
    sudo systemctl status gunicorn --no-pager
    echo "Deployment completed successfully!"
    echo "------ DEPLOYMENT FINISHED AT $(date) ------"
    echo ""
} >> "$LOG_FILE" 2>&1

```
Make executable:
bash
```
Chmod +x deploy.sh
```
### 10. 🔒 Git SSH Setup

When you clone or pull using HTTPS, GitHub asks for username + token.
With SSH, authentication is done using keys, avoiding manual input.

**1. Generate SSH Key**
```ssh-keygen -t rsa -b 4096 -C "your_email@example.com" ```

**2. Add to GitHub**
Copy the contents of ~/.ssh/id_rsa.pub
Go to GitHub → Settings → SSH and GPG Keys → New SSH key

**3. Change Remote to SSH**
git remote set-url origin git@github.com:username/repo.git

### 11. 📊 CloudWatch Setup

**✅ 1. Install CloudWatch Agent**
bash
```sudo yum install -y amazon-cloudwatch-agent
sudo mkdir -p /opt/aws/amazon-cloudwatch-agent/etc
 ```

**✅ 2. Create Configuration File**

 bash
```sudo nano /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json ```

Paste:
bash
```
{
  "agent": {
    "metrics_collection_interval": 60,
    "run_as_user": "root"
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/home/ec2-user/flask-app/app.log",
            "log_group_name": "flask-app-logs",
            "log_stream_name": "{instance_id}-app",
            "timestamp_format": "%Y-%m-%d %H:%M:%S"
          }
        ]
      }
    }
  },
  "metrics": {
    "append_dimensions": {
      "InstanceId": "${aws:InstanceId}"
    },
    "metrics_collected": {
      "cpu": {
        "measurement": ["cpu_usage_idle", "cpu_usage_user", "cpu_usage_system"],
        "metrics_collection_interval": 60
      },
      "mem": {
        "measurement": ["mem_used_percent"],
        "metrics_collection_interval": 60
      },
      "disk": {
        "measurement": ["used_percent"],
        "metrics_collection_interval": 60,
        "resources": ["/"]
      }
    }
  }
}
```
**✅ 3. Start Agent**
bash
```
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json \
  -s
  ```

### 12. Flask Logging Integration
 Integrated robust logging in app.py:Logs saved to app.log
 - Critical events/errors are visible for troubleshooting
bash
```
import logging
logging.basicConfig(filename='app.log', level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
 ```


### 13.👨‍💻 Developed By
- Khushboo
- 📧 Khushboobhardwaj1999@gmail.com
- 🔗 GitHub: [khus22](https://github.com/khus22/)
