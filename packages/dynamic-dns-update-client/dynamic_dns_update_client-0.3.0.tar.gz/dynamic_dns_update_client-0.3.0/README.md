[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/max-pfeiffer/dynamic-dns-update-client/graph/badge.svg?token=lPYop1verl)](https://codecov.io/gh/max-pfeiffer/dynamic-dns-update-client)
[![Pipeline](https://github.com/max-pfeiffer/dynamic-dns-update-client/actions/workflows/pipeline.yml/badge.svg)](https://github.com/max-pfeiffer/dynamic-dns-update-client/actions/workflows/pipeline.yml)

# Dynamic DNS Update Client
A CLI tool for updating the IP address at dynamic DNS providers.

Instead of supporting any dynamic DNS provider in the world (like almost any other tool I found), this CLI tool aims to
be a flexible tool kit. Using it, you can put together a solution which works for 90% of the use cases.

It obtains the current IP address by different means depending on the `--ip-address-provider` option:
* `openwrt_network` on an OpenWRT device by calling OpenWRT specific functions, specify network with `--ip-network`
* `interface` physical network interface to look for the public IP address, specify interface with `--ip-interface`
* by calling one of the following IP address services using an HTTP GET request:
  * [`ipify`](https://www.ipify.org/)
  * [`dyndns`](https://help.dyn.com/remote-access-api/checkip-tool/)


It then updates the obtained IP address with another HTTP GET request at the dynamic DNS provider using
the specified URL parameters and authentication method.

You can run it from any machine which has a Python v3 environment.

## Install
```shell
$ pip install dynamic-dns-update-client 
```

## Usage
For instance, executing:
```shell
$ dynamic-dns-update-client https://example.com --ip-address-url-parameter-name ip-address --url-parameter api-token=nd4u33huruffbn
```
Will result in calling: GET `https://example.com/?ip-address=172.16.31.10&api-token=nd4u33huruffbn`

```shell
$ dynamic-dns-update-client --help
Usage: dynamic-dns-update-client [OPTIONS] DYNAMIC_DNS_PROVIDER_URL

  Dynamic DNS Update Client.

  A CLI tool for updating the IP address for dynamic DNS providers. It obtains
  the current IP address by calling one the following IP address services
  using a HTTP GET request:

  - ipfy: https://www.ipify.org/

  - dyndns: https://help.dyn.com/remote-access-api/checkip-tool/

  It then updates the obtained IP address with another HTTP GET request at the
  dynamic DNS provider using the specified URL parameters and authentication
  method.

Options:
  --ip-address-provider [openwrt_network|interface|ipify|dyndns]
                                  Type of IP address provider. Default: ipify
  --ip-network TEXT               OpenWRT network to look for the public IP
                                  address. Default: wan
  --ip-interface TEXT             Physical interface to look for the public IP
                                  address. Default: eth0
  --ipv6                          Use IP V6 addresses.
  --ip-address-url-parameter-name TEXT
                                  Name of the URL parameter for IP address. It
                                  will be appended to the dynamic DNS provider
                                  URL.  [required]
  --url-parameter URL_PARAMETER   URL parameter which will be appended to the
                                  dynamic DNS provider URL. Format:
                                  param=value
  --basic-auth-username TEXT      Basic Auth username for calling dynamic DNS
                                  provider URL.
  --basic-auth-password TEXT      Basic Auth password for calling dynamic DNS
                                  provider URL.
  --dry-run                       Instead of calling the dynamic DNS provider,
                                  print the URL which would have been called.
  --help                          Show this message and exit.
```

## Environment Variables
If you are concerned about security and don't want to use the CLI options for secrets or passwords, you can also use
the following environment variables to provide these values to Dynamic DNS Update Client.
```shell
DYNAMIC_DNS_UPDATE_CLIENT_IP_ADDRESS_PROVIDER=ipify
DYNAMIC_DNS_UPDATE_CLIENT_IP_NETWORK=wan
DYNAMIC_DNS_UPDATE_CLIENT_IP_INTERFACE=eth0
DYNAMIC_DNS_UPDATE_CLIENT_IPV6=0
DYNAMIC_DNS_UPDATE_CLIENT_IP_ADDRESS_URL_PARAMETER_NAME=ip
DYNAMIC_DNS_UPDATE_CLIENT_URL_PARAMETER="foo=bar boom=bang cat=mouse"
DYNAMIC_DNS_UPDATE_CLIENT_BASIC_AUTH_USERNAME=username
DYNAMIC_DNS_UPDATE_CLIENT_BASIC_AUTH_PASSWORD=password
DYNAMIC_DNS_UPDATE_CLIENT_DRY_RUN=0
```