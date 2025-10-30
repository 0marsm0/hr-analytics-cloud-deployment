
output "resource_group_name" {
  value       = azurerm_resource_group.rg.name
}

output "acr_login_server" {
  value       = azurerm_container_registry.acr.login_server
}

output "acr_admin_username" {
  value       = azurerm_container_registry.acr.admin_username
  sensitive   = true
}

output "acr_admin_password" {
  value       = azurerm_container_registry.acr.admin_password
  sensitive   = true
}

output "dwh_pipeline_fqdn" {
  value       = "http://${azurerm_container_group.dwh_pipeline.fqdn}:3000"
}

output "dashboard_fqdn" {
  value       = "http://${azurerm_container_group.dashboard.fqdn}:8501"
}

output "storage_account_name" {
  value       = azurerm_storage_account.storage.name
}

output "storage_primary_key" {
  value       = azurerm_storage_account.storage.primary_access_key
  sensitive   = true
}
