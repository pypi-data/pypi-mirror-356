from typing import Dict, Any

from rich.console import Console
from rich.table import Table
import typer

app = typer.Typer(help="IAM related commands")


def _policy_allows_admin(policy: Dict[str, Any]) -> bool:
    """Return True if the policy document grants full admin permissions."""
    statements = policy.get("Statement", [])
    if not isinstance(statements, list):
        statements = [statements]
    for stmt in statements:
        if stmt.get("Effect") != "Allow":
            continue
        actions = stmt.get("Action")
        resources = stmt.get("Resource")
        if actions == "*" or actions == ["*"] or (isinstance(actions, list) and "*" in actions):
            if resources == "*" or resources == ["*"] or (isinstance(resources, list) and "*" in resources):
                return True
    return False


@app.command()
def check():
    """List IAM users and highlight those with admin-level permissions."""
    try:
        import boto3  # type: ignore
    except ImportError:
        typer.echo("boto3 is required for this command")
        raise typer.Exit(code=1)

    iam = boto3.client("iam")
    console = Console()
    table = Table(title="IAM Users", show_header=True, header_style="bold magenta")
    table.add_column("User", style="cyan")
    table.add_column("Admin Access")

    paginator = iam.get_paginator("list_users")
    for page in paginator.paginate():
        for user in page.get("Users", []):
            user_name = user["UserName"]
            is_admin = False

            # Check attached user policies
            aup = iam.list_attached_user_policies(UserName=user_name)
            for policy in aup.get("AttachedPolicies", []):
                if "AdministratorAccess" in policy.get("PolicyName", ""):
                    is_admin = True
                    break
                pol = iam.get_policy(PolicyArn=policy["PolicyArn"])
                version_id = pol["Policy"]["DefaultVersionId"]
                version = iam.get_policy_version(PolicyArn=policy["PolicyArn"], VersionId=version_id)
                doc = version["PolicyVersion"]["Document"]
                if _policy_allows_admin(doc):
                    is_admin = True
                    break

            if not is_admin:
                # Inline user policies
                for pname in iam.list_user_policies(UserName=user_name).get("PolicyNames", []):
                    pol = iam.get_user_policy(UserName=user_name, PolicyName=pname)
                    doc = pol.get("PolicyDocument", {})
                    if _policy_allows_admin(doc):
                        is_admin = True
                        break

            if not is_admin:
                # Group policies
                for grp in iam.list_groups_for_user(UserName=user_name).get("Groups", []):
                    grp_name = grp["GroupName"]
                    for policy in iam.list_attached_group_policies(GroupName=grp_name).get("AttachedPolicies", []):
                        if "AdministratorAccess" in policy.get("PolicyName", ""):
                            is_admin = True
                            break
                        pol = iam.get_policy(PolicyArn=policy["PolicyArn"])
                        version_id = pol["Policy"]["DefaultVersionId"]
                        version = iam.get_policy_version(PolicyArn=policy["PolicyArn"], VersionId=version_id)
                        doc = version["PolicyVersion"]["Document"]
                        if _policy_allows_admin(doc):
                            is_admin = True
                            break
                    if is_admin:
                        break
            badge = "[red]⚠️ admin[/red]" if is_admin else ""
            table.add_row(user_name, badge)

    console.print(table)
