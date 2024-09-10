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
    "POSTGRES_USER=myuser",
    "POSTGRES_PASSWORD=mypassword",
    "POSTGRES_DB=mydatabase"
  ]

  networks_advanced {
    name = docker_network.my_network.name
  }
}

resource "docker_image" "api" {
  name = "flask-api"
  build {
    context = "${path.root}/src"
    tag     = ["flask-api:latest"]
    label = {
      author : "omaciasd"
    }
  }
  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset(path.module, "src/*") : filesha1(f)]))
  }
}

resource "docker_container" "api" {
  name  = "flask-api"
  image = docker_image.api.name

  ports {
    internal = 50010
    external = 50010
  }

  networks_advanced {
    name = docker_network.my_network.name
  }

  depends_on = [docker_container.postgres]
}
