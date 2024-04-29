terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.13.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_network" "app_network" {
  name = "app_network"
}

resource "docker_image" "alpca_consumer" {
  name         = "alpca-consumer:latest"
  keep_locally = true
}

resource "docker_image" "redis" {
  name         = "redis:latest"
  keep_locally = false
}

resource "docker_image" "dashboard_react" {
  name         = "dashboard:latest"
  keep_locally = true
}

resource "docker_container" "web" {
  image = docker_image.alpca_consumer.latest
  name  = "web"
  command = ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
  networks_advanced {
    name = docker_network.app_network.name
  }
  volumes {
    host_path      = "/Users/omerSuliman/dev/py/TradeIntelli-AI/alpca-consumer"
    container_path = "/app"
  }
  working_dir = "/app"
  ports {
    internal = 8000
    external = 8000
  }
  env = ["PYTHONUNBUFFERED=1"]
}

resource "docker_container" "celery" {
  image = docker_image.alpca_consumer.latest
  name  = "celery"
  command = ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
  networks_advanced {
    name = docker_network.app_network.name
  }
  volumes {
    host_path      = "/Users/omerSuliman/dev/py/TradeIntelli-AI/alpca-consumer"
    container_path = "/app"
  }
  working_dir = "/app"
  env = ["PYTHONUNBUFFERED=1"]
  depends_on = [docker_container.web, docker_container.redis]
}

resource "docker_container" "celerybeat" {
  image = docker_image.alpca_consumer.latest
  name  = "celerybeat"
  command = ["celery", "-A", "celery_app", "beat", "--loglevel=info", "--scheduler", "celery.beat.PersistentScheduler"]
  networks_advanced {
    name = docker_network.app_network.name
  }
  volumes {
    host_path      = "/Users/omerSuliman/dev/py/TradeIntelli-AI/alpca-consumer"
    container_path = "/app"
  }
  working_dir = "/app"
  env = ["PYTHONUNBUFFERED=1"]
  depends_on = [docker_container.web, docker_container.redis]
}

resource "docker_container" "redis" {
  image = docker_image.redis.latest
  networks_advanced {
    name = docker_network.app_network.name
  }
  name  = "redis"
  ports {
    internal = 6379
    external = 6379
  }
}


resource "docker_container" "npm" {
  image = docker_image.dashboard_react.latest
  networks_advanced {
    name = docker_network.app_network.name
  }
  name  = "npm"
  ports {
    internal = 3000
    external = 80
  }
  volumes {
    host_path      = "/Users/omerSuliman/dev/py/TradeIntelli-AI/dashboard-react"
    container_path = "/app"
  }
  working_dir = "/app"
  depends_on = [docker_container.web]
}
