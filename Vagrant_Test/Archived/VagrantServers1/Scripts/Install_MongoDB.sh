#!/bin/bash

echo "Install MongoDB."

# Add Repo.
cat > /etc/yum.repos.d/mongodb-org-3.4.repo << EOF
[mongodb-org-3.4]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/7/mongodb-org/3.4/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.4.asc
EOF

# Install.
yum install -y mongodb-org

# Enable remote access.
sed -i "s/\(^.*bindIp.*$\)/#\1/g" /etc/mongod.conf

# Enable and start service.
systemctl enable mongod
systemctl start mongod
sleep 5

# Create users for admin DB and test DB.
mongo << EOF
use admin
db.createUser(
  {
    user: "root",
    pwd: "P@ssw0rd",
    roles: [{role: "root", db: "admin"}]
  }
)
db.createUser(
  {
    user: "admin",
    pwd: "P@ssw0rd",
    roles: [{role: "userAdminAnyDatabase", db: "admin"}]
  }
)

use test
db.createUser(
  {
    user: "tester",
    pwd: "P@ssw0rd",
    roles: [{role: "dbOwner", db: "test"}]
 }
)
EOF
