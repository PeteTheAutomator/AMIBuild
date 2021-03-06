module "codebuild" {
    source = "github.com/PeteTheAutomator/terraform-aws-codebuild"
    codebuild_project_name = "AMIBuild-Testing"
    codebuild_project_description = "POC for AMI Build Pipeline"
    codebuild_source_type = "GITHUB"
    codebuild_source_location = "https://github.com/PeteTheAutomator/AMIBuild.git"
    codebuild_image = "docker.io/petetheautomator/ansible"
    codebuild_vpc_id = "vpc-d1a64fb8"
    codebuild_subnets = ["subnet-5a2a3a21"]
    codebuild_security_group_ids = ["sg-902c74f8"]
    codebuild_public_subnet_id = "subnet-7316010b"
    codebuild_private_route_table_id = "rtb-0709dd6f"
}
