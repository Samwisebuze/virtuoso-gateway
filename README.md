# virtuoso-api-gateway

A simple API Gateway for Virtuoso services.

## Usage

Clone, then build the image:

```sh
$ docker build -t virtuoso-api-gateway .
```

Create a Docker network for the API Gateway:

```sh
$ docker network create kong-net
```

Run:

```sh
docker run -d --rm --name kong \
     --network=kong-net \
     -p 8000:8000 \
     -p 8001:8001 \
     virtuoso-api-gateway
```

Ports:

- 8000: Proxying http traffic
<!-- - 8443: proxying https traffic -->
- 8001: Admin API
<!-- - 8444: Admin API HTTPS -->

Get list of available services:

```sh
$ curl -i http://localhost:8001/services
```

Get API Gateway Status:

```sh
$ curl -i http://localhost:8001/status
```

Docs: [https://docs.konghq.com/install/docker/](https://docs.konghq.com/install/docker/)

Sidenote: SSL support: `-e "KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl"` and `-p 8443:8443` arguement.

## Service Configurations

Use `kong.yml` to create and manage service configurations.

Example `kong.yml` service configuration and example usage:

```yml
- name: network-service
  url: http://network-service-host.com
  routes:
  - name: network
    paths:
    - /
```

Note: This service's container must be registered on the `kong-net` network.

Example usage (creating a network):

```sh
$ curl -i -X GET \
  --url http://localhost:8000/api/v1/status \
  --header 'Host: network-service-host.com'
```

```sh
$ curl --request POST \
    --url http://localhost:8000/api/v1/create-network \
    --header 'Host: network-service-host.com' \
    --header 'content-type: application/json' \
    --data '{
	  "networkId": "<unique id>",
	  "networkDetails": [
        {
          "machineId": "<unique id>",
          "machineType": "<host | switch>",
          "adjacentMachines": [<list of adjacent machine ids>]
        }
      ]
    }'
```

## Test Configuration

Run a dummy service:

```sh
$ cd dummy-service
$ docker build -t dummy-service .
$ docker run --rm --network=kong-net -it -p 5000:5000 dummy-service
```

Add dummy service to `kong.yml`:

```yml
- name: dummy-service
  url: http://host.docker.internal:5000
  routes:
  - name: dummy-routes
    paths:
    - /
```

Now that the dummy service is in `kong.yml`, build API Gateway:

```sh
$ docker build -t virtuoso-api-gateway .
$ docker run -it --rm --name kong \
     --network=kong-net \
     -p 8000:8000 \
     -p 8443:8443 \
     -p 8001:8001 \
     virtuoso-api-gateway
```

Test the endpoints:

```sh
$ curl --request GET \
  --url http://localhost:8000/api/v1/bar \
  --header 'host: host.docker.internal:5000'
```
