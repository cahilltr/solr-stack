from resource_management.core.resources.system import Execute, File
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.script.script import Script
from setup_solr import setup_solr
from setup_solr_cloud import setup_solr_cloud
from setup_solr_hdfs_support import setup_solr_hdfs_support
from setup_solr_ssl_support import setup_solr_ssl_support, remove_solr_ssl_support
from setup_solr_kerberos_auth import setup_solr_kerberos_auth, remove_solr_kerberos_auth
from solr_utils import solr_status_validation, solr_port_validation, delete_write_lock_files


class Solr(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Execute('mkdir -p /opt/lucidworks-hdpsearch')
        Execute(format('wget -qO- {solr_config_url} | tar xvz -C /opt/ && mv /opt/solr-* /opt/lucidworks-hdpsearch/solr'))


def configure(self, env):
    import params
    env.set_params(params)
    setup_solr()

    if params.solr_cloud_mode:
        setup_solr_cloud()

    if params.solr_ssl_enable:
        setup_solr_ssl_support()
    else:
        remove_solr_ssl_support()

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        if not solr_port_validation():
            exit(1)

        if not solr_status_validation():
            exit(1)

        start_command = format('{solr_config_bin_dir}/solr start -h {hostname}')

        if params.solr_cloud_mode:
            start_command += format(' -cloud -z {zookeeper_hosts}{solr_cloud_zk_directory}')

        start_command += format(' -p {solr_config_port} -m {solr_config_memory} >> {solr_config_service_log_file} 2>&1')

        Execute(
            start_command,
            environment={'JAVA_HOME': params.java64_home},            
            user=params.solr_config_user
        )

    def stop(self, env):
        import params
        env.set_params(params)

        Execute(
            format('{solr_config_bin_dir}/solr stop -all >> {solr_config_service_log_file} 2>&1'),
            environment={'JAVA_HOME': params.java64_home},
            user=params.solr_config_user
        )

        File(params.solr_config_pid_file,
             action="delete"
             )

    def status(self, env):
        import status_params
        env.set_params(status_params)

        check_process_status(status_params.solr_config_pid_file)


if __name__ == "__main__":
    Solr().execute()
