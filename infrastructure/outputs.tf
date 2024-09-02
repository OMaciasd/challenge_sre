output "api_url" {
  value = "http://${docker_container.api.network_data.0.ip_address}:50010"
}
