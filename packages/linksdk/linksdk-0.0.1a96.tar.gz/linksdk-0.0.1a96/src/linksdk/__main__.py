# wiim/__main__.py
import asyncio
import logging
from typing import Dict, List, cast
from urllib.parse import urlparse
import socket # Import the socket module

from aiohttp import ClientSession, TCPConnector
from zeroconf import ServiceInfo
from zeroconf.asyncio import AsyncServiceBrowser, AsyncZeroconf, Zeroconf 

from .consts import SDK_LOGGER
from .controller import WiimController
from .discovery import verify_wiim_device
from .endpoint import WiimApiEndpoint
from .wiim_device import WiimDevice


class ZeroconfListener:
    """
    A listener class for discovering and collecting Zeroconf services on the network.
    """
    def __init__(self):
        self.discovered_devices: Dict[str, ServiceInfo] = {}

    def remove_service(self, zeroconf: 'Zeroconf', type: str, name: str) -> None:
        """Called when a service is removed."""
        SDK_LOGGER.info(f"Zeroconf service removed: {name}, type: {type}")
        self.discovered_devices.pop(name, None)

    def add_service(self, zeroconf: 'Zeroconf', type: str, name: str) -> None:
        """Called when a service is added or updated."""
        SDK_LOGGER.info(f"Zeroconf service added/updated: {name}, type: {type}")
        asyncio.create_task(self._async_add_service(zeroconf, type, name))
    
    async def _async_add_service(self, zeroconf: 'Zeroconf', type: str, name: str) -> None:
        """Asynchronously retrieves and stores service information."""
        info = await zeroconf.async_get_service_info(type, name)
        if info:
            self.discovered_devices[name] = info


async def _create_cli_session() -> ClientSession:
    """Creates an aiohttp client session for the CLI."""
    return ClientSession(connector=TCPConnector(ssl=False))

def get_local_ip_address() -> str:
    """Attempts to get the local machine's IP address."""
    try:
        # Create a UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to an external address; this doesn't send data, just triggers the OS to pick a local IP
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        # If unable to get via the above method, try to get hostname and resolve it
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            SDK_LOGGER.warning("Could not determine local IP address. Using '127.0.0.1' as fallback.")
            return "127.0.0.1"


async def main_cli():
    """
    Command-line interface for discovering and interacting with WiiM devices using Zeroconf.
    """
    # Set up logging
    SDK_LOGGER.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    SDK_LOGGER.info("Starting WiiM SDK CLI discovery using Zeroconf...")

    # Get the IP address of the host running Home Assistant
    ha_host_ip_address = get_local_ip_address()
    SDK_LOGGER.info(f"Determined Home Assistant Host IP for callbacks: {ha_host_ip_address}")

    # 1. Discover using Zeroconf
    aiozc = AsyncZeroconf()
    listener = ZeroconfListener()
    # Browse for service types common to Linkplay/WiiM devices
    browser = AsyncServiceBrowser(aiozc.zeroconf, "_linkplay._tcp.local.", listener)

    # Wait a few seconds for devices to be discovered
    discover_duration = 5
    SDK_LOGGER.info(f"Waiting {discover_duration} seconds for devices to be discovered...")
    await asyncio.sleep(discover_duration)
    
    # Stop Browse
    await browser.async_cancel()
    await aiozc.async_close()

    if not listener.discovered_devices:
        SDK_LOGGER.info("No WiiM devices found via Zeroconf on the network.")
        return

    # 2. Verify and initialize discovered devices
    async with await _create_cli_session() as session:
        controller = WiimController(session)
        verified_devices: List[WiimDevice] = []
        
        for name, info in listener.discovered_devices.items():
            if not info or not info.parsed_addresses():
                continue
            
            # This 'wiim_device_ip' is the IP of the discovered WiiM device, not the HA host.
            wiim_device_ip = info.parsed_addresses()[0] 
            SDK_LOGGER.info(f"Found potential device '{name}' at {wiim_device_ip}. Verifying...")

            # Zeroconf provides the service port, but we need to find the UPnP description file URL.
            # We will probe several common locations.
            # The port is often 80 or a high port (like 49152), and the path is usually /description.xml
            potential_locations = [
                f"http://{wiim_device_ip}:{info.port}/description.xml", # Try the service's own port
                f"http://{wiim_device_ip}/description.xml",           # Try the standard HTTP port
                f"http://{wiim_device_ip}:49152/description.xml"       # Try a common UPnP port
            ]
            
            upnp_device = None
            for location in potential_locations:
                # Use the verify_wiim_device function from discovery.py to check if this is a WiiM device
                upnp_device = await verify_wiim_device(location, session)
                if upnp_device:
                    SDK_LOGGER.info(f"Successfully verified WiiM device at {location}")
                    break
            
            if not upnp_device:
                SDK_LOGGER.warning(f"Could not verify device '{name}' at {wiim_device_ip}. It might not be a WiiM device or is not responding.")
                continue

            # Create an HTTP API endpoint, using the WiiM device's IP
            http_api = WiimApiEndpoint(protocol="https", port=443, endpoint=wiim_device_ip, session=session) #
            
            # Create and initialize the WiimDevice instance.
            # Set ha_host_ip to the local IP address we just obtained.
            wiim_dev = WiimDevice(upnp_device, session, http_api_endpoint=http_api, ha_host_ip=ha_host_ip_address, polling_interval=60) #
            await controller.add_device(wiim_dev) #
            # if await wiim_dev.async_init_services_and_subscribe(): #
            #     await controller.add_device(wiim_dev) #
            # else:
            #     SDK_LOGGER.warning(f"Failed to initialize WiimDevice after discovery: {upnp_device.friendly_name}")


        if not controller.devices:
            SDK_LOGGER.info("No verifiable WiiM devices could be initialized.")
            return

        # 3. Print device information (same logic as original __main__.py)
        SDK_LOGGER.info(f"Found and verified {len(controller.devices)} WiiM device(s):")
        for device_idx, device in enumerate(controller.devices):
            print(f"\n--- Device {device_idx + 1} ---")
            if not device.available:
                print(f"Name: {device.name} (UDN: {device.udn}) - Currently Unavailable")
                continue

            print(f"  Name: {device.name}") #
            print(f"  UDN: {device.udn}") #
            print(f"  Model: {device.model_name}") #
            print(f"  IP Address: {device.ip_address}") #
            print(f"  Firmware: {device.firmware_version or 'N/A'}") #
            print(f"  UPnP Device URL: {device.upnp_device.device_url if device.upnp_device else 'N/A'}") #
            # print(f"  Home Assistant Host IP (for callbacks): {device.ha_host_ip}") # Display the HA host IP

            print(f"  Status: {device.playing_status.value if device.playing_status else 'N/A'}") #
            print(f"  Volume: {device.volume}% {'(Muted)' if device.is_muted else ''}") #
            # print(f"  Source (Play Mode): {device.play_mode}") #

            if device.current_track_info:
                track_info = device.current_track_info
                print(f"  Current Track:") #
                print(f"    Title: {track_info.get('title', 'N/A')}") #
                print(f"    Artist: {track_info.get('artist', 'N/A')}") #
                print(f"    Album: {track_info.get('album', 'N/A')}") #

        # Clean up resources
        print("\nDisconnecting from devices...")
        for device in controller.devices:
            await device.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main_cli())
    except KeyboardInterrupt:
        SDK_LOGGER.info("Discovery process interrupted by user.")
    except Exception as e:
        SDK_LOGGER.error(f"An error occurred: {e}", exc_info=True)
