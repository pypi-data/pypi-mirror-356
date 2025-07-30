import sys

from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from tqdm import tqdm

from .manager import VaultManager

__all__ = ["create_parser", "main"]


def is_pod_ready(pod: client.V1Pod) -> bool:
    """Checks if a V1Pod is in the 'Ready' condition."""
    if not pod.status or not pod.status.conditions:
        return False

    return any(condition.type == "Ready" and condition.status == "True" for condition in pod.status.conditions)


def create_parser(parser):
    """Configures the parser for the 'rollout' command."""
    parser.add_argument(
        "namespace",
        nargs="?",
        default="vault",
        help="The Kubernetes namespace where Vault is running.",
    )
    parser.add_argument(
        "--vault-addr",
        required=True,
        help='Address of the Vault (e.g., "http://127.0.0.1:8200")',
    )
    parser.add_argument("-r", "--oidc-role", help="OIDC role for Vault authentication")
    parser.add_argument(
        "--kube-context",
        default=None,
        help="The kubeconfig context to use. If not specified, uses the current context or in-cluster config.",
    )


def main(args):
    """Main logic for rolling restart."""
    # Initialize and authenticate VaultManager
    vault_client = VaultManager(args.vault_addr)
    try:
        vault_client.authenticate_with_oidc(oidc_role=args.oidc_role)
        print(f"Authenticated with Vault at {args.vault_addr}")
    except Exception as e:
        print(f"Failed to authenticate with Vault: {e}")
        return

    if not vault_client.is_authenticated():
        print("Error: Vault token is missing or invalid.")
        sys.exit(2)

    vault_version = vault_client.get_vault_version()
    if vault_version:
        print(f"Confirmed initial Vault version: {vault_version}")
    else:
        print("Could not determine initial Vault version. Exiting.")
        sys.exit(1)

    perform_vault_rollout(args.namespace, vault_client, args.kube_context)


def load_kube_config_or_incluster(context_to_load):
    try:
        if not context_to_load:
            contexts, active_context = config.list_kube_config_contexts()
            if not active_context:
                raise config.ConfigException(
                    "Could not find a default context in kubeconfig."
                )
            context_to_load = active_context["name"]
        print(f"Loading Kubernetes configuration using context: '{context_to_load}'")
        config.load_kube_config(context=context_to_load)
    except (config.ConfigException, FileNotFoundError):
        try:
            print("Kubeconfig not found. Attempting to load in-cluster configuration...")
            config.load_incluster_config()
        except config.ConfigException as e:
            print("Could not load any Kubernetes configuration. Exiting.")
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    return client.CoreV1Api()


def rollout_standby_pods(k8s_core_v1, namespace):
    print("\n--- Phase 1: Rolling out standby pods ---")
    try:
        standby_pods = k8s_core_v1.list_namespaced_pod(
            namespace=namespace, label_selector="vault-active=false"
        )
        with tqdm(standby_pods.items, desc="Standby Pods", unit="pod") as pbar:
            for pod in pbar:
                pod_name = pod.metadata.name
                pod_uid = pod.metadata.uid
                pbar.set_description(f"Deleting pod {pod_name}")
                k8s_core_v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
                pbar.set_description(f"Waiting for {pod_name} to be ready")
                w = watch.Watch()
                for event in w.stream(
                    k8s_core_v1.list_namespaced_pod,
                    namespace=namespace,
                    field_selector=f"metadata.name={pod_name}",
                    timeout_seconds=300,
                ):
                    new_pod = event["object"]  # type: ignore
                    if new_pod.metadata.uid != pod_uid and is_pod_ready(new_pod):  # type: ignore
                        w.stop()
                        break
    except ApiException as e:
        print(f"Error handling standby pods: {e}")
        sys.exit(1)


def handle_active_pod(k8s_core_v1, namespace, vault_client):
    print("\n--- Phase 2: Handling active pod ---")
    try:
        with tqdm(total=5, desc="Active Pod Steps") as pbar:
            active_pods = k8s_core_v1.list_namespaced_pod(
                namespace=namespace, label_selector="vault-active=true"
            )
            if not active_pods.items:
                print(
                    "\nWarning: No active Vault pod found. Skipping step-down.",
                    file=sys.stderr,
                )
                return
            old_active_pod = active_pods.items[0]
            old_active_pod_name = old_active_pod.metadata.name
            old_active_pod_uid = old_active_pod.metadata.uid
            pbar.update(1)
            pbar.set_description(f"Stepping down {old_active_pod_name}")
            vault_client.step_down()
            pbar.update(1)
            pbar.set_description("Waiting for new leader")
            w = watch.Watch()
            for event in w.stream(
                k8s_core_v1.list_namespaced_pod,
                namespace=namespace,
                label_selector="vault-active=true",
                timeout_seconds=120,
            ):
                pod = event["object"]  # type: ignore
                if pod.metadata.name != old_active_pod_name and is_pod_ready(pod):  # type: ignore
                    pbar.set_description(f"New leader {pod.metadata.name} ready")  # type: ignore
                    w.stop()
                    break
            pbar.update(1)
            pbar.set_description(f"Deleting old pod {old_active_pod_name}")
            k8s_core_v1.delete_namespaced_pod(
                name=old_active_pod_name, namespace=namespace
            )
            pbar.update(1)
            pbar.set_description(f"Waiting for {old_active_pod_name} to restart")
            w = watch.Watch()
            for event in w.stream(
                k8s_core_v1.list_namespaced_pod,
                namespace=namespace,
                field_selector=f"metadata.name={old_active_pod_name}",
                timeout_seconds=300,
            ):
                restarted_pod = event["object"]  # type: ignore
                if restarted_pod.metadata.uid != old_active_pod_uid and is_pod_ready(restarted_pod):  # type: ignore
                    w.stop()
                    break
            pbar.update(1)
        print("Vault rollout complete.")
        print("\nConfirming Vault version post-rollout...")
        vault_version = vault_client.get_vault_version()
        if vault_version:
            print(f"Confirmed finale Vault version: {vault_version}")
        else:
            print("Could not determine final Vault version. Exiting.")
    except ApiException as e:
        print(f"Kubernetes API error handling active pod: {e}")


def perform_vault_rollout(
    namespace: str, vault_client: VaultManager, kube_context: str
):
    k8s_core_v1 = load_kube_config_or_incluster(kube_context)
    rollout_standby_pods(k8s_core_v1, namespace)
    handle_active_pod(k8s_core_v1, namespace, vault_client)
