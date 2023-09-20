# ---------------------------------------------------------------------------------------------------------------------
# TERRAGRUNT CONFIGURATION
# Terragrunt is a thin wrapper for Terraform that provides extra tools for working with multiple Terraform modules,
# remote state, and locking: https://github.com/gruntwork-io/terragrunt
# ---------------------------------------------------------------------------------------------------------------------

locals {
  # Automatically load account-level variables
  azure_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))

  # Automatically load region-level variables
  region_vars = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  # Extract the variables we need for easy access
  account_name = local.azure_vars.locals.account_name
  azure_id     = local.azure_vars.locals.azure_id
  az_region    = local.region_vars.locals.az_region
  environment  = local.azure_vars.locals.env

  # pick a region for the state bucket for global resources
  region = local.az_region == "global" ? "westeurope" : local.az_region
}

# Generate an Azure provider block
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
    }
  }
}
EOF
}

# Configure Terragrunt to automatically store tfstate files in an Azure storage bucket
remote_state {
  backend = "azurerm"
  config = {
    resource_group_name  = "${local.account_name}"
    storage_account_name = "ddgterraform"
    container_name       = "ddg-terraform-state-${local.account_name}-${local.az_region}"
    key                  = "${path_relative_to_include()}/terraform.tfstate"
    subscription_id      = "${local.azure_id}"
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# GLOBAL PARAMETERS
# These variables apply to all configurations in this subfolder. These are automatically merged into the child
# `terragrunt.hcl` config via the include block.
# ---------------------------------------------------------------------------------------------------------------------

# Configure root level variables that all resources can inherit. This is especially helpful with multi-account configs
# where terraform_remote_state data sources are placed directly into the modules.
inputs = merge(
  local.azure_vars.locals,
  {
    region      = local.region
    az_region   = local.region
    environment = local.environment
  }
)
