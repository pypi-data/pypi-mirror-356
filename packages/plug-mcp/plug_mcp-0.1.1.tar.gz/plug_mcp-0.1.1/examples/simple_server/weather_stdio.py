#!/usr/bin/env python3
"""
Weather MCP Server Example
A simple weather server that provides forecast and alerts tools.
"""

import logging
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# SSL verification setting - can be controlled via environment variable
import os
SSL_VERIFY = os.getenv("SSL_VERIFY", "true").lower() not in ("false", "0", "no")
SSL_VERIFY = False

logger.info(f"SSL verification enabled: {SSL_VERIFY}")


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    logger.info(f"Making request to: {url} (SSL verify: {SSL_VERIFY})")
    
    # Create client with SSL verification setting
    async with httpx.AsyncClient(verify=SSL_VERIFY) as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            logger.info(f"Response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            logger.info(f"Response data keys: {list(data.keys()) if data else 'None'}")
            return data
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
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
    logger.info(f"Getting alerts for state: {state}")
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
    logger.info(f"Getting forecast for coordinates: {latitude}, {longitude}")
    
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location. This might be due to the location being outside NWS coverage area or API issues."

    try:
        # Get the forecast URL from the points response
        properties = points_data.get("properties", {})
        forecast_url = properties.get("forecast")
        
        if not forecast_url:
            logger.error(f"No forecast URL found in points response. Available properties: {list(properties.keys())}")
            return "No forecast URL available for this location. The coordinates might be outside the NWS coverage area."
        
        logger.info(f"Fetching forecast from: {forecast_url}")
        forecast_data = await make_nws_request(forecast_url)

        if not forecast_data:
            return "Unable to fetch detailed forecast from NWS API."

        # Format the periods into a readable forecast
        forecast_properties = forecast_data.get("properties", {})
        periods = forecast_properties.get("periods", [])
        
        if not periods:
            logger.error(f"No forecast periods in response. Available forecast properties: {list(forecast_properties.keys())}")
            return "No forecast periods available in the response."
        
        forecasts = []
        for period in periods[:5]:  # Only show next 5 periods
            forecast = f"""
{period.get('name', 'Unknown Period')}:
Temperature: {period.get('temperature', 'Unknown')}°{period.get('temperatureUnit', 'F')}
Wind: {period.get('windSpeed', 'Unknown')} {period.get('windDirection', '')}
Forecast: {period.get('detailedForecast', 'No detailed forecast available')}
"""
            forecasts.append(forecast)

        return "\n---\n".join(forecasts)
        
    except Exception as e:
        logger.error(f"Error processing forecast data: {str(e)}")
        return f"Error processing forecast: {str(e)}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')