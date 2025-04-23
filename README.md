# 📘 Flask Task Manager with MySQL in Private EC2 | AWS Deployment

This is a secure AWS-based project where a **Flask Task Manager app** (hosted in a public EC2) connects to a **MySQL database** in a **private EC2**. A bastion host enables private EC2 access. The app performs full **CRUD operations** and is deployed using **Gunicorn + Systemd**, with code pushed to GitHub via SSH.

---

## 📑 Table of Contents

- [📦 Application Code](#application-code)
- [📝 Project Details](#project-details)
- [⚙️ Setup Guide](#️setup-guide)

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
   

### 5. Mysql setup 

sudo yum install -y mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld


### 6.Create user and DB:

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

###👨‍💻 Developed By
    Khushboo
📧 Khushboobhardwaj1999@gmail.com
🔗 GitHub: khus22
