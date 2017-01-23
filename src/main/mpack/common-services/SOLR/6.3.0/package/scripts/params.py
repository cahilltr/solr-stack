#!/usr/bin/env python

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import get_kinit_path

import status_params
import functools


def build_zookeeper_hosts():
    zookeeper_hosts_length = len(zookeeper_hosts_list)
    response = ''
    for i, val in enumerate(zookeeper_hosts_list):
        response += val + ':' + zk_client_port
        if (i + 1) < zookeeper_hosts_length:
            response += ','
    return response


config = Script.get_config()

java64_home = config['hostLevelParams']['java_home']
hostname = config['hostname']
zk_client_port = str(default('/configurations/zoo.cfg/clientPort', None))
zookeeper_hosts_list = config['clusterHostInfo']['zookeeper_hosts']
zookeeper_hosts = build_zookeeper_hosts()

map_solr_config = config['configurations']['solr-config-env']
solr_config_url = map_solr_config['solr_config_url']
solr_config_user = map_solr_config['solr_config_user']
solr_hdfs_home_directory = '/user/' + solr_config_user
solr_config_group = map_solr_config['solr_config_group']
solr_config_port = status_params.solr_config_port
solr_config_memory = map_solr_config['solr_config_memory']
solr_config_log_dir = map_solr_config['solr_config_log_dir']
solr_config_service_log_dir = map_solr_config['solr_config_service_log_dir']
solr_config_service_log_file = format('{solr_config_service_log_dir}/solr-service.log')
solr_config_conf_dir = map_solr_config['solr_config_conf_dir']
solr_config_data_dir = map_solr_config['solr_config_data_dir']
solr_config_in_sh = map_solr_config['content']
solr_hostname = hostname

log4j_properties = config['configurations']['solr-log4j']['content']

solr_config_dir = '/opt/lucidworks-hdpsearch/solr'
solr_config_bin_dir = format('{solr_config_dir}/bin')
solr_config_pid_dir = status_params.solr_config_pid_dir
solr_config_pid_file = status_params.solr_config_pid_file
solr_webapp_dir = format('{solr_config_dir}/server/solr-webapp')

# solr cloud
cloud_scripts = format('{solr_config_dir}/server/scripts/cloud-scripts')
map_solr_cloud = config['configurations']['solr-cloud']
solr_cloud_mode = map_solr_cloud['solr_cloud_enable']
solr_cloud_zk_directory = map_solr_cloud['solr_cloud_zk_directory']
zk_client_prefix = format('export JAVA_HOME={java64_home}; {cloud_scripts}/zkcli.sh -zkhost {zookeeper_hosts}')
clusterprops_json = '/clusterprops.json'
clusterstate_json = '/clusterstate.json'

# solr collection sample
map_example_collection = config['configurations']['example-collection']
solr_collection_sample_create = bool(map_example_collection['solr_collection_sample_create'])
solr_collection_name = map_example_collection['solr_collection_sample_name']
solr_collection_config_dir = map_example_collection['solr_collection_sample_config_directory']
solr_collection_shards = str(map_example_collection['solr_collection_sample_shards'])
solr_collection_replicas = str(map_example_collection['solr_collection_sample_replicas'])
