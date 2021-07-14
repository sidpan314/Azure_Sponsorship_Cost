from azure.common.credentials import (
    ServicePrincipalCredentials,
    get_azure_cli_credentials,
)
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.privatedns import PrivateDnsManagementClient
from azure.mgmt.recoveryservices import RecoveryServicesClient
from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.loganalytics import LogAnalyticsDataClient
from canalyzer.analyzer import configuration

credential = ClientSecretCredential(
    configuration.tenant_id,
    configuration.client_id,
    configuration.client_secret,
)
loganalytics_credential = ServicePrincipalCredentials(
    tenant=configuration.tenant_id,
    client_id=configuration.client_id,
    secret=configuration.client_secret,
    resource="https://api.loganalytics.io",
)

resource_client = ResourceManagementClient(credential, configuration.subscription_id)
compute_client = ComputeManagementClient(credential, configuration.subscription_id)
network_client = NetworkManagementClient(credential, configuration.subscription_id)
storage_client = StorageManagementClient(credential, configuration.subscription_id)
sql_client = SqlManagementClient(credential, configuration.subscription_id)
dns_client = DnsManagementClient(credential, configuration.subscription_id)
subscription_client = SubscriptionClient(credential)
log_analytics_data_client = LogAnalyticsDataClient(loganalytics_credential)
log_analytics_client = LogAnalyticsManagementClient(
    credential, configuration.subscription_id
)
container_registry_client = ContainerRegistryManagementClient(
    credential, configuration.subscription_id
)
private_dns_client = PrivateDnsManagementClient(
    credential, configuration.subscription_id
)
recovery_service_client = RecoveryServicesClient(
    credential, configuration.subscription_id
)
recovery_service_backup_client = RecoveryServicesBackupClient(
    credential, configuration.subscription_id
)
monitor_management_client = MonitorManagementClient(
    credential, configuration.subscription_id
)
