import csv
from urllib.parse import urlparse

from .manager import VaultManager

__all__ = ["create_parser", "main"]


def create_parser(parser):
    """Configures the parser for the 'sync' command."""
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
        "-o",
        "--override-secrets",
        help="Path to a CSV file with secrets to override during restore",
    )
    parser.add_argument(
        "--override-column",
        help="Name of the column in the override CSV to use for values. Defaults to the destination hostname.",
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


def confirm_destructive_action(dest_hostname, dest_addr):
    print("\n" + "=" * 80)
    print("!! WARNING: DESTRUCTIVE OPERATION !!")
    print(
        "You are about to restore a snapshot that will completely OVERWRITE all existing data"
    )
    print(f"in the destination Vault at: {dest_addr}")
    print("=" * 80)
    confirmation = input(
        f"To confirm this action, please type the destination hostname '{dest_hostname}': "
    )
    if confirmation != dest_hostname:
        print("Confirmation failed. Aborting synchronization.")
        return False
    return True


def take_and_restore_snapshot(source_vault, destination_vault):
    try:
        print("Taking snapshot from source Vault...")
        snapshot = source_vault.take_raft_snapshot()
        print("Snapshot taken.")
    except Exception as e:
        print(f"Failed to take snapshot: {e}")
        return None
    try:
        print("Restoring snapshot to destination Vault...")
        result = destination_vault.restore_raft_snapshot(snapshot)
        print("Snapshot restored.")
        return result
    except Exception as e:
        print(f"Failed to restore snapshot: {e}")
        return None


def apply_overrides_if_needed(result, args, destination_vault, dest_hostname):
    if result is None or result.status_code != 204 or args.override_secrets is None:
        return
    destination_vault.authenticate_with_oidc(oidc_role=args.oidc_role)
    print(f"Applying overrides to destination Vault at {args.destination_vault_addr}")
    with open(args.override_secrets) as fin:
        reader = csv.reader(fin, dialect="excel-tab")
        headers = next(reader)
        header_map = {name.strip(): idx for idx, name in enumerate(headers)}
        override_column = (
            args.override_column if args.override_column else dest_hostname
        )
        required_headers = ["Secret", "Field", override_column]
        for col in required_headers:
            if col not in header_map:
                raise ValueError(f"Missing required column: {col}")
        idx_secret = header_map["Secret"]
        idx_field = header_map["Field"]
        idx_override = header_map[override_column]
        for row in reader:
            if (
                len(row) <= max(idx_secret, idx_field, idx_override)
                or not row[idx_secret]
                or not row[idx_field]
            ):
                continue
            secret_path = row[idx_secret].strip()
            field_key = row[idx_field].strip()
            override = row[idx_override].strip()
            try:
                secret = destination_vault.read_secret_path(secret_path)
                if secret is None:
                    print(
                        f"Warning: Cannot apply override for non-existent secret: {secret_path}"
                    )
                    continue
                secret[field_key] = override
                destination_vault.update_secret_path(secret_path, secret)
            except Exception as e:
                print(f"Error updating {secret_path}: {e}")
    print("Override apply complete.")


def main(args):
    source_vault = authenticate_vault(args.source_vault_addr, args.oidc_role)
    if not source_vault:
        return
    destination_vault = authenticate_vault(args.destination_vault_addr, args.oidc_role)
    if not destination_vault:
        return
    dest_hostname = urlparse(args.destination_vault_addr).hostname
    if not confirm_destructive_action(dest_hostname, args.destination_vault_addr):
        return
    result = take_and_restore_snapshot(source_vault, destination_vault)
    apply_overrides_if_needed(result, args, destination_vault, dest_hostname)
