AMIBuild
========

POC pipeline for AMI building/baking


Description
-----------

TODO: full description & drawing


CodeBuild
---------

A CodeBuild project is created using Terraform, which can be provisioned using the following commands...

```
cd terraform
terraform init
terraform apply
```

Docker
------

A Docker image with Ansible is required for provisioning the EC2 instance to bake, carrying out any software installation and OS configuration on it, and then to stop & snapshot the AMI.  The docker image can be build using these commands...

```
cd docker
docker build -t petetheautomator/ansible
docker push petetheautomator/ansible
```


Building an AMI
---------------

Locate the "AMIBuild-Testing" CodeBuild project in the AWS Console and build from there.

TODO: awscli examples
