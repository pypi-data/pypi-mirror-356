"""Example SSE MCP Server for testing with the enhanced client."""

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn

# Initialize FastMCP server for Weather tools (SSE)
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    # The line below is modified to include verify=False
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # It's good practice to log the exception, e.g., print(f"Error during NWS request: {e}")
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.tool()
async def get_current_conditions(latitude: float, longitude: float) -> str:
    """Get current weather conditions for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the observation stations
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch location data."

    # Get the observation station URL
    stations_url = points_data["properties"]["observationStations"]
    stations_data = await make_nws_request(stations_url)

    if not stations_data or not stations_data["features"]:
        return "No observation stations found for this location."

    # Get the first station's latest observation
    station_id = stations_data["features"][0]["properties"]["stationIdentifier"]
    observations_url = f"{NWS_API_BASE}/stations/{station_id}/observations/latest"
    observation_data = await make_nws_request(observations_url)

    if not observation_data:
        return "Unable to fetch current conditions."

    props = observation_data["properties"]
    
    # Convert temperature from Celsius to Fahrenheit if needed
    temp_c = props.get("temperature", {}).get("value")
    temp_str = "Unknown"
    if temp_c is not None:
        temp_f = (temp_c * 9/5) + 32
        temp_str = f"{temp_f:.1f}°F ({temp_c:.1f}°C)"

    return f"""
Current Conditions:
Temperature: {temp_str}
Humidity: {props.get('relativeHumidity', {}).get('value', 'Unknown')}%
Wind Speed: {props.get('windSpeed', {}).get('value', 'Unknown')} mph
Wind Direction: {props.get('windDirection', {}).get('value', 'Unknown')}°
Visibility: {props.get('visibility', {}).get('value', 'Unknown')} meters
Barometric Pressure: {props.get('barometricPressure', {}).get('value', 'Unknown')} Pa
Description: {props.get('textDescription', 'No description available')}
"""


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can serve the provided mcp server with SSE."""
    sse = SseServerTransport("/messages")

    async def handle_sse(request: Request) -> Response:
        """Handle SSE connection and return proper response."""
        try:
            async with sse.connect_sse(
                    request.scope,
                    request.receive,
                    request._send,  # noqa: SLF001
            ) as (read_stream, write_stream):
                await mcp_server.run(
                    read_stream,
                    write_stream,
                    mcp_server.create_initialization_options(),
                )
            # Return a proper response after handling the SSE connection
            return Response("SSE Connection closed", status_code=200)
        except Exception as e:
            print(f"SSE Handler Error: {e}")
            return Response(f"SSE Error: {str(e)}", status_code=500)

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages", app=sse.handle_post_message),
        ],
    )


if __name__ == "__main__":
    mcp_server = mcp._mcp_server  # noqa: WPS437

    import argparse
    
    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to listen on')
    args = parser.parse_args()

    print(f"Starting SSE MCP server on {args.host}:{args.port}")
    print(f"Connect to: http://{args.host}:{args.port}/sse")

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host=args.host, port=args.port)