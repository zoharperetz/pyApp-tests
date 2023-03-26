provider "aws" {
  region = "us-east-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "my-vpc"
  cidr   = "10.0.0.0/16"
  azs    = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  enable_nat_gateway = true
  
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "17.0.0"

  cluster_name = "staging-cluster"
  subnets      = module.vpc.private_subnets
  vpc_id       = module.vpc.vpc_id
  tags = {
    Terraform   = "true"
    Environment = "dev"
  }

  worker_groups_launch_template = [{
    name                 = "my-node-group"
    instance_type        = "t2.micro"
    asg_desired_capacity = 1
    additional_security_group_ids = [module.vpc.default_security_group_id]
  }]
  
  cluster_version = "1.21"
  
}

