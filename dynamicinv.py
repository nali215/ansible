#!/usr/bin/env python3

'''
Example custom dynamic inventory script for Ansible, in Python.
'''

import os
import sys
import argparse
import psycopg2
import requests
from configparser import ConfigParser
#from config import config

try:
    import json
except ImportError:
    import simplejson as json

class ExampleInventory(object):
# Example inventory for testing.

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.example_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print (json.dumps(self.inventory))


# Example inventory for testing.
    def example_inventory(self):
        conn = None
        conn = psycopg2.connect("host=10.10.0.50 dbname=testdb user=naveed password=adminpass")
        cur = conn.cursor()
        cur.execute('SELECT host_ip, host_type, host_name from ipadd')
        hosts = cur.fetchall()
        hostip = []
        masterip = []
        for row in hosts:
            if row[1]=="master":
                masterip.append(row[0])
            else:
                hostip.append(row[0])
        cur.close()
        ipadd = ', '.join(hostip)
        masteripadd = ','.join(masterip)
        return {
            'master':{
                'hosts':[masteripadd],
                'vars': {

                    'example_variable': 'value'
                    }
            },

            'workernodes':{
                'hosts':[ipadd],
                'vars': {
                    'example_variable': 'value'
                    }
            },

            '_meta': {
                'hostvars': {
                    '192.168.28.71': {
                        'host_specific_var': 'foo'
                    },
                    '192.168.28.72': {
                        'host_specific_var': 'bar'
                        }
                    }
                }
            }


    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

# Get the inventory.
ExampleInventory()
                                
