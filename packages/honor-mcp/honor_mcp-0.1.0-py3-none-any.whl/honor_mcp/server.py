"""Honor MCP server implementation."""

from typing import Any
import json

import httpx
from mcp.server.fastmcp import FastMCP

from honor_mcp.config import get_config
from honor_mcp.utils import format_course_data

mcp = FastMCP("honor-mcp")

config = get_config()
URL_BASE = config["url_base"]
USER_AGENT = config["user_agent"]
HONOR_MCP_API_KEY = config.get("honor_mcp_api_key", "")


async def get_course_list() -> dict[str, Any] | None:
    """Make a request to the Honor Platform Server to get course."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json", "x-api-key": HONOR_MCP_API_KEY}
    async with httpx.AsyncClient() as client:
        url = f"{URL_BASE}/v1/mcp/courses"
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP error occurred: {e}",
                "status_code": e.response.status_code,
                "response_text": e.response.text,
                "request_url": str(e.request.url),
                "request_headers": dict(e.request.headers),
            }
        except httpx.RequestError as e:
            return {
                "error": f"Request error occurred: {e}",
                "request_url": str(e.request.url) if hasattr(e, 'request') else url,
            }
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}", "type": type(e).__name__}


async def post_new_course(
    course_title: str,
    course_description: str,
    start_date: str | None = None,
    end_date: str | None = None,
    course_code: str | None = None,
) -> dict[str, Any] | None:
    """Make a request to the Honor Platform Server to create a new course."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json", "x-api-key": HONOR_MCP_API_KEY}

    payload = {"courseName": course_title, "desc": course_description}

    if course_code:
        payload["courseIdentifier"] = course_code

    # Add dates if provided (format: YYYY-MM-DD for Java LocalDate)
    if start_date:
        payload["startDate"] = start_date
    if end_date:
        payload["endDate"] = end_date

    async with httpx.AsyncClient() as client:
        try:
            url = f"{URL_BASE}/v1/mcp/create-course"
            response = await client.post(
                url,
                headers=headers,
                timeout=30.0,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP error occurred: {e}",
                "status_code": e.response.status_code,
                "response_text": e.response.text,
                "request_url": str(e.request.url),
                "request_headers": dict(e.request.headers),
                "payload": payload
            }
        except httpx.RequestError as e:
            return {
                "error": f"Request error occurred: {e}",
                "request_url": str(e.request.url) if hasattr(e, 'request') else url,
                "payload": payload
            }
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}", "type": type(e).__name__, "payload": payload}


@mcp.tool()
async def get_courses() -> str:
    """Get a list of courses for a user of Honor Platform."""

    data = await get_course_list()
    if not data:
        return "Unable to fetch courses."

    if "error" in data:
        return f"Error fetching courses: {json.dumps(data, indent=2)}"

    try:
        # Use the utility function to format the course data into a structured dictionary
        formatted_data = format_course_data(data)
        return json.dumps(formatted_data, indent=2)
    except Exception as e:
        # If something goes wrong with formatting, return the raw data with an error message
        return f"Error formatting course data: {str(e)}\n\nRaw data: {json.dumps(data, indent=2)}"


@mcp.tool()
async def create_course(
    course_title: str,
    course_description: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    course_code: str | None = None,
) -> str:
    """Create a course in Honor Platform.

    Args:
        course_title: The title of the course to create.
        course_description: Optional description of the course. Limited to 1500 characters.
        start_date: Optional start date in YYYY-MM-DD format (e.g., "2024-01-15").
        end_date: Optional end date in YYYY-MM-DD format (e.g., "2024-05-15").
        course_code: Optional course code for the course.
    """
    data = await post_new_course(course_title, course_description, start_date, end_date, course_code)

    if not data:
        return "Unable to create course."

    if "error" in data:
        return f"Error creating course: {json.dumps(data, indent=2)}"

    # Just return the JSON data directly for the LLM to parse
    return json.dumps(data, indent=2)


def run_server():
    """Run the Honor MCP server."""
    mcp.run(transport="stdio")
