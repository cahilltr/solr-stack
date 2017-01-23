from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.format import format
from resource_management.core.shell import call


def setup_solr_ssl_support():
    import params

    Execute(format('{zk_client_prefix}{solr_cloud_zk_directory} -cmd clusterprop -name urlScheme -val https'),
            ignore_failures=True,
            user=params.solr_config_user
            )


def remove_solr_ssl_support():
    import params

    code, output = call(format('{zk_client_prefix} -cmd get {solr_cloud_zk_directory}{clusterprops_json}'),
                        timeout=60
                        )

    if "NoNodeException" in output:
        return

    Execute(format('{zk_client_prefix} -cmd clear {solr_cloud_zk_directory}{clusterprops_json}'),
            ignore_failures=True,
            user=params.solr_config_user
            )
