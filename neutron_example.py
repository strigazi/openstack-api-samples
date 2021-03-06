#!/usr/bin/python

import os
import sys
import argparse

from neutronclient.common.exceptions import *
import neutronclient.v2_0.client as neutronclient

# Import code common to all of the examples.
import common
import keystone_example


def get_neutron_client(keystone_client, args):
    # Find an endpoint for the 'image' service.
    endpoint = keystone_client.service_catalog.url_for(
        service_type='network',
        endpoint_type='publicURL')

    # Authenticate to neutron using our Keystone token.
    nc = neutronclient.Client(
        endpoint_url=endpoint,
        token=keystone_client.auth_token,
        tenant_id=args.os_tenant_id,
        auth_url=args.os_auth_url)

    return nc

def parse_args():
    p = common.create_parser()
    return p.parse_args()

def main():
    args = parse_args()
    kc = keystone_example.get_keystone_client(
        os_username=args.os_username,
        os_password=args.os_password,
        os_tenant_name=args.os_tenant_name,
        os_tenant_id=args.os_tenant_id,
        os_auth_url=args.os_auth_url
    )

    # Find an endpoint for the 'image' service.
    endpoint = kc.service_catalog.url_for(
        service_type='network',
        endpoint_type='publicURL')

    # Authenticate to neutron using our Keystone token.
    nc = get_neutron_client(kc, args)

    networks = nc.list_networks()
    for network in networks.get('networks', []):
        print network['id'], network['name']
        for subnet in network['subnets']:
            try:
                data = nc.show_subnet(subnet)
                print '    ', subnet, data['subnet']['cidr']
            except NeutronClientException:
                print '    ', subnet, 'not found'


if __name__ == '__main__':
    main()

