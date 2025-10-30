terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>4.4"
    }
  }
  required_version = "~> 1.12"
}

provider "azurerm" {
  features {}
  subscription_id = "4d1a4da3-07d0-4889-a1dd-a60d6a8a8e2d"
}


resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  
  tags = var.tags
}


resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
  
  tags = var.tags
}


resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  tags = var.tags
}


resource "azurerm_storage_share" "duckdb_share" {
  name                 = "duckdb-data"
  storage_account_id   = azurerm_storage_account.storage.id 
  quota                = 5
}



resource "azurerm_container_group" "dwh_pipeline" {
  name                = "dwh-pipeline-ci"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  restart_policy      = "Always"
  
  image_registry_credential {
    server   = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
  }
  
  container {
    name   = "dwh-pipeline"
    image  = "${azurerm_container_registry.acr.login_server}/hr-pipeline:latest"
    cpu    = "2"
    memory = "3"
    
    ports {
      port     = 3000
      protocol = "TCP"
    }
    
    environment_variables = {
      DBT_PROFILES_DIR = "/root/.dbt"
      DUCKDB_PATH      = "/mnt/data/job_ads.duckdb"
    }
    
    volume {
      name                 = "duckdb-volume"
      mount_path           = "/mnt/data"
      storage_account_name = azurerm_storage_account.storage.name
      storage_account_key  = azurerm_storage_account.storage.primary_access_key
      share_name           = azurerm_storage_share.duckdb_share.name
    }
  }
  
  ip_address_type = "Public"
  dns_name_label  = "dwh-pipeline-${var.environment}"
  
  tags = var.tags
  
  depends_on = [
    azurerm_storage_share.duckdb_share
  ]
}


resource "azurerm_container_group" "dashboard" {
  name                = "dashboard-ci"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  restart_policy      = "Always"
  
  image_registry_credential {
    server   = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
  }
  
  container {
    name   = "dashboard"
    image  = "${azurerm_container_registry.acr.login_server}/dashboard:latest"
    cpu    = "0.5"
    memory = "1"
    
    ports {
      port     = 8501
      protocol = "TCP"
    }
    
    environment_variables = {
      DUCKDB_PATH = "/mnt/data/job_ads.duckdb"
    }
    
    volume {
      name                 = "duckdb-volume"
      mount_path           = "/mnt/data"
      storage_account_name = azurerm_storage_account.storage.name
      storage_account_key  = azurerm_storage_account.storage.primary_access_key
      share_name           = azurerm_storage_share.duckdb_share.name
      read_only            = true
    }
  }
  
  ip_address_type = "Public"
  dns_name_label  = "dashboard-${var.environment}"
  
  tags = var.tags
  
  depends_on = [
    azurerm_storage_share.duckdb_share,
    azurerm_container_group.dwh_pipeline
  ]
}
