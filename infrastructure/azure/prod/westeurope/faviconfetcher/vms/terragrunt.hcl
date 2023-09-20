include "root" {
  path = find_in_parent_folders()
}

# Include the Terraform configuration for the Azure VM module
terraform {
  source = "../.modules/azure/azure-vm"
}

inputs = {
  resource_group_name = "prod-api"
  location            = "westeurope"
  vm_name             = "faviconfetcher"
  vm_size             = "Standard_B1s"
  region              = "West Europe"
  replicas            = 2 # Use this input to horizontally scale the deployment
  source_image_reference = {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts-gen2"
    version   = "latest"
  }
  security_rules = [
    {
      name               = "allow_api"
      priority           = 100
      direction          = "Inbound"
      access             = "Allow"
      protocol           = "Tcp"
      source_port_range  = "*"
      destination_port   = "8000"
      source_addy_prefix = "*"
      dest_addy_prefix   = "*"
    },
    {
      name               = "allow_ssh"
      priority           = 101
      direction          = "Inbound"
      access             = "Allow"
      protocol           = "Tcp"
      source_port_range  = "*"
      destination_port   = "22"
      source_addy_prefix = "*" # you may consider limiting this an IP
      dest_addy_prefix   = "*"
    },
    {
      name               = "allow_http"
      priority           = 102
      direction          = "Inbound"
      access             = "Allow"
      protocol           = "Tcp"
      source_port_range  = "*"
      destination_port   = "80"
      source_addy_prefix = "*"
      dest_addy_prefix   = "*"
    },
    {
      name               = "allowhttps"
      priority           = 106
      direction          = "Inbound"
      access             = "Allow"
      protocol           = "Tcp"
      source_port_range  = "*"
      destination_port   = "443"
      source_addy_prefix = "*"
      dest_addy_prefix   = "*"
    }
  ]
  tags = {
    "env" = "prod"
  }
}

