"""Snapshot management tools."""
from datetime import datetime

from fastmcp import Context, FastMCP
from loguru import logger

from mcp_server_vss.client import VssApiClient
from mcp_server_vss.exceptions import VssError
from mcp_server_vss.models.requests import VmInfoRequest, VmSnapshotRequest
from mcp_server_vss.models.vms import VmChangeRequestResult, VMInfo
from mcp_server_vss.tools.common import BaseVmTool


class ManageSnapshotVmTool(BaseVmTool):
    """Create a snapshot of a virtual machine."""

    def __init__(self, mcp: FastMCP, auth_token: str, api_endpoint: str):
        """Initialize class."""
        super().__init__(auth_token, api_endpoint)
        mcp.tool(name='create_vm_snapshot')(self.create_vm_snapshot)
        mcp.tool(name='get_vm_snapshots')(self.get_vm_snapshots)

    async def create_vm_snapshot(
        self, ctx: Context, request: VmSnapshotRequest
    ) -> str:
        """Create a snapshot of a virtual machine.

        Use this tool when you need to:
        - Create backup point before changes
        - Save VM state for rollback capability
        - Document VM configuration at a specific time
        - Prepare for maintenance or updates

        Snapshot options:
        - Memory snapshots: Include RAM state (slower but complete state capture)
        - Disk-only snapshots: Faster, suitable for powered-off VMs
        - Consolidate snapshots: Combine multiple snapshots into one after deletion

        Important:
        - Snapshots are not backups. Use for short-term rollback only.
        """
        try:
            async with VssApiClient(
                self.auth_token, self.api_endpoint
            ) as api_client:
                vm_data = await self.handle_vm_info(
                    api_client, request.vm_id_or_name, ctx
                )
                # Get the VM's snapshot data
                snapshots_data = await self.handle_vm_snapshots(
                    api_client, vm_data, ctx
                )
                snapshot_count = len(snapshots_data.snapshots)

                if request.from_date is None:
                    # set Timestamp in format YYYY-MM-DD HH:MM when
                    # to take the snapshot
                    request.from_date = datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )

                await ctx.info(
                    f"Found {snapshot_count} snapshots for VM {vm_data.name}"
                )
                change_request = await self.handle_vm_snapshot_creation(
                    api_client, vm_data, request
                )
                response = self._format_response(
                    vm_data, request, change_request, snapshot_count
                )
                return response
        except VssError as e:
            logger.error(
                f"VSS error in create_vm_snapshot: {str(e)}", exc_info=True
            )
            raise VssError(f"VSS API error: {str(e)}")
        except Exception as e:
            logger.error(
                f"Unexpected error in create_vm_snapshot: {e}", exc_info=True
            )
            raise VssError(f"Internal error: {str(e)}")

    async def get_vm_snapshots(
        self, ctx: Context, request: VmInfoRequest
    ) -> str:
        """Retrieve and analyze an ITS Private Cloud VM Snapshots by ID, Name, or UUID.

        Use this tool when you need to:
        - Get detailed information about a virtual machine snapshots

        Args:
            request: The request object containing the VM ID, UUID, or name.
            ctx: The Context object providing access to MCP capabilities.

        Return:
            str: A string representation of the VM information.
        """

        try:
            async with VssApiClient(
                self.auth_token, self.api_endpoint
            ) as api_client:
                vm_data = await self.handle_vm_info(
                    api_client, request.vm_id_or_uuid_or_name, ctx
                )
                vm_snapshots = await self.handle_vm_snapshots(
                    api_client, vm_data, ctx
                )
                # Convert to tool result format
                tool_results = vm_snapshots.to_tool_result()
                # Extract text content from tool results
                if tool_results and hasattr(tool_results[0], 'text'):
                    return tool_results[0].text
                return str(vm_snapshots)
        except VssError as e:
            logger.error(f"VSS error in get_vm_info: {str(e)}")
            raise Exception(f"VSS API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in get_vm_info: {e}")
            raise Exception(f"Internal error: {str(e)}")

    async def handle_vm_snapshot_creation(
        self,
        api_client: VssApiClient,
        vm_data: VMInfo,
        request: VmSnapshotRequest,
    ) -> VmChangeRequestResult:
        """Create a new snapshot for a VM by ID or name."""
        # Create the snapshot
        rv = await api_client.post(
            f"v2/vm/{vm_data.moref}/snapshot",
            json_data=request.model_dump(),
            context="creating snapshot",
        )
        result = rv.get("data", {})
        return VmChangeRequestResult.model_validate(result)

    @staticmethod
    def _format_response(
        vm_data: VMInfo,
        request: VmSnapshotRequest,
        change_request: VmChangeRequestResult,
        snapshot_count: int,
    ) -> str:
        """Format response."""
        response = f"""VM Snapshot Creation Summary
        {'=' * 50}

        VM Details:
        - Name: {vm_data.name}
        - ID: {vm_data.moref}
        - Current State: {vm_data.power_state}

        Request Summary:
        {request.to_text()}

        Operation Result:
        {change_request.to_text()}

        Current Snapshot Count: {snapshot_count + 1}
        """
        # Add warnings and recommendations
        if snapshot_count >= 2:
            response += "\n⚠️ WARNING: Multiple snapshots detected. Performance may be impacted."
            response += "\n💡Recommendation: Remove old snapshots when no longer needed."

        if request.include_memory and vm_data.power_state == "poweredOn":
            response += "\n⏱️ Memory snapshot may take longer to complete."

        if vm_data.power_state == "poweredOn":
            response += (
                "\n💡TIP: For faster snapshots, consider powering off VM first."
            )

        response += """

        NEXT STEPS:
        - Monitor snapshot completion status
        - Test rollback procedure if this is a critical change
        - Document snapshot purpose for future reference
        - Schedule snapshot cleanup after changes are validated

        IMPORTANT: Snapshots are not backups. They should be temporary and removed after validation.
        """
        return response
