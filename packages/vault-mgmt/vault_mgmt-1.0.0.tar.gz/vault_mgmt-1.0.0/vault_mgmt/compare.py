import csv
import os
import sys
from urllib.parse import urlparse

from tqdm import tqdm

from .manager import VaultManager

__all__ = ["create_parser", "main"]


def create_parser(parser):
    """Configures the parser for the 'compare' command."""
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    default_output = f"{script_name}_results.csv"

    parser.add_argument(
        "-s",
        "--source-vault-addr",
        required=True,
        help='Address of the source Vault (e.g., "http://127.0.0.1:8200")',
    )
    parser.add_argument(
        "-d",
        "--destination-vault-addr",
        required=True,
        help='Address of the destination Vault (e.g., "http://127.0.0.1:8200")',
    )
    parser.add_argument("-r", "--oidc-role", help="OIDC role for authentication")
    parser.add_argument(
        "-b", "--base-path", default="", help="Base path for secrets to synchronize"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        default=default_output,
        help=f"Path to tab-delimited CSV output file (default: {default_output})",
    )
    parser.add_argument(
        "--ignore-path",
        action="append",
        default=[],
        help="Path to ignore during comparison. Can be specified multiple times.",
    )


def authenticate_vault(addr, oidc_role):
    vault = VaultManager(addr)
    try:
        vault.authenticate_with_oidc(oidc_role=oidc_role)
        print(f"Authenticated with Vault at {addr}")
        return vault
    except Exception as e:
        print(f"Failed to authenticate with Vault: {e}")
        return None


def get_filtered_secret_paths(vault, base_path, ignore_paths):
    paths = set(vault.list_all_secret_paths(base_path=base_path))
    for ignore in ignore_paths:
        paths = {p for p in paths if ignore not in p}
    return paths


def compare_secrets(source_vault, dest_vault, common_paths):
    results = []
    for secret_path in tqdm(common_paths, desc="Comparing secrets"):
        try:
            source_secret = source_vault.read_secret_path(secret_path)
            destination_secret = dest_vault.read_secret_path(secret_path)
            if source_secret != destination_secret:
                source_secret = source_secret or {}
                destination_secret = destination_secret or {}
                all_keys = set(source_secret.keys()) | set(destination_secret.keys())
                for field in all_keys:
                    source_field = source_secret.get(field)
                    destination_field = destination_secret.get(field)
                    if source_field != destination_field:
                        results.append(
                            [secret_path, field, source_field, destination_field]
                        )
        except Exception as e:
            print(f"Failed to compare secret at path '{secret_path}': {e}")
    return results


def write_results_to_csv(results, args):
    if results:
        with open(args.output_file, mode="w", newline="") as fout:
            writer = csv.writer(fout, dialect="excel-tab")
            writer.writerow(
                [
                    "Secret",
                    "Field",
                    f"{urlparse(args.source_vault_addr).hostname}",
                    f"{urlparse(args.destination_vault_addr).hostname}",
                ]
            )
            writer.writerows(results)
        print(
            f"\nCompare complete. Found {len(results)} differences. Results saved to {args.output_file}"
        )
    else:
        print("\nCompare complete. No differences found. No output file written.")


def main(args):
    """Main logic for comparing secrets."""
    source_vault = authenticate_vault(args.source_vault_addr, args.oidc_role)
    if not source_vault:
        return
    destination_vault = authenticate_vault(args.destination_vault_addr, args.oidc_role)
    if not destination_vault:
        return
    print(f"Listing secret paths from source Vault at base path '{args.base_path}/'...")
    source_secret_paths = get_filtered_secret_paths(
        source_vault, args.base_path, args.ignore_path
    )
    print(f"Found {len(source_secret_paths)} secret paths in source.")
    print(
        f"Listing secret paths from destination Vault at base path '{args.base_path}/'..."
    )
    destination_secret_paths = get_filtered_secret_paths(
        destination_vault, args.base_path, args.ignore_path
    )
    print(f"Found {len(destination_secret_paths)} secret paths in destination.")
    common_paths = source_secret_paths & destination_secret_paths
    print(f"Found {len(common_paths)} common secrets to compare...")
    results = compare_secrets(source_vault, destination_vault, common_paths)
    write_results_to_csv(results, args)
