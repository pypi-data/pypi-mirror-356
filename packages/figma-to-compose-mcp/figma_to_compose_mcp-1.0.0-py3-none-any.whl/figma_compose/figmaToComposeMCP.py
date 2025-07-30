from mcp.server.fastmcp import FastMCP, Context
import requests
import os
from importlib import resources

mcp = FastMCP("Figma→Compose with Tool Calls")

# Tool B: Fetches Figma node JSON
@mcp.tool()
def get_figma_node(file_key: str, node_id: str, token: str) -> dict:
    # Replace '-' with ':' in node_id
    node_id = node_id.replace('-', ':')
    url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}"
    res = requests.get(url, headers={"X-Figma-Token": token})
    res.raise_for_status()
    return res.json()["nodes"][node_id]

# Tool C: Fetches SVG for a node
@mcp.tool()
def get_figma_svg(file_key: str, node_id: str, token: str) -> str:
    # Replace '-' with ':' in node_id
    node_id = node_id.replace('-', ':')
    url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=svg"
    res = requests.get(url, headers={"X-Figma-Token": token})
    res.raise_for_status()
    img_url = res.json()["images"][node_id]
    return requests.get(img_url).text

# Tool A: Generates Compose prompt by calling Tools B and C
@mcp.tool()
async def generate_compose_code(
    file_key: str,
    node_id: str,
    ctx: Context
) -> str:
    """Generates jetpack compose code from figma link can have alias jc

    Args:
        file_key: figma node file key
        node_id: figma node id
        ctx: context
    """
    # Get token from environment
    token = os.environ.get("FIGMA_TOKEN")
    if not token:
        return "Error: FIGMA_TOKEN environment variable not set."

    # Call get_figma_node
    await ctx.info("Invoking get_figma_node…")
    node_json = await mcp.call_tool(
        "get_figma_node",
        {"file_key": file_key, "node_id": node_id, "token": token}
    )

    # Call get_figma_svg
    await ctx.info(f"Downloaded json: {node_json}")
    await ctx.info("Invoking get_figma_svg…")
    svg = await mcp.call_tool(
        "get_figma_svg",
        {"file_key": file_key, "node_id": node_id, "token": token}
    )

    # Read the prompt template from package resources
    prompt_template = resources.read_text("figma_compose", "prompt.txt")

    # Build prompt text
    prompt = (
        f"{prompt_template}\n\n"
        f"Figma JSON:\n{node_json}\n\n"
    )
    return prompt




# if __name__ == "__main__":
#     mcp.run()