variable "resource_group_name" {
  description = "Name of the Azure resource group"
}

variable "location" {
  description = "Azure region"
}

variable "vm_name" {
  description = "Name of the virtual machine"
}

variable "vm_size" {
  description = "Size of the virtual machine"
}

variable "admin_username" {
  description = "Username for SSH access"
  default     = "azureuser"
}

variable "tags" {
  description = "Tags for the virtual machine"
  type        = map(string)
  default     = {}
}

variable "security_rules" {
  description = "List of security rules for the network security group."
  type = list(object({
    name               = string
    priority           = number
    direction          = string
    access             = string
    protocol           = string
    source_port_range  = string
    source_addy_prefix = string
    destination_port   = string
    dest_addy_prefix   = string
  }))
  default = []
}

variable "source_image_reference" {
  description = "The reference to the source image for the virtual machine."
  type = object({
    publisher = string
    offer     = string
    sku       = string
    version   = string
  })
}

variable "replicas" {
  description = "Number of VM replicas to create"
  type        = number
  default     = 1
}
