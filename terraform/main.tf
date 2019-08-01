# Configure AWS
provider "aws" {
  region = "us-east-1"
}

module "iam_user" {
  source = "github.com/cisagov/molecule-packer-travisci-iam-user-tf-module"

  ssm_parameters = ["/guacamole/postgres_username", "/guacamole/postgres_password"]
  user_name      = "test-ansible-role-guacamole"
  tags = {
    Team        = "NCATS OIS - Development"
    Application = "ansible-role-guacamole testing"
  }
}
