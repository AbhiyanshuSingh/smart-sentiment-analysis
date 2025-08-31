terraform {
  required_providers {
    azurerm = {
        source = "hashicorp/azurerm"
        version = "~>3.0"
    }
  }

}

provider "azurerm" {
  features {
    
  }
}

resource "azurerm_resource_group" "rg" {
  name = "sentiment-rg"
  location = "Central India"
}

resource "azurerm_container_registry" "acr" {
  name = "sentimentacr${random_id.id.hex}"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  sku = "Basic"
  admin_enabled = true
}

resource "random_id" "id" {
  byte_length = 8
}

resource "azurerm_container_group" "acg" {
  name = "sentiment-acg"
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  depends_on = [ azurerm_container_registry.acr ]

  ip_address_type = "Public"
  dns_name_label = "api-sentiment-${random_id.id.hex}"
  os_type = "Linux"


  image_registry_credential {
    server = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
  }

  container {
    name = "sentiment-container-api"
    image = "${azurerm_container_registry.acr.login_server}/sentiment-api:v1"
    memory = "1.5"
    cpu = "1"

    ports {
        port = 80
        protocol = "TCP"
    }
  }
}


output "app_url" {
  value = "http://${azurerm_container_group.acg.fqdn}"
}