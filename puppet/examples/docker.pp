# This class deploys a docker-ce host on Ubuntu 16.04 from scratch

class docker {
  
  $docker_repo = "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable\n"
  $docker_repo_file = "/etc/apt/sources.list.d/docker.list"

  # Add Docker's official GPG key only if the Docker repository is not present
  exec { 'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -':
    path   => '/usr/bin:/bin',
    unless => "test -f $docker_repo_file",
  }


  # Add the Docker repository
  file { $docker_repo_file:
    ensure  => 'present',
    replace => 'no',
    content => $docker_repo,
    mode    => '0644',
  }

  # Make sure your source list is up-to-date
  exec { 'apt-get-update':
    command     => '/usr/bin/apt-get update',
    refreshonly => true,
  }

  # Install package
  package { 'docker-ce':
    name    => 'docker-ce',
    ensure  => latest,
    require => Exec['apt-get-update'],
  }

  # Ensure service running and enabled
  service { 'docker-service':
    name    => docker,
    ensure  => running,
    enable  => true,
  }

}
