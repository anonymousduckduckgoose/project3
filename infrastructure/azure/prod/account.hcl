# Set account-wide variables. These are automatically pulled in to configure the remote state bucket in the root
# terragrunt.hcl configuration.
locals {
  account_name = "prod"
  azure_id     = "000000000-0000-0000-0000-000000000000"
  env          = "prod"
}
