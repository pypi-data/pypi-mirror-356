from __future__ import annotations

from typing import Dict

import boto3


def whoami(env: Dict) -> str:
    """Return AWS identity ARN."""
    client = boto3.client("sts", region_name=env.get("region"))
    resp = client.get_caller_identity()
    return resp.get("Arn", "")

