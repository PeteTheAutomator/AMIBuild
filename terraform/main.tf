module "codebuild" {
    source = "github.com/PeteTheAutomator/terraform-aws-codebuild"
    codebuild_project_name = "AMIBuild-Testing"
    codebuild_project_description = "POC for AMI Build Pipeline"
    codebuild_source_type = "GITHUB"
    codebuild_source_location = "https://github.com/PeteTheAutomator/AMIBuild.git"
    codebuild_image = "docker.io/petetheautomator/ansible"
}

resource "aws_iam_policy_attachment" "codebuild_policy_attachment2" {
  name       = "codebuild-policy-attachment2"
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
  roles      = ["${module.codebuild.codebuild_role_id}"]
}

resource "aws_iam_policy" "codebuild_ssm_policy" {
  name        = "codebuild-ssm-policy"
  path        = "/service-role/"
  description = "Policy for Systems Manager Parameter Store"

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:DescribeParameters"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssm:GetParameters"
            ],
            "Resource": "arn:aws:ssm:eu-west-2:*:parameter/AMIBuild-Key"
        }
    ]
}
POLICY
}

resource "aws_iam_policy_attachment" "codebuild_policy_attachment3" {
  name       = "codebuild-policy-attachment3"
  policy_arn = "${aws_iam_policy.codebuild_ssm_policy.arn}"
  roles      = ["${module.codebuild.codebuild_role_id}"]
}
