variable "postgres_user" {
  description = "The username for PostgreSQL"
  type        = string
  default     = "postgres"
}

variable "postgres_db" {
  description = "The name of the database for PostgreSQL"
  type        = string
  default     = "appx_db"
}

variable "postgres_password" {
  description = "The password for PostgreSQL"
  type        = string
}

variable "postgres_url" {
  description = "The URL for PostgreSQL"
  type        = string
}

variable "rabbitmq_uri" {
  description = "The URi for RabbitMQ"
  type        = string
}
