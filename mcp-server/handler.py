"""
handler.py — Lambda entry point for the NC AOC Criminal Forms MCP server.

Implements the MCP Streamable HTTP transport (2025-11-25 spec) over a single
/mcp endpoint.  Handles: initialize, ping, tools/list, tools/call,
notifications/* (no-response).  Returns SSE-formatted responses so Claude's
MCP client can parse the event stream.
"""

import base64
import json
import logging
import warnings

warnings.filterwarnings("ignore")
logging.getLogger("pypdf").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

from fill_logic import fill_nc_aoc_form_logic  # noqa: E402

_MCP_PROTOCOL_VERSION = "2025-11-25"
_SERVER_NAME = "nc-aoc-cr-forms"
_SERVER_VERSION = "1.0.0"

_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "https://claude.ai",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Mcp-Session-Id, Authorization",
    "Access-Control-Max-Age": "300",
}

_TOOL_SCHEMA = {
    "name": "fill_nc_aoc_form",
    "description": (
        "Fill a North Carolina AOC criminal court form PDF with the provided field values. "
        "Returns the completed PDF as a base64-encoded string and the canonical filename."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "form_ref": {
                "type": "string",
                "description": (
                    "Exact PDF filename (e.g. 'AOC-CR-100-Warrant-For-Arrest.pdf') "
                    "or form number (e.g. 'AOC-CR-100'). Use the exact filename for "
                    "multi-edition forms to avoid ambiguity errors."
                ),
            },
            "values": {
                "type": "object",
                "description": (
                    "Field name → value mapping. Checkbox fields: true/false or 'Yes'/'No'. "
                    "Text/dropdown fields: string. Use exact field names from fields_index.json."
                ),
                "additionalProperties": True,
            },
        },
        "required": ["form_ref", "values"],
    },
}


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------

def _sse(payload: dict) -> dict:
    """Wrap a JSON-RPC payload in SSE format for MCP Streamable HTTP."""
    body = f"event: message\ndata: {json.dumps(payload, separators=(',', ':'))}\n\n"
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            **_CORS_HEADERS,
        },
        "body": body,
    }


def _rpc_error(req_id, code: int, message: str) -> dict:
    return _sse({
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": code, "message": message},
    })


# ---------------------------------------------------------------------------
# JSON-RPC method handlers
# ---------------------------------------------------------------------------

def _handle_initialize(req_id, _params: dict) -> dict:
    return _sse({
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "protocolVersion": _MCP_PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": _SERVER_NAME, "version": _SERVER_VERSION},
        },
    })


def _handle_tools_list(req_id) -> dict:
    return _sse({
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {"tools": [_TOOL_SCHEMA]},
    })


def _handle_tools_call(req_id, params: dict) -> dict:
    tool_name = params.get("name", "")
    if tool_name != "fill_nc_aoc_form":
        return _rpc_error(req_id, -32601, f"Unknown tool: {tool_name}")

    args = params.get("arguments", {})
    form_ref = args.get("form_ref")
    values = args.get("values", {})

    if not form_ref:
        return _rpc_error(req_id, -32602, "Missing required argument: form_ref")

    # Reject obviously oversized or path-traversal inputs before hitting S3.
    if not isinstance(form_ref, str) or len(form_ref) > 300:
        return _rpc_error(req_id, -32602, "form_ref must be a string ≤ 300 characters")
    if ".." in form_ref or "/" in form_ref or "\\" in form_ref:
        return _rpc_error(req_id, -32602, "form_ref must not contain path separators")
    if not isinstance(values, dict) or len(values) > 500:
        return _rpc_error(req_id, -32602, "values must be an object with ≤ 500 keys")

    try:
        pdf_b64, filename = fill_nc_aoc_form_logic(form_ref, values)
    except (ValueError, KeyError) as exc:
        return _rpc_error(req_id, -32602, str(exc))
    except Exception as exc:
        # Log the real cause server-side (CloudWatch); do NOT echo internal details
        # (e.g. boto3 ClientError messages include bucket name and S3 key) to callers.
        logger.exception("Unhandled error in fill_nc_aoc_form: %s", type(exc).__name__)
        return _rpc_error(req_id, -32603, "Internal server error — please try again.")

    result_json = json.dumps({"filled_pdf_base64": pdf_b64, "filename": filename})
    return _sse({
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "content": [{"type": "text", "text": result_json}],
            "isError": False,
        },
    })


# ---------------------------------------------------------------------------
# Lambda handler
# ---------------------------------------------------------------------------

def lambda_handler(event: dict, context) -> dict:  # noqa: ANN001
    http = event.get("requestContext", {}).get("http", {})
    method = http.get("method", "GET")

    # CORS preflight
    if method == "OPTIONS":
        return {"statusCode": 200, "headers": _CORS_HEADERS, "body": ""}

    # GET /mcp — acknowledge SSE endpoint (no server-initiated events for stateless server)
    if method == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                **_CORS_HEADERS,
            },
            "body": "",
        }

    if method != "POST":
        return {"statusCode": 405, "headers": _CORS_HEADERS, "body": "Method Not Allowed"}

    # Decode body (Function URL may base64-encode binary bodies)
    raw_body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        raw_body = base64.b64decode(raw_body).decode("utf-8")

    try:
        request = json.loads(raw_body)
    except json.JSONDecodeError:
        return {"statusCode": 400, "headers": _CORS_HEADERS, "body": "Invalid JSON"}

    rpc_method = request.get("method", "")
    req_id = request.get("id")

    # Notifications carry no id and require no response per MCP spec.
    if req_id is None and rpc_method.startswith("notifications/"):
        return {"statusCode": 202, "headers": _CORS_HEADERS, "body": ""}

    if rpc_method == "initialize":
        return _handle_initialize(req_id, request.get("params", {}))
    if rpc_method == "ping":
        return _sse({"jsonrpc": "2.0", "id": req_id, "result": {}})
    if rpc_method == "tools/list":
        return _handle_tools_list(req_id)
    if rpc_method == "tools/call":
        return _handle_tools_call(req_id, request.get("params", {}))

    return _rpc_error(req_id, -32601, f"Method not found: {rpc_method}")
