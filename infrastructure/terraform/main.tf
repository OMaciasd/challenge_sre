resource "docker_network" "my_network" {
  name = "my_network"
}

resource "docker_image" "postgres" {
  name = "postgres:latest"
}

resource "docker_container" "postgres" {
  name  = "postgres"
  image = docker_image.postgres.name

  ports {
    internal = 5432
    external = 5432
  }

  env = [
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}"
  ]

  networks_advanced {
    name = docker_network.my_network.name
  }
}

resource "docker_image" "api" {
  name = "omaciasd/flask-api:latest"
}

resource "docker_container" "api" {
  name  = "flask-api"
  image = docker_image.api.name

  ports {
    internal = 50010
    external = 50010
  }

  env = [
    "DATABASE_URL=${var.postgres_url}",
    "RABBITMQ_URL=${var.rabbitmq_uri}"
  ]

  restart = "always"
  networks_advanced {
    name = docker_network.my_network.name
  }

  depends_on = [docker_container.postgres]
}
