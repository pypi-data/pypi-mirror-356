from typing import Dict
from typing import List
from typing import Optional

import click

from tecton import tecton_context
from tecton._internals.infra_operations import create_feature_server_cache
from tecton._internals.infra_operations import create_feature_server_group
from tecton._internals.infra_operations import create_ingest_server_group
from tecton._internals.infra_operations import create_transform_server_group
from tecton._internals.infra_operations import delete_feature_server_cache
from tecton._internals.infra_operations import delete_feature_server_group
from tecton._internals.infra_operations import delete_ingest_server_group
from tecton._internals.infra_operations import delete_transform_server_group
from tecton._internals.infra_operations import get_feature_server_cache
from tecton._internals.infra_operations import get_feature_server_group
from tecton._internals.infra_operations import get_ingest_server_group
from tecton._internals.infra_operations import get_realtime_logs
from tecton._internals.infra_operations import get_transform_server_group
from tecton._internals.infra_operations import list_feature_server_caches
from tecton._internals.infra_operations import list_feature_server_groups
from tecton._internals.infra_operations import list_ingest_server_groups
from tecton._internals.infra_operations import list_transform_server_groups
from tecton._internals.infra_operations import update_feature_server_cache
from tecton._internals.infra_operations import update_feature_server_group
from tecton._internals.infra_operations import update_ingest_server_group
from tecton._internals.infra_operations import update_transform_server_group
from tecton.cli import printer
from tecton.cli.cli_utils import click_exception_wrapper
from tecton.cli.cli_utils import display_table
from tecton.cli.cli_utils import timestamp_to_string
from tecton.cli.command import TectonCommand
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import AutoscalingConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import FeatureServerCache
from tecton_proto.servergroupservice.server_group_service__client_pb2 import FeatureServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetRealtimeLogsResponse
from tecton_proto.servergroupservice.server_group_service__client_pb2 import IngestServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ProvisionedScalingConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import Status
from tecton_proto.servergroupservice.server_group_service__client_pb2 import TransformServerGroup


INFO_SIGN = "💡"


def _get_validated_workspace(workspace_name: Optional[str]) -> str:
    """Gets the workspace name, falling back to current context, and exits if none is found."""
    workspace = workspace_name or tecton_context.get_current_workspace()
    if not workspace:
        msg = "No workspace selected. Please specify a workspace with --workspace or run 'tecton workspace select <workspace>'"
        raise click.ClickException(msg)
    return workspace


def _get_scaling_config_str(
    autoscaling_config: Optional[AutoscalingConfig], provisioned_scaling_config: Optional[ProvisionedScalingConfig]
) -> str:
    if autoscaling_config is not None:
        return f"Autoscaling (Min:{autoscaling_config.min_nodes}, Max:{autoscaling_config.max_nodes})"
    elif provisioned_scaling_config:
        return f"Provisioned (Desired:{provisioned_scaling_config.desired_nodes})"
    return ""


def _get_pairs_str(pairs: Dict[str, str]) -> str:
    return ", ".join(f"{k}={v}" for k, v in pairs.items()) if pairs else ""


def _get_color_for_status(status):
    status_name = Status.Name(status)
    color_map = {"READY": "green", "CREATING": "cyan", "UPDATING": "yellow", "DELETING": "red"}
    return color_map.get(status_name, "white")


def _get_colored_status(status):
    """Get a colored status display using Rich Text formatting."""
    from rich.text import Text

    status_name = Status.Name(status)
    color = _get_color_for_status(status)
    return Text(status_name, style=color)


def _parse_pairs_str(pairs_str: str, var_name: str) -> Dict[str, str]:
    if pairs_str is None:
        return None
    pairs = {}
    for pair in pairs_str.split(","):
        if not pair or pair.count("=") != 1:
            msg = f"Invalid {var_name} format. Expected format: KEY1=VALUE1,KEY2=VALUE2"
            raise click.ClickException(msg)
        k, v = pair.split("=")
        pairs[k] = v
    return pairs


def _create_multi_line_display(
    current_value: str, pending_value: str, pending_color: str, prefix: str = "Pending"
) -> Dict:
    """Helper function to create multi-line display for current and pending values."""
    if current_value == "":
        current_value = "None"

    return {
        "type": "multi_line",
        "lines": [
            {"text": current_value, "style": "dim"},
            {"text": f"{prefix}: {pending_value}", "style": f"{pending_color}"},
        ],
    }


def _process_pending_scaling_config(current_scaling: str, pending_config, pending_color: str):
    """Process pending scaling configuration for any server group type."""
    if not pending_config:
        return current_scaling

    has_pending_scaling = pending_config.HasField("autoscaling_config") or pending_config.HasField("provisioned_config")

    if has_pending_scaling:
        pending_scaling = _get_scaling_config_str(
            pending_config.autoscaling_config if pending_config.HasField("autoscaling_config") else None,
            pending_config.provisioned_config if pending_config.HasField("provisioned_config") else None,
        )
        return _create_multi_line_display(current_scaling, pending_scaling, pending_color)

    return current_scaling


def _process_pending_field(current_value: str, pending_config, field_name: str, pending_color: str):
    """Process any pending field for display."""
    if not pending_config:
        return current_value

    # Handle map fields (like environment_variables) differently from optional fields
    if field_name == "environment_variables":
        pending_value = getattr(pending_config, field_name, {})
        if not pending_value:
            return current_value
    else:
        if not pending_config.HasField(field_name) or getattr(pending_config, field_name) == "":
            return current_value
        pending_value = getattr(pending_config, field_name)

    if isinstance(pending_value, dict):
        pending_value = _get_pairs_str(pending_value)

    return _create_multi_line_display(current_value, pending_value, pending_color)


@click.command(
    "feature-server-cache",
    cls=TectonGroup,
    command_category=TectonCommandCategory.INFRA,
    hidden=True,
)
def feature_server_cache():
    """Provision and manage Feature Server Caches."""


def _extract_metadata(obj):
    """Extract description and tags from metadata field."""
    description = ""
    tags = {}
    if obj.HasField("metadata"):
        description = obj.metadata.description if obj.metadata.HasField("description") else ""
        tags = obj.metadata.tags
    return description, tags


def _extract_server_fields(server_or_servers, single=False, field_config=None):
    """
    Generic function to extract fields for any server type display.

    Args:
        server_or_servers: Single server object or list of servers
        single: Whether this is for single-item display
        field_config: Dictionary containing field extraction configuration
    """
    if field_config is None:
        field_config = {}

    if single:
        server = server_or_servers
        data = []

        data.extend(
            [
                ("ID", server.id),
                ("Workspace", server.workspace),
                ("Name", server.name),
                ("Status", _get_colored_status(server.status)),
                ("Status Details", server.status_details or ""),
            ]
        )

        if field_config.get("has_scaling", True):
            current_scaling = _get_scaling_config_str(
                getattr(server, "autoscaling_config", None) if server.HasField("autoscaling_config") else None,
                getattr(server, "provisioned_config", None) if server.HasField("provisioned_config") else None,
            )
            pending_config = getattr(server, "pending_config", None) if server.HasField("pending_config") else None
            pending_color = _get_color_for_status(server.status)
            scaling_display = _process_pending_scaling_config(current_scaling, pending_config, pending_color)
            data.append(("Scaling", scaling_display))

        if field_config.get("has_node_type", True):
            pending_config = getattr(server, "pending_config", None) if server.HasField("pending_config") else None
            pending_color = _get_color_for_status(server.status)
            node_type_display = _process_pending_field(server.node_type, pending_config, "node_type", pending_color)
            data.append(("Node Type", node_type_display))

        if field_config.get("has_cache_fields", False):
            data.extend(
                [
                    ("Num Shards", server.provisioned_config.num_shards),
                    ("Num Replicas", server.provisioned_config.num_replicas_per_shard),
                    ("Preferred Maintenance Window", server.preferred_maintenance_window or ""),
                ]
            )

        if field_config.get("has_cache_id", False):
            data.extend(
                [
                    ("Cache ID", server.cache_id or ""),
                ]
            )

        if field_config.get("has_environment", False):
            current_env_vars = _get_pairs_str(server.environment_variables)
            pending_config = getattr(server, "pending_config", None) if server.HasField("pending_config") else None
            pending_color = _get_color_for_status(server.status)
            environment_display = _process_pending_field(
                server.environment, pending_config, "environment", pending_color
            )
            env_vars_display = _process_pending_field(
                current_env_vars, pending_config, "environment_variables", pending_color
            )
            data.extend(
                [
                    ("Environment", environment_display),
                    ("Environment Variables", env_vars_display),
                ]
            )

        if field_config.get("has_metadata", True):
            description, tags = _extract_metadata(server)
            data.extend(
                [
                    ("Description", description),
                    ("Tags", _get_pairs_str(tags)),
                ]
            )

        data.extend(
            [
                ("Created At", timestamp_to_string(server.created_at)),
                ("Updated At", timestamp_to_string(server.updated_at)),
            ]
        )

        headings = ("Field", "Value")
        return headings, data

    else:
        # Multi-item display
        headings = field_config.get("multi_headings", ["ID", "Workspace", "Name", "Status", "Updated At"])

        rows = []
        for server in server_or_servers:
            row_data = []

            for heading in headings:
                if heading == "ID":
                    row_data.append(server.id)
                elif heading == "Workspace":
                    row_data.append(server.workspace)
                elif heading == "Name":
                    row_data.append(server.name)
                elif heading == "Status":
                    row_data.append(_get_colored_status(server.status))
                elif heading == "Scaling":
                    current_scaling = _get_scaling_config_str(
                        getattr(server, "autoscaling_config", None) if server.HasField("autoscaling_config") else None,
                        getattr(server, "provisioned_config", None) if server.HasField("provisioned_config") else None,
                    )
                    pending_config = (
                        getattr(server, "pending_config", None) if server.HasField("pending_config") else None
                    )
                    pending_color = _get_color_for_status(server.status)
                    row_data.append(_process_pending_scaling_config(current_scaling, pending_config, pending_color))
                elif heading == "Node Type":
                    pending_config = (
                        getattr(server, "pending_config", None) if server.HasField("pending_config") else None
                    )
                    pending_color = _get_color_for_status(server.status)
                    row_data.append(
                        _process_pending_field(server.node_type, pending_config, "node_type", pending_color)
                    )
                elif heading == "Cache ID":
                    row_data.append(server.cache_id or "")
                elif heading == "Pending Config":
                    row_data.append(server.pending_config or "")
                elif heading == "Num Shards":
                    row_data.append(server.provisioned_config.num_shards)
                elif heading == "Num Replicas":
                    row_data.append(server.provisioned_config.num_replicas_per_shard)
                elif heading == "Preferred Maintenance Window":
                    row_data.append(server.preferred_maintenance_window or "")
                elif heading == "Environment":
                    pending_config = (
                        getattr(server, "pending_config", None) if server.HasField("pending_config") else None
                    )
                    pending_color = _get_color_for_status(server.status)
                    row_data.append(
                        _process_pending_field(server.environment, pending_config, "environment", pending_color)
                    )
                elif heading == "Environment Variables":
                    current_env_vars = _get_pairs_str(server.environment_variables)
                    pending_config = (
                        getattr(server, "pending_config", None) if server.HasField("pending_config") else None
                    )
                    pending_color = _get_color_for_status(server.status)
                    row_data.append(
                        _process_pending_field(current_env_vars, pending_config, "environment_variables", pending_color)
                    )
                elif heading == "Description":
                    description, _ = _extract_metadata(server)
                    row_data.append(description)
                elif heading == "Tags":
                    _, tags = _extract_metadata(server)
                    row_data.append(_get_pairs_str(tags))
                elif heading == "Updated At":
                    row_data.append(timestamp_to_string(server.updated_at))
                else:
                    row_data.append("")

            rows.append(tuple(row_data))

        return headings, rows


def print_feature_server_caches(caches: List[FeatureServerCache], single: bool = False):
    """Print Feature Server Caches in single or multi-item format."""
    FEATURE_SERVER_CACHE_CONFIG = {
        "has_scaling": False,
        "has_node_type": False,
        "has_cache_fields": True,
        "has_metadata": True,
        "multi_headings": [
            "ID",
            "Workspace",
            "Name",
            "Status",
            "Num Shards",
            "Num Replicas",
            "Preferred Maintenance Window",
            "Pending Config",
            "Description",
            "Tags",
            "Updated At",
        ],
    }

    if single and len(caches) == 1:
        headings, rows = _extract_server_fields(caches[0], single=True, field_config=FEATURE_SERVER_CACHE_CONFIG)
    else:
        headings, rows = _extract_server_fields(caches, single=False, field_config=FEATURE_SERVER_CACHE_CONFIG)

    display_table(headings, rows, title="Feature Server Caches", show_lines=True)


def print_feature_server_groups(fsgs: List[FeatureServerGroup], single: bool = False):
    """Print Feature Server Groups in single or multi-item format."""
    FEATURE_SERVER_GROUP_CONFIG = {
        "has_scaling": True,
        "has_node_type": True,
        "has_cache_id": True,
        "has_metadata": True,
        "multi_headings": [
            "ID",
            "Workspace",
            "Name",
            "Status",
            "Scaling",
            "Node Type",
            "Cache ID",
            "Pending Config",
            "Description",
            "Tags",
            "Updated At",
        ],
    }

    if single and len(fsgs) == 1:
        headings, rows = _extract_server_fields(fsgs[0], single=True, field_config=FEATURE_SERVER_GROUP_CONFIG)
    else:
        headings, rows = _extract_server_fields(fsgs, single=False, field_config=FEATURE_SERVER_GROUP_CONFIG)

    display_table(headings, rows, title="Feature Server Groups", show_lines=True)


def print_ingest_server_groups(isgs: List[IngestServerGroup], single: bool = False):
    """Print Ingest Server Groups in single or multi-item format."""
    INGEST_SERVER_GROUP_CONFIG = {
        "has_scaling": True,
        "has_node_type": True,
        "has_metadata": True,
        "multi_headings": [
            "ID",
            "Workspace",
            "Name",
            "Status",
            "Scaling",
            "Node Type",
            "Description",
            "Tags",
            "Updated At",
        ],
    }

    if single:
        title = f"Ingest Server Group: {isgs[0].name}"
    else:
        title = "Ingest Server Groups"

    if single and len(isgs) == 1:
        headings, rows = _extract_server_fields(isgs[0], single=True, field_config=INGEST_SERVER_GROUP_CONFIG)
    else:
        headings, rows = _extract_server_fields(isgs, single=False, field_config=INGEST_SERVER_GROUP_CONFIG)

    display_table(headings, rows, title=title, show_lines=True)


def print_transform_server_groups(tsgs: List[TransformServerGroup], single: bool = False):
    """Print Transform Server Groups in single or multi-item format."""
    TRANSFORM_SERVER_GROUP_CONFIG = {
        "has_scaling": True,
        "has_node_type": True,
        "has_environment": True,
        "has_metadata": True,
        "multi_headings": [
            "ID",
            "Workspace",
            "Name",
            "Status",
            "Scaling",
            "Node Type",
            "Environment",
            "Environment Variables",
            "Description",
            "Tags",
            "Updated At",
        ],
    }

    if single and len(tsgs) == 1:
        headings, rows = _extract_server_fields(tsgs[0], single=True, field_config=TRANSFORM_SERVER_GROUP_CONFIG)
    else:
        headings, rows = _extract_server_fields(tsgs, single=False, field_config=TRANSFORM_SERVER_GROUP_CONFIG)

    if single:
        title = f"Transform Server Group: {tsgs[0].name}"
    else:
        title = "Transform Server Groups"

    display_table(headings, rows, title=title, show_lines=True)


@feature_server_cache.command("create", requires_auth=True, cls=TectonCommand)
@click.option("--name", help="Name of the cache", required=True, type=str)
@click.option("--num-shards", help="Number of shards", required=True, type=int)
@click.option("--num-replicas-per-shard", help="Number of replicas per shard", required=True, type=int)
@click.option(
    "--preferred-maintenance-window",
    help="Preferred maintenance window (format: ddd:hh24:mi-ddd:hh24:mi)",
    required=False,
    type=str,
)
@click.option("--description", help="Description of the cache", required=False, type=str)
@click.option("--tags", help="Tags for the cache", required=False, type=str)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def create_feature_server_cache_cmd(
    name: str,
    num_shards: int,
    num_replicas_per_shard: int,
    preferred_maintenance_window: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    workspace: Optional[str] = None,
):
    """Create a new Feature Server Cache."""
    workspace = _get_validated_workspace(workspace)

    tags = _parse_pairs_str(tags, "tags")

    cache = create_feature_server_cache(
        workspace=workspace,
        name=name,
        num_shards=num_shards,
        num_replicas_per_shard=num_replicas_per_shard,
        preferred_maintenance_window=preferred_maintenance_window,
        description=description,
        tags=tags,
    )

    print_feature_server_caches([cache], single=True)


@feature_server_cache.command("get", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the cache", required=True, type=str)
@click_exception_wrapper
def get_feature_server_cache_cmd(id: str):
    """Get a Feature Server Cache by ID."""
    cache = get_feature_server_cache(id=id)

    print_feature_server_caches([cache], single=True)


@feature_server_cache.command("list", requires_auth=True, cls=TectonCommand)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def list_feature_server_caches_cmd(workspace: Optional[str] = None):
    """List all Feature Server Caches."""
    workspace = _get_validated_workspace(workspace)

    response = list_feature_server_caches(workspace=workspace)

    print_feature_server_caches(response.caches)


@feature_server_cache.command("update", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the cache", required=True, type=str)
@click.option("--num-shards", help="Number of shards", required=False, type=int)
@click.option("--num-replicas-per-shard", help="Number of replicas per shard", required=False, type=int)
@click.option("--preferred-maintenance-window", help="Preferred maintenance window", required=False, type=str)
@click.option("--description", help="Description of the cache", required=False, type=str)
@click.option("--tags", help="Tags for the cache", required=False, type=str)
@click_exception_wrapper
def update_feature_server_cache_cmd(
    id: str,
    num_shards: Optional[int] = None,
    num_replicas_per_shard: Optional[int] = None,
    preferred_maintenance_window: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
):
    """Update a Feature Server Cache."""
    cache = update_feature_server_cache(
        id=id,
        num_shards=num_shards,
        num_replicas_per_shard=num_replicas_per_shard,
        preferred_maintenance_window=preferred_maintenance_window,
        description=description,
        tags=_parse_pairs_str(tags, "tags"),
    )
    print_feature_server_caches([cache], single=True)


@feature_server_cache.command("delete", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the cache", required=True, type=str)
@click_exception_wrapper
def delete_feature_server_cache_cmd(id: str):
    """Delete a Feature Server Cache by ID."""
    delete_feature_server_cache(id=id)
    printer.safe_print(f"Deleted Feature Server Cache with ID {id}")


@click.command(
    "feature-server-group",
    cls=TectonGroup,
    command_category=TectonCommandCategory.INFRA,
    hidden=True,
)
def feature_server_group():
    """Provision and manage Feature Server Groups."""


@feature_server_group.command("create", requires_auth=True, cls=TectonCommand)
@click.option("--name", help="Name of the server group", required=True, type=str)
@click.option("--cache-id", help="ID of the Feature Server Cache to use", required=False, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option("--tags", help="Tags for the server group", required=False, type=str)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def create_feature_server_group_cmd(
    name: str,
    cache_id: Optional[str] = None,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    workspace: Optional[str] = None,
):
    """Create a new Feature Server Group."""
    workspace = _get_validated_workspace(workspace)

    server_group = create_feature_server_group(
        workspace=workspace,
        name=name,
        cache_id=cache_id,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags"),
    )

    print_feature_server_groups([server_group], single=True)


@feature_server_group.command("get", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def get_feature_server_group_cmd(id: str):
    """Get a Feature Server Group by ID."""
    server_group = get_feature_server_group(id=id)

    print_feature_server_groups([server_group], single=True)


@feature_server_group.command("list", requires_auth=True, cls=TectonCommand)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def list_feature_server_groups_cmd(workspace: Optional[str] = None):
    """List all Feature Server Groups."""
    workspace = _get_validated_workspace(workspace)

    response = list_feature_server_groups(workspace=workspace)

    print_feature_server_groups(response.feature_server_groups)


@feature_server_group.command("update", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option("--tags", help="Tags to add to the server group", required=False, type=str)
@click_exception_wrapper
def update_feature_server_group_cmd(
    id: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
):
    """Update a Feature Server Group."""
    server_group = update_feature_server_group(
        id=id,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags"),
    )
    print_feature_server_groups([server_group])


@feature_server_group.command("delete", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def delete_feature_server_group_cmd(id: str):
    """Delete a Feature Server Group by ID."""
    delete_feature_server_group(id=id)
    printer.safe_print(f"Deleted Feature Server Group with ID {id}")


@click.command(
    "ingest-server-group",
    cls=TectonGroup,
    command_category=TectonCommandCategory.INFRA,
)
def ingest_server_group():
    """Provision and manage Ingest Server Groups.

    This command can also be called using the alias 'isg'.
    """


def _validate_scaling_params(min_nodes: Optional[int], max_nodes: Optional[int], desired_nodes: Optional[int]):
    if (min_nodes is None and max_nodes is None) and desired_nodes is None:
        msg = "Please specify either `min-nodes` and `max-nodes` for autoscaling or `desired-nodes` for provisioned scaling."
        raise click.ClickException(msg)
    if (min_nodes is not None and max_nodes is None) or (min_nodes is None and max_nodes is not None):
        msg = "Both min-nodes and max-nodes must be specified together for autoscaling."
        raise click.ClickException(msg)
    if (min_nodes is not None or max_nodes is not None) and desired_nodes is not None:
        msg = (
            "Either specify min-nodes and max-nodes for autoscaling or desired-nodes for provisioned scaling, not both."
        )
        raise click.ClickException(msg)


@ingest_server_group.command("create", requires_auth=True, cls=TectonCommand)
@click.option("--name", help="Name of the server group", required=True, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option("--tags", help="Tags to add to the server group", required=False, type=str)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def create_ingest_server_group_cmd(
    name: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    workspace: Optional[str] = None,
):
    """Create a new Ingest Server Group."""
    workspace = _get_validated_workspace(workspace)

    _validate_scaling_params(min_nodes, max_nodes, desired_nodes)

    server_group = create_ingest_server_group(
        workspace=workspace,
        name=name,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags"),
    )

    print_ingest_server_groups([server_group], single=True)


@ingest_server_group.command("get", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def get_ingest_server_group_cmd(id: str):
    """Get an Ingest Server Group by ID."""
    server_group = get_ingest_server_group(id=id)

    print_ingest_server_groups([server_group], single=True)


@ingest_server_group.command("list", requires_auth=True, cls=TectonCommand)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def list_ingest_server_groups_cmd(workspace: Optional[str] = None):
    """List all Ingest Server Groups."""
    workspace = _get_validated_workspace(workspace)

    response = list_ingest_server_groups(workspace=workspace)
    print_ingest_server_groups(response.ingest_server_groups)


@ingest_server_group.command("update", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option("--tags", help="Tags to add to the server group", required=False, type=str)
@click_exception_wrapper
def update_ingest_server_group_cmd(
    id: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
):
    """Update an Ingest Server Group."""
    server_group = update_ingest_server_group(
        id=id,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags"),
    )

    print_ingest_server_groups([server_group], single=True)


@ingest_server_group.command("delete", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def delete_ingest_server_group_cmd(id: str):
    """Delete an Ingest Server Group by ID."""
    delete_ingest_server_group(id=id)
    printer.safe_print(f"Deleted Ingest Server Group with ID {id}")


@click.command(
    "transform-server-group",
    cls=TectonGroup,
    command_category=TectonCommandCategory.INFRA,
)
def transform_server_group():
    """Provision and manage Transform Server Groups."""


@transform_server_group.command("create", requires_auth=True, cls=TectonCommand)
@click.option("--name", help="Name of the server group", required=True, type=str)
@click.option("--environment-name", help="Name of the Python environment to use", required=True, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option(
    "--tags", help="Tags to add to the server group in the format TAG1=VALUE1,TAG2=VALUE2", required=False, type=str
)
@click.option("--env-vars", help="Environment variable in the format KEY1=VALUE1,KEY2=VALUE2", required=False, type=str)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def create_transform_server_group_cmd(
    name: str,
    environment_name: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    env_vars: Optional[str] = None,
    workspace: Optional[str] = None,
):
    """Create a new Transform Server Group."""
    workspace = _get_validated_workspace(workspace)

    _validate_scaling_params(min_nodes, max_nodes, desired_nodes)

    server_group = create_transform_server_group(
        workspace=workspace,
        name=name,
        environment=environment_name,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags"),
        environment_variables=_parse_pairs_str(env_vars, "env-vars"),
    )

    print_transform_server_groups([server_group], single=True)


@transform_server_group.command("get", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def get_transform_server_group_cmd(id: str):
    """Get a Transform Server Group by ID."""
    server_group = get_transform_server_group(id=id)

    print_transform_server_groups([server_group], single=True)


@transform_server_group.command("list", requires_auth=True, cls=TectonCommand)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def list_transform_server_groups_cmd(workspace: Optional[str] = None):
    """List all Transform Server Groups."""
    workspace = _get_validated_workspace(workspace)

    response = list_transform_server_groups(workspace=workspace)

    print_transform_server_groups(response.transform_server_groups)


@transform_server_group.command("update", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click.option("--environment-name", help="Name of the Python environment to use", required=False, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option(
    "--tags", help="Tags to add to the server group in the format TAG1=VALUE1,TAG2=VALUE2", required=False, type=str
)
@click.option("--env-vars", help="Environment variable in the format KEY1=VALUE1,KEY2=VALUE2", required=False, type=str)
@click_exception_wrapper
def update_transform_server_group_cmd(
    id: str,
    environment_name: Optional[str] = None,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    env_vars: Optional[str] = None,
):
    """Update a Transform Server Group."""
    server_group = update_transform_server_group(
        id=id,
        environment=environment_name,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags"),
        environment_variables=_parse_pairs_str(env_vars, "env-vars"),
    )
    print_transform_server_groups([server_group])


@transform_server_group.command("delete", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def delete_transform_server_group_cmd(id: str):
    """Delete a Transform Server Group by ID."""
    delete_transform_server_group(id=id)
    printer.safe_print(f"Deleted Transform Server Group with ID {id}")


def _display_realtime_logs(response: GetRealtimeLogsResponse):
    display_table(
        headings=["Timestamp", "Node", "Message"],
        display_rows=[(log.timestamp.ToJsonString(), log.node, log.message) for log in response.logs],
        center_align=False,
    )

    if response.warnings:
        printer.safe_print(f"{INFO_SIGN} WARNING: {response.warnings}")


@transform_server_group.command("logs", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the transform server group", required=True, type=str)
@click.option(
    "-s",
    "--start",
    help="Start timestamp filter, in ISO 8601 format with UTC zone (YYYY-MM-DDThh:mm:ss.SSSSSSZ). Microseconds optional. Defaults to the one day prior to the current time if both start and end time are not specified.",
    required=False,
    type=str,
)
@click.option(
    "-e",
    "--end",
    help="End timestamp filter, in ISO 8601 format with UTC zone (YYYY-MM-DDThh:mm:ss.SSSSSSZ). Microseconds optional. Defaults to the current time if both start and end time are not specified.",
    required=False,
    type=str,
)
@click.option("-t", "--tail", help="Tail number of logs to return (max/default 100)", required=False, type=int)
@click_exception_wrapper
def logs(id: str, start: Optional[str] = None, end: Optional[str] = None, tail: Optional[int] = None):
    server_group_logs = get_realtime_logs(id, start, end, tail)
    _display_realtime_logs(server_group_logs)


@click.command(name="isg", hidden=True, cls=TectonGroup)
def isg():
    """Provision and manage Ingest Server Groups."""


isg.add_command(create_ingest_server_group_cmd)
isg.add_command(get_ingest_server_group_cmd)
isg.add_command(list_ingest_server_groups_cmd)
isg.add_command(update_ingest_server_group_cmd)
isg.add_command(delete_ingest_server_group_cmd)


@click.command(name="tsg", hidden=True, cls=TectonGroup)
def tsg():
    """Provision and manage Transform Server Groups."""


tsg.add_command(create_transform_server_group_cmd)
tsg.add_command(get_transform_server_group_cmd)
tsg.add_command(list_transform_server_groups_cmd)
tsg.add_command(update_transform_server_group_cmd)
tsg.add_command(delete_transform_server_group_cmd)
tsg.add_command(logs)
