"""Command line interface."""

# ruff: noqa: D301, D401

import click

from dynamic_dns_update_client.dyn_dns_update import update_dyn_dns_provider
from dynamic_dns_update_client.ip_address import IpAddressProviderType, get_ip_address
from dynamic_dns_update_client.types import UrlParameterType, UrlType


@click.command()
@click.argument(
    "dynamic_dns_provider_url",
    type=UrlType(),
    required=True,
)
@click.option(
    "--ip-address-provider",
    envvar="DYNAMIC_DNS_UPDATE_CLIENT_IP_ADDRESS_PROVIDER",
    type=click.Choice(IpAddressProviderType, case_sensitive=False),
    default=IpAddressProviderType.IPIFY,
    help=f"Type of IP address provider. Default: {IpAddressProviderType.IPIFY.value}",
)
@click.option(
    "--ip-network",
    envvar="DYNAMIC_DNS_UPDATE_CLIENT_IP_NETWORK",
    default="wan",
    help="OpenWRT network to look for the public IP address. Default: wan",
)
@click.option(
    "--ip-interface",
    envvar="DYNAMIC_DNS_UPDATE_CLIENT_IP_INTERFACE",
    default="eth0",
    help="Physical interface to look for the public IP address. Default: eth0",
)
@click.option(
    "--ipv6",
    envvar="DYNAMIC_DNS_UPDATE_CLIENT_IPV6",
    is_flag=True,
    help="Use IP V6 addresses.",
)
@click.option(
    "--ip-address-url-parameter-name",
    envvar="DYNAMIC_DNS_UPDATE_CLIENT_IP_ADDRESS_URL_PARAMETER_NAME",
    required=True,
    help="Name of the URL parameter for IP address. "
    "It will be appended to the dynamic DNS provider URL.",
)
@click.option(
    "--url-parameter",
    envvar="DYNAMIC_DNS_UPDATE_CLIENT_URL_PARAMETER",
    type=UrlParameterType(),
    multiple=True,
    help="URL parameter which will be appended to the dynamic DNS provider URL. "
    "Format: param=value",
)
@click.option(
    "--basic-auth-username",
    envvar="DYNAMIC_DNS_UPDATE_CLIENT_BASIC_AUTH_USERNAME",
    help="Basic Auth username for calling dynamic DNS provider URL.",
)
@click.option(
    "--basic-auth-password",
    envvar="DYNAMIC_DNS_UPDATE_CLIENT_BASIC_AUTH_PASSWORD",
    help="Basic Auth password for calling dynamic DNS provider URL.",
)
def cli(
    dynamic_dns_provider_url: str,
    ip_address_provider: IpAddressProviderType,
    ip_network: str,
    ip_interface: str,
    ipv6: bool,
    ip_address_url_parameter_name: str,
    url_parameter: list[str] | None,
    basic_auth_username: str | None,
    basic_auth_password: str | None,
) -> None:
    """Dynamic DNS Update Client.

    A CLI tool for updating the IP address for dynamic DNS providers.
    It obtains the current IP address by calling one the following IP address services
    using a HTTP GET request:

    - ipfy: https://www.ipify.org/

    - dyndns: https://help.dyn.com/remote-access-api/checkip-tool/

    It then updates the obtained IP address with another HTTP GET request at the dynamic
    DNS provider using the specified URL parameters and authentication method.

    \f

    :param dynamic_dns_provider_url:
    :param ip_address_provider:
    :param ip_network:
    :param ip_interface:
    :param ipv6:
    :param ip_address_url_parameter_name:
    :param url_parameter:
    :param basic_auth_username:
    :param basic_auth_password:
    :return:
    """
    if basic_auth_username and basic_auth_password is None:
        raise click.BadOptionUsage(
            "--basic-auth-password", "Please specify also a Basic Auth password."
        )
    if basic_auth_password and basic_auth_username is None:
        raise click.BadOptionUsage(
            "--basic-auth-username", "Please specify also a Basic Auth username."
        )

    current_ip_address: str = get_ip_address(
        ip_address_provider, ip_network, ip_interface, ipv6
    )
    click.echo(f"Current IP address: {current_ip_address}")

    update_dyn_dns_provider(
        dynamic_dns_provider_url,
        ip_address_url_parameter_name,
        url_parameter,
        basic_auth_username,
        basic_auth_password,
        current_ip_address,
    )
    click.echo("The IP address was successfully updated at the dynamic DNS provider.")
