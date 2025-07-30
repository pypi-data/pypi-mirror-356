"""
TwinFabric MCP Server

A simple MCP server for interacting with TwinFabric.
"""

import logging
import socket
import sys
import os
import json
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any, Optional
from fastmcp import FastMCP
import struct
# Configure logging with more detailed format
log_dir = os.getenv("LOG_DIR", "./logs")
log_file = os.path.join(log_dir, "TwinFabric_mcp.log")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)  # 如果目录不存在，则创建
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG level for more details
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        # logging.StreamHandler(sys.stdout) # Remove this handler to unexpected non-whitespace characters in JSON
    ]
)
logger = logging.getLogger("TwinFabricMCP")

# Configuration
UNREAL_HOST = "127.0.0.1"
UNREAL_PORT = 55557

class TwinFabricConnection:
    """Connection to an TwinFabric instance."""
    
    def __init__(self):
        """Initialize the connection."""
        self.socket = None
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to the TwinFabric instance."""
        try:
            # Close any existing socket
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            
            logger.info(f"Connecting to TwinFabric at {UNREAL_HOST}:{UNREAL_PORT}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # 5 second timeout
            
            # Set socket options for better stability
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            # Set larger buffer sizes
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
            
            self.socket.connect((UNREAL_HOST, UNREAL_PORT))
            self.connected = True
            logger.info("Connected to TwinFabric Engine")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to TwinFabric: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the TwinFabric Engine instance."""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.socket = None
        self.connected = False

    def receive_all(self,sock,length):
        data =bytearray()
        while len(data)<length:
            chunk=sock.recv(length-len(data))
            if not chunk:
                raise ConnectionError("Socket connection broken")
            data += chunk
        return data

    def receive_full_response(self, sock, buffer_size=65536) -> bytes:
        """Receive a complete response from TwinFabric, handling chunked data."""
        chunks = []
        sock.settimeout(450)  # 5 second timeout
        try:
            while True:
                chunk = sock.recv(buffer_size)

                if not chunk:
                    if not chunks:
                        raise Exception("Connection closed before receiving data")
                    break
                chunks.append(chunk)
                
                # Process the data received so far
                data = b''.join(chunks)
                decoded_data = data.decode('utf-8')
                logger.info(decoded_data)
                logger.info(f"Received response ({len(data)} bytes)")

                # Try to parse as JSON to check if complete
                try:
                    json.loads(decoded_data)
                    logger.info(f"Received complete response ({len(data)} bytes)")
                    return data
                except json.JSONDecodeError:
                    # Not complete JSON yet, continue reading
                    logger.debug(f"Received partial response, waiting for more data...")
                    continue
                except Exception as e:
                    logger.warning(f"Error processing response chunk: {str(e)}")
                    continue
        except socket.timeout:
            logger.warning("Socket timeout during receive")
            if chunks:
                # If we have some data already, try to use it
                data = b''.join(chunks)
                try:
                    json.loads(data.decode('utf-8'))
                    logger.info(f"Using partial response after timeout ({len(data)} bytes)")
                    return data
                except:
                    pass
            raise Exception("Timeout receiving TwinFabric response")
        except Exception as e:
            logger.error(f"Error during receive: {str(e)}")
            raise
    
    def send_command(self, command: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Send a command to TwinFabric Engine and get the response."""
        # Always reconnect for each command, since TwinFabric closes the connection after each command
        # This is different from Unity which keeps connections alive
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            self.connected = False
        
        if not self.connect():
            logger.error("Failed to connect to TwinFabric Engine for command")
            return None
        
        try:
            # Match Unity's command format exactly
            command_obj = {
                "type": command,  # Use "type" instead of "command"
                "params": params or {}  # Use Unity's params or {} pattern
            }
            
            # Send without newline, exactly like Unity
            command_json = json.dumps(command_obj)
            logger.info(f"Sending command: {command_json}")
            self.socket.sendall(command_json.encode('utf-8'))
            
            # Read response using improved handler
            response_data_size = self.receive_all(self.socket,4)
            logger.error(f"json_len: {response_data_size}")

            json_len = struct.unpack('!I', response_data_size)[0]
            logger.error(f"json_len: {json_len}")
            json_data = self.receive_all(self.socket, json_len)
            #esponse_data = self.receive_full_response(self.socket)
            response = json.loads(json_data.decode('utf-8'))
            
            # Log complete response for debugging
            logger.info(f"Complete response from TwinFabric: {response}")
            
            # Check for both error formats: {"status": "error", ...} and {"success": false, ...}
            if response.get("status") == "error":
                error_message = response.get("error") or response.get("message", "Unknown TwinFabric error")
                logger.error(f"TwinFabric error (status=error): {error_message}")
                # We want to preserve the original error structure but ensure error is accessible
                if "error" not in response:
                    response["error"] = error_message
            elif response.get("success") is False:
                # This format uses {"success": false, "error": "message"} or {"success": false, "message": "message"}
                error_message = response.get("error") or response.get("message", "Unknown TwinFabric error")
                logger.error(f"TwinFabric error (success=false): {error_message}")
                # Convert to the standard format expected by higher layers
                response = {
                    "status": "error",
                    "error": error_message
                }
            
            # Always close the connection after command is complete
            # since TwinFabric will close it on its side anyway
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            self.connected = False
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending command: {e}")
            # Always reset connection state on any error
            self.connected = False
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            return {
                "status": "error",
                "error": str(e)
            }

# Global connection state
_twin_fabric_connection: TwinFabricConnection = None

def get_twinfabric_connection() -> Optional[TwinFabricConnection]:
    """Get the connection to TwinFabric Engine."""
    global _twin_fabric_connection
    try:
        if _twin_fabric_connection is None:
            _twin_fabric_connection = TwinFabricConnection()
            if not _twin_fabric_connection.connect():
                logger.warning("Could not connect to TwinFabric Engine")
                _twin_fabric_connection = None
        else:
            # Verify connection is still valid with a ping-like test
            try:
                # Simple test by sending an empty buffer to check if socket is still connected
                _twin_fabric_connection.socket.sendall(b'\x00')
                logger.debug("Connection verified with ping test")
            except Exception as e:
                logger.warning(f"Existing connection failed: {e}")
                _twin_fabric_connection.disconnect()
                _twin_fabric_connection = None
                # Try to reconnect
                _twin_fabric_connection = TwinFabricConnection()
                if not _twin_fabric_connection.connect():
                    logger.warning("Could not reconnect to TwinFabric Engine")
                    _twin_fabric_connection = None
                else:
                    logger.info("Successfully reconnected to TwinFabric Engine")
        
        return _twin_fabric_connection
    except Exception as e:
        logger.error(f"Error getting TwinFabric connection: {e}")
        return None

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Handle server startup and shutdown."""
    global _twin_fabric_connection
    logger.info("UnrealMCP server starting up")
    try:
        _twin_fabric_connection = get_twinfabric_connection()
        if _twin_fabric_connection:
            logger.info("Connected to TwinFabric Engine on startup")
        else:
            logger.warning("Could not connect to TwinFabric Engine on startup")
    except Exception as e:
        logger.error(f"Error connecting to TwinFabric Engine on startup: {e}")
        _twin_fabric_connection = None
    
    try:
        yield {}
    finally:
        if _twin_fabric_connection:
            _twin_fabric_connection.disconnect()
            _twin_fabric_connection = None
        logger.info("TwinFabric MCP server shut down")

# Initialize server
mcp = FastMCP(
    "TwinFabricMCP")

sys.path.append(os.path.abspath(__file__))
# Import and register tools
from datav_twinfabric_mcp.tools.dtf_opus_tools import register_opus_tools
from datav_twinfabric_mcp.tools.dtf_project_tools import register_project_tools
from datav_twinfabric_mcp.tools.dtf_twin_tools import register_twin_system_tools
from datav_twinfabric_mcp.tools.agent_app_tools import register_agent_app_tools
from datav_twinfabric_mcp.tools.dtf_bailian_tools import register_bailian_tools
# Register tools 
register_bailian_tools(mcp)
register_opus_tools(mcp)
register_project_tools(mcp)
register_twin_system_tools(mcp)
register_agent_app_tools(mcp)
@mcp.prompt()
def info():
    """Information about available TwinFabric MCP tools and best practices."""
    return """
    # How to operate
    1. determine the type of user needs (such as "information query" or "operation execution")
    2. match the corresponding tool set according to the type
    3. generate specific parameters
    4. Prioritize calling related tools
    # TwinFabric MCP Server Tools and Best Practices
    ## Basic Concepts 
    1. Camera
    - Similar to the camera in 3D games, including basic camera parameters and playback duration
    2. Graphics_primitive
    - Use Graphics_primitive to visualize geographic data including point, line and surface data. The main types are POI, geo-fence, fly line, radar, etc.
    3. Custom_graphics_primitive
    - Use custom_graphics_primitive to visualize other data, such as 2D web pages, etc.
    4. Scene
    - The scene in TwinFabric contains the basic 3D scene + Camera + graphics_primitives + custom_graphics_primitive, which is a basic unit for demonstration switching.
    5. Storyline
    - The storyline consists of a series of scenes. Play a storyline means play these scenes in order.
    6. TwinPrefab
    - Twin Prefab is an abstract concept. It consists of multiple twin components. Each twin component has its own function. For example, the model component is used to display a model, etc.
    7. TwinActor
    - When TwinPrefab is instantiated to the scene, it forms a TwinActor
    ## TwinFabric Studio Tools
    - `play_scene(uuid)`
      Play a scene in TwinFabric Studio with its uuid
    - `gather_scene_info()`
      gather all scenes info in TwinFabric Studio
    - `play_camera(uuid)`
      switch to a camera in TwinFabric Studio with its uuid
    - `gather_scene_info()`
      gather all cameras info in TwinFabric Studio
    - `gather_all_graphics_primitive()`
      gather all graphics_primitive info in TwinFabric Studio  
    - `show_graphics_primitive(uuid)`
      set graphics_primitive visibility true in TwinFabric Studio with its uuid  
    - `hide_graphics_primitive(uuid)`
      set graphics_primitive visibility false in TwinFabric Studio with its uuid 
    - `gather_all_custom_graphics_primitive()`
      gather all custom_graphics_primitive info in TwinFabric Studio  
    - `show_custom_graphics_primitive(uuid)`
      set custom_graphics_primitive visibility true in TwinFabric Studio with its uuid  
    - `hide_custom_graphics_primitive(uuid)`
      set custom_graphics_primitive visibility false in TwinFabric Studio with its uuid 
    - `gather_storyline_info()`
      gather all storyline info in TwinFabric Studio  
    - `play_storyline(uuid)`
      start playing a storyline in TwinFabric Studio with its uuid  
    - `stop_storyline(uuid)`
      stop playing a storyline in TwinFabric Studio with its uuid 
    ## TwinFabric TwinSystem Tools
    - `gather_all_twin_prefab_info()`
      gather all twin_prefabs info in TwinFabric
    - `gather_all_twin_actor_info()`
      gather all twin_actors info in TwinFabric  
    ## Best Practices
    ### Scene
    - When the user says I want to watch a certain content, you should find the scene that best matches what the user said based on the collected TwinFabric scenes, and then call play_scene(uuid), where uuid is the uuid field of the scene
    
    ### Error Handling
    - Check command responses for success
    - Handle errors gracefully
    - Log important operations
    - Validate parameters
    - Clean up resources on errors
    """

def run():
    logger.info("Starting MCP server with stdio transport")
    mcp.run(transport='stdio') 
# Run the server
if __name__ == "__main__":
   run()
    #mcp.run(transport="streamable-http",host="30.232.92.111", port=9000, path="/mcp")