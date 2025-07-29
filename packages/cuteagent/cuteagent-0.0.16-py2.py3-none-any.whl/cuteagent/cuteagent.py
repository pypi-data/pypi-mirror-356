"""Main module."""
from gradio_client import Client
import time
import re
import os
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Union, Optional, Any
# https://working-tuna-massive.ngrok-free.app
# https://upright-mantis-intensely.ngrok-free.app/
# https://working-tuna-massive.ngrok-free.app/

# Load environment variables from .env file
load_dotenv()

OS_URL = "https://fintor-cute-test-1.ngrok.app"
HF_FINTOR_GUI_ENDPOINT = "https://jtpozbeohnafofam.us-east-1.aws.endpoints.huggingface.cloud/v1/"
HF_TOKEN = os.environ.get("HF_TOKEN")

HITL_URL = "https://d5x1qrpuf7.execute-api.us-west-1.amazonaws.com/prod/"
SHARED_STATE_URL = "https://c16bgaz0i2.execute-api.us-west-1.amazonaws.com/prod"

HITL_TOKEN = os.environ.get("HITL_TOKEN")

class WindowsAgent:
    def __init__(self, variable_name="friend" , os_url=OS_URL):
        """
        Initializes the WindowsAgent with a configurable variable name.

        Args:
            variable_name (str): The name to be used by hello_old_friend.
                                 Defaults to "friend".
        """
        self.config_variable_name = variable_name
        self.os_url = os_url

    def hello_world(self):
        """Prints a hello world message."""
        print("Hello World from WindowsAgent!")

    def hello_old_friend(self):
        """Prints a greeting to the configured variable name."""
        print(f"Hello, my old {self.config_variable_name}!")

    def add(self, a, b):
        """Adds two numbers and returns the result."""
        return a + b

    def act(self, input_data):
        try:
            client = Client(self.os_url) 
            result = client.predict(
                user_input=str(input_data),
                api_name="/process_input1"
            )
            print(result)
        except Exception as e:
            print(f"Error in act operation: {e}")
            return None

    def click_element(self, x: int, y: int):
        """Click at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        try:
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise ValueError("Coordinates must be numbers")
                
            input_data = {
                "action": "CLICK",
                "coordinate": [int(x), int(y)],
                "value": "value",
                "model_selected": "claude"
            }
            
            client = Client(self.os_url)
            result = client.predict(
                user_input=str(input_data),
                api_name="/process_input1"
            )
            print(result)
            return result
        except Exception as e:
            print(f"Error in click operation: {e}")
            return None

    def screenshot(self):
        try:
            client = Client(self.os_url) 
            result = client.predict(
                api_name="/get_screenshot_url"
            )
            print(result)
            return result
        except Exception as e:
            print(f"Error in act operation: {e}")
            return result
        

    def screenshot_cropped(self, arr_input):
        try:
            client = Client(self.os_url) 
            result = client.predict(
                array_input=arr_input,
                api_name="/get_cropped_screenshot"
            )
            print(result)
            return result
        except Exception as e:
            print(f"Error in act operation: {e}")
            return result

    def pause(self, seconds: float):
        """Pauses execution for the specified number of seconds.
        
        Args:
            seconds (float): Number of seconds to pause
        """
        try:
            if not isinstance(seconds, (int, float)) or seconds < 0:
                raise ValueError("Seconds must be a non-negative number")
                
            time.sleep(seconds)
            return True
        except Exception as e:
            print(f"Error in pause operation: {e}")
            return False

class VisionAgent:
    def __init__(self,screen_size=(1366, 768), model_selected="FINTOR_GUI", hf_fintor_gui_endpoint=HF_FINTOR_GUI_ENDPOINT, hf_token=HF_TOKEN):
        """
        Initializes the Vision class with a configurable variable name and OS URL.

        Args:
            variable_name (str): The name to use for configuration.
                                Defaults to "friend".
            os_url (str): The URL for OS operations.
                        Defaults to OS_URL.
        """
        self.hf_fintor_gui_endpoint = hf_fintor_gui_endpoint
        self.hf_token = hf_token
        self.model_selected = model_selected
        self.screen_size = screen_size
        
    def find_element(self, screenshot_url, element_name):
        try:
            if self.model_selected != "FINTOR_GUI":
                raise ValueError("We only support FINTOR_GUI for now!")
            
            print("Element name in find_element", element_name)
            
            print("Screenshot url in find_element", screenshot_url)
            client = OpenAI(
                base_url = self.hf_fintor_gui_endpoint,   
                api_key = self.hf_token
            )
            _NAV_SYSTEM_GROUNDING = """
            You are a GUI agent. You are given a task and your action history, with screenshots. You need to perform the next action to complete the task. 

            ## Output Format
            ```Action: ...```

            ## Action Space
            click(start_box='<|box_start|>(x1,y1)<|box_end|>')
            hotkey(key='')
            type(content='') #If you want to submit your input, use \"\" at the end of `content`.
            scroll(start_box='<|box_start|>(x1,y1)<|box_end|>', direction='down or up or right or left')
            wait() #Sleep for 5s and take a screenshot to check for any changes.
            finished()
            call_user() # Submit the task and call the user when the task is unsolvable, or when you need the user's help.

            ## Note
            - Do not generate any other text.
            """

            chat_completion = client.chat.completions.create(
                model="tgi",
                messages=[
                {"role": "system", "content": _NAV_SYSTEM_GROUNDING},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": screenshot_url}},
                        {
                            "type": "text",
                            "text": element_name
                        }
                    ]
                }
            ],
                top_p=None,
                temperature=0,
                max_tokens=150,
                stream=True,
                seed=None,
                stop=None,
                frequency_penalty=None,
                presence_penalty=None
            )
            word_buffer = ""
            full_text = []

            for message in chat_completion:
                chunk = message.choices[0].delta.content
                if chunk:
                    word_buffer += chunk
                    words = word_buffer.split()
                    full_text.extend(words[:-1])
                    word_buffer = words[-1] if words else ""

            if word_buffer:
                full_text.append(word_buffer)

            final_text = " ".join(full_text)
            print("final_text", final_text)
            pattern = r"\(\d+,\d+\)"

            matches = re.findall(pattern, final_text)
            print("matches", matches)

            if matches:
                if len(matches) == 1:
                    extracted_coordinates = matches[0]
                elif len(matches) == 2:
                    # Parse the two coordinate pairs
                    coord1 = matches[0].strip('()')
                    coord2 = matches[1].strip('()')
                    x1, y1 = map(int, coord1.split(','))
                    x2, y2 = map(int, coord2.split(','))
                    
                    # Average the coordinates
                    avg_x = (x1 + x2) // 2
                    avg_y = (y1 + y2) // 2
                    extracted_coordinates = f"({avg_x},{avg_y})"
                else:
                    # If more than 2 matches, use the first one
                    extracted_coordinates = matches[0]
                

                extracted_coordinates = self.convert_coordinates(extracted_coordinates)
                if extracted_coordinates:
                    return extracted_coordinates
            else:
                return "NOT FOUND"
        except Exception as e:
            print(f"Error in ui_tars_coordinates: {e}")
            return None

    def convert_coordinates(self, coordinates_str):
        """
        Convert coordinates based on screen size ratio (screen_size/1000).
        
        Args:
            coordinates_str (str): String in format "(x,y)"
            
        Returns:
            str: Converted coordinates in same format
        """
        try:
            # Strip parentheses and split by comma
            coords = coordinates_str.strip('()')
            x, y = map(int, coords.split(','))
            
            # Convert coordinates based on screen ratio
            x_ratio = self.screen_size[0] / 1000
            y_ratio = self.screen_size[1] / 1000
            
            new_x = int(x * x_ratio)
            new_y = int(y * y_ratio)
            
            return f"({new_x},{new_y})"
        except Exception as e:
            print(f"Error converting coordinates: {e}")
            return coordinates_str

class HumanAgent:
    def __init__(self, HITL_token=HITL_TOKEN, HITL_url=HITL_URL):
        """
        Initializes the HumanAgent with token and URL.

        Args:
            HITL_token (str): Authentication token
            HITL_url (str): API endpoint URL
        """
        self.HITL_token = HITL_token
        self.HITL_url = HITL_url

    def task(self,  image_urls, thread_id="1234567890", questions=None, task_type="NotSpecified", thread_state=None):
        """
        Creates a human task with images, instructions, and questions.

        Args:
            image_urls (list): List of image URLs to display
            instruction_markdown (str, optional): Markdown formatted instructions
            instruction_url (str, optional): URL to instructions
            questions (list, optional): List of question dictionaries with format:
                {
                    "Question": "Is this green?",
                    "Choices": ["Yes", "No", "Maybe"],  # Optional
                    "TypeIn": True  # Optional, defaults to True
                }

        Returns:
            Response from the human task API
        """
        try:
            if not image_urls:
                raise ValueError("At least one image URL is required")

            # Default empty list if questions parameter is None
            if questions is None:
                questions = []


            # Prepare task data
            task_data = {
                "type": "task",
                "image_urls": image_urls,
                "questions": questions,
                "thread_id": thread_id,
                "task_type": task_type,
                "thread_state": thread_state,
            }

            # Set up headers for the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.HITL_token}"
            }

            # Make the API call
            response = requests.post(
                self.HITL_url,
                headers=headers,
                data=json.dumps(task_data)
            )

            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response from the API
            print(f"Task sent to {self.HITL_url} successfully")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None
        except Exception as e:
            print(f"Error creating human task: {e}")
            return None

    def reporting(self, thread_id="1234567890", report_type="NotSpecified", thread_state=None):
            """
            Creates a human task with images, instructions, and questions.

            Args:
                thread_id (str): ID for the thread. Defaults to "1234567890"
                thread_state (dict, optional): Dictionary containing thread state information

            Returns:
                Response from the reporting API containing thread status and any updates
            """
            try:
                task_data = {
                    "type": "reporting",
                    "thread_id": thread_id,
                    "thread_state": thread_state,
                    "report_type": report_type
                }

                # Set up headers for the API request
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.HITL_token}"
                }

                # Make the API call
                response = requests.post(
                    self.HITL_url,
                    headers=headers,
                    data=json.dumps(task_data)
                )

                # Check if the request was successful
                response.raise_for_status()
                
                # Return the response from the API
                print(f"Reporting sent to {self.HITL_url} successfully")
                return response.json()
                
            except requests.exceptions.RequestException as e:
                print(f"API request error: {e}")
                return None
            except Exception as e:
                print(f"Error creating human reporting: {e}")
                return None

class StationAgent:
    """
    A class for managing shared state and server coordination between LangGraph workflows.
    
    This class integrates with a SharedState API to coordinate state and server management
    across different workflow instances in LangGraph.
    
    Server Status Constraint:
        The "server" variable can only have two values: "busy" or "idle"
        - "idle": Server is available for new tasks
        - "busy": Server is currently processing a task
        
    Reserved Variables:
        - "server": Server status (managed by server.load/unload methods only)
        - "serverThread": Current task type (managed by server.load/unload methods only)
    """
    
    # Reserved variable names that cannot be set by users
    RESERVED_VARIABLES = {"server", "serverThread"}
    
    # Valid server status values
    VALID_SERVER_STATUS = {"busy", "idle"}
    
    def __init__(self, station_thread_id: str, graph_thread_id: str, token: str, shared_state_url: str = SHARED_STATE_URL):
        """
        Initialize the StationAgent with thread IDs and authentication token.
        
        Args:
            station_thread_id (str): Identifier for the station/workflow instance
            graph_thread_id (str): LangGraph thread identifier
            token (str): Authentication token for API access
            shared_state_url (str): Base URL for the SharedState API. Defaults to SHARED_STATE_URL.
        """
        self.station_thread_id = station_thread_id
        self.graph_thread_id = graph_thread_id
        self.token = token
        self.base_url = shared_state_url
        
        # Set up HTTP session with authentication
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        })
        
        # Initialize nested classes
        self.state = self.State(self)
        self.server = self.Server(self)
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     data: Optional[Dict] = None, max_retries: int = 3) -> Optional[Dict]:
        """
        Make HTTP request with retry logic and error handling.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            data (dict, optional): Request body data
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            dict: Response JSON or None on failure
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 401:
                    raise ValueError("Authentication failed: Invalid token")
                
                if response.status_code == 404:
                    return None
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 1  # Exponential backoff
                    print(f"Request timeout, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    print("Request timeout after maximum retries")
                    return None
                    
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 1
                    print(f"Request error: {e}, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Request failed after maximum retries: {e}")
                    return None
                    
            except json.JSONDecodeError:
                print("Invalid JSON response received")
                return None
                
        return None
    
    def validate_server_status(self, status: str) -> bool:
        """
        Validate that a server status value is allowed.
        
        Args:
            status (str): Server status to validate
            
        Returns:
            bool: True if status is "busy" or "idle", False otherwise
        """
        return status in self.VALID_SERVER_STATUS
    
    def validate_connection(self) -> Dict:
        """
        Validate the connection to the SharedState API.
        
        Returns:
            dict: Connection status and information
        """
        try:
            # Try to list variables to test connection
            response = self._make_request("GET", f"/shared-state/list?stationThread={self.station_thread_id}")
            
            if response is not None:
                return {
                    "connected": True,
                    "api_url": self.base_url,
                    "station_thread": self.station_thread_id,
                    "variable_count": len(response.get("attributes", {}))
                }
            else:
                return {
                    "connected": False,
                    "error": "Failed to connect to API",
                    "api_url": self.base_url
                }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e),
                "api_url": self.base_url
            }
    
    class State:
        """Nested class for state management operations."""
        
        def __init__(self, agent: 'StationAgent'):
            self.agent = agent
        
        def get(self, variable_name: str) -> Union[Dict, str, None]:
            """
            Get single variable from SharedState API.
            
            Args:
                variable_name (str): Name of the variable to retrieve
                
            Returns:
                Union[Dict, str, None]: The attributeValue from response or None if not found
            """
            params = {
                "stationThread": self.agent.station_thread_id,
                "attributeName": variable_name
            }
            
            response = self.agent._make_request("GET", "/shared-state", params=params)
            
            if response and response.get("success"):
                return response.get("data", {}).get("attributeValue")
            
            return None
        
        def set(self, variable_name: str, variable_value: Any) -> bool:
            """
            Create/update single variable using PUT endpoint.
            
            Args:
                variable_name (str): Name of the variable to set
                variable_value (Any): Value to assign to the variable
                
            Returns:
                bool: True on success, False on failure
                
            Raises:
                ValueError: If variable_name is a reserved variable
            """
            if variable_name in self.agent.RESERVED_VARIABLES:
                raise ValueError(f"Cannot set reserved variable '{variable_name}'. Reserved variables: {self.agent.RESERVED_VARIABLES}")
            
            data = {
                "stationThread": self.agent.station_thread_id,
                "attributeName": variable_name,
                "attributeValue": variable_value
            }
            
            response = self.agent._make_request("PUT", "/shared-state", data=data)
            
            return response is not None and response.get("success", False)
        
        def pull(self) -> Dict:
            """
            Get ALL variables from SharedState API using list endpoint.
            
            Returns:
                dict: The attributes dict from response
            """
            params = {
                "stationThread": self.agent.station_thread_id
            }
            
            response = self.agent._make_request("GET", "/shared-state/list", params=params)
            
            if response and response.get("success"):
                return response.get("attributes", {})
            
            return {}
        
        def push(self, json_object: Dict) -> bool:
            """
            Bulk create/update variables using bulk-upsert endpoint.
            
            Args:
                json_object (Dict): Dictionary of variables to create/update
                
            Returns:
                bool: True on success, False on failure
                
            Raises:
                ValueError: If any variable name is reserved
            """
            # Check for reserved variables in the input
            reserved_found = set(json_object.keys()) & self.agent.RESERVED_VARIABLES
            if reserved_found:
                raise ValueError(f"Cannot set reserved variables: {reserved_found}. Reserved variables: {self.agent.RESERVED_VARIABLES}")
            
            # Automatically add server and serverThread if not present
            variables = json_object.copy()
            if "server" not in variables:
                variables["server"] = "idle"  # Always default to valid "idle" status
            if "serverThread" not in variables:
                variables["serverThread"] = "idle"
            
            data = {
                "stationThread": self.agent.station_thread_id,
                "variables": variables
            }
            
            response = self.agent._make_request("POST", "/shared-state/bulk-upsert", data=data)
            
            return response is not None and response.get("success", False)
        
        def sync(self, variable_name: str, langgraph_state: Any = None) -> Any:
            """
            Sync variable from SharedState API to LangGraph state.
            
            If langgraph_state is provided, this method will:
            1. Get the variable from SharedState API
            2. Create state.sharedState if it doesn't exist
            3. Set state.sharedState[variable_name] = retrieved_value
            4. Return the updated state object
            
            Args:
                variable_name (str): Name of the variable to sync
                langgraph_state (Any, optional): LangGraph state object to update
                
            Returns:
                Any: If langgraph_state provided, returns the updated state object.
                     If no langgraph_state provided, returns just the variable value.
            """
            # Get the variable from SharedState API
            variable_value = self.get(variable_name)
            
            # If LangGraph state is provided, update it and return the state
            if langgraph_state is not None:
                # Check if sharedState exists, if not create it
                if not hasattr(langgraph_state, 'sharedState'):
                    langgraph_state.sharedState = {}
                elif langgraph_state.sharedState is None:
                    langgraph_state.sharedState = {}
                
                # Set the variable in sharedState
                langgraph_state.sharedState[variable_name] = variable_value
                
                print(f"✅ Synced '{variable_name}' to LangGraph state.sharedState['{variable_name}'] = {variable_value}")
                
                # Return the updated state object
                return langgraph_state
            
            # Backward compatibility: return just the variable value if no state provided
            return variable_value
        
        def sync_all(self, langgraph_state: Any) -> Any:
            """
            Sync ALL variables from SharedState API to LangGraph state.
            
            This method will:
            1. Pull all variables from SharedState API
            2. Create state.sharedState if it doesn't exist
            3. Replace state.sharedState with all variables from API
            4. Return the updated state object
            
            Args:
                langgraph_state (Any): LangGraph state object to update
                
            Returns:
                Any: The updated LangGraph state object
            """
            # Get all variables from SharedState API
            all_variables = self.pull()
            
            # Update LangGraph state
            if not hasattr(langgraph_state, 'sharedState'):
                langgraph_state.sharedState = {}
            
            # Replace sharedState with all variables from API
            langgraph_state.sharedState = all_variables.copy()
            
            print(f"✅ Synced ALL variables to LangGraph state.sharedState: {len(all_variables)} variables")
            return langgraph_state
        
        def sync_multiple(self, variable_names: list, langgraph_state: Any = None) -> Any:
            """
            Sync multiple variables from SharedState API to LangGraph state.
            
            Args:
                variable_names (list): List of variable names to sync
                langgraph_state (Any, optional): LangGraph state object to update
                
            Returns:
                Any: If langgraph_state provided, returns the updated state object.
                     If no langgraph_state provided, returns dict with variable_name -> value mappings.
            """
            results = {}
            
            # Create sharedState if needed
            if langgraph_state is not None:
                if not hasattr(langgraph_state, 'sharedState'):
                    langgraph_state.sharedState = {}
                elif langgraph_state.sharedState is None:
                    langgraph_state.sharedState = {}
            
            # Sync each variable
            for variable_name in variable_names:
                variable_value = self.get(variable_name)
                results[variable_name] = variable_value
                
                # Update LangGraph state if provided
                if langgraph_state is not None:
                    langgraph_state.sharedState[variable_name] = variable_value
            
            if langgraph_state is not None:
                print(f"✅ Synced {len(variable_names)} variables to LangGraph state.sharedState")
                # Return the updated state object
                return langgraph_state
            
            # Backward compatibility: return just the results dict if no state provided
            return results
        
        def delete(self, variable_name: str) -> bool:
            """
            Delete a variable from SharedState API.
            
            Args:
                variable_name (str): Name of the variable to delete
                
            Returns:
                bool: True on success, False on failure
                
            Raises:
                ValueError: If variable_name is a reserved variable
            """
            if variable_name in self.agent.RESERVED_VARIABLES:
                raise ValueError(f"Cannot delete reserved variable '{variable_name}'. Reserved variables: {self.agent.RESERVED_VARIABLES}")
            
            params = {
                "stationThread": self.agent.station_thread_id,
                "attributeName": variable_name
            }
            
            response = self.agent._make_request("DELETE", "/shared-state", params=params)
            
            return response is not None and response.get("success", False)
        
        def exists(self, variable_name: str) -> bool:
            """
            Check if a variable exists in SharedState API.
            
            Args:
                variable_name (str): Name of the variable to check
                
            Returns:
                bool: True if variable exists, False otherwise
            """
            return self.get(variable_name) is not None
        
        def list_variables(self) -> list:
            """
            Get list of all variable names for the station thread.
            
            Returns:
                list: List of variable names
            """
            all_vars = self.pull()
            return list(all_vars.keys())
    
    class Server:
        """
        Nested class for server management operations.
        
        Note: Server management methods use direct API calls to manage reserved variables
        (server, serverThread) while maintaining absolute protection against user access.
        Server status can only be "busy" or "idle".
        """
        
        def __init__(self, agent: 'StationAgent'):
            self.agent = agent
        
        def _validate_server_status(self, status: str) -> bool:
            """
            Validate that server status is one of the allowed values.
            
            Args:
                status (str): Server status to validate
                
            Returns:
                bool: True if valid, False otherwise
            """
            return status in self.agent.VALID_SERVER_STATUS
        
        def _set_server_status(self, status: str, thread_value: str = "idle") -> Dict:
            """
            Internal method to set server status with validation.
            
            Args:
                status (str): Server status ("busy" or "idle")
                thread_value (str): ServerThread value
                
            Returns:
                dict: Result of the operation
            """
            if not self._validate_server_status(status):
                return {
                    "status": "error", 
                    "error": f"Invalid server status '{status}'. Must be one of: {self.agent.VALID_SERVER_STATUS}"
                }
            
            # Update server status using direct API calls
            server_data = {
                "stationThread": self.agent.station_thread_id,
                "attributeName": "server",
                "attributeValue": status
            }
            
            thread_data = {
                "stationThread": self.agent.station_thread_id,
                "attributeName": "serverThread",
                "attributeValue": thread_value
            }
            
            response1 = self.agent._make_request("PUT", "/shared-state", data=server_data)
            response2 = self.agent._make_request("PUT", "/shared-state", data=thread_data)
            
            success1 = response1 is not None and response1.get("success", False)
            success2 = response2 is not None and response2.get("success", False)
            
            return {"success": success1 and success2, "response1": response1, "response2": response2}
        
        def load(self, task_type: str) -> Dict:
            """
            Load server for a specific task type.
            
            Args:
                task_type (str): Type of task to load the server for
                
            Returns:
                dict: Status information about the load operation
            """
            # Check if server is busy
            current_server_status = self.agent.state.get("server")
            
            # Validate current server status if it exists
            if current_server_status is not None and not self._validate_server_status(current_server_status):
                return {
                    "status": "error", 
                    "error": f"Invalid current server status '{current_server_status}'. Must be 'busy' or 'idle'"
                }
            
            if current_server_status == "busy":
                return {"status": "busy", "error": "Server is busy"}
            
            # Set server to busy using validated method
            result = self._set_server_status("busy", task_type)
            
            if result["success"]:
                return {"status": "loaded", "serverThread": task_type}
            else:
                return {"status": "error", "error": "Failed to update server status"}
        
        def unload(self) -> Dict:
            """
            Unload the server and set it to idle.
            
            Returns:
                dict: Status information about the unload operation
            """
            # Check if server is already idle
            current_server_status = self.agent.state.get("server")
            
            # Validate current server status if it exists
            if current_server_status is not None and not self._validate_server_status(current_server_status):
                return {
                    "status": "error", 
                    "error": f"Invalid current server status '{current_server_status}'. Must be 'busy' or 'idle'"
                }
            
            if current_server_status == "idle":
                return {"status": "idle", "error": "Server is already idle"}
            
            # Set server to idle using validated method
            result = self._set_server_status("idle", "idle")
            
            if result["success"]:
                return {"status": "unloaded"}
            else:
                return {"status": "error", "error": "Failed to update server status"}
        
        def avail(self) -> Dict:
            """
            Get current server availability status.
            
            Returns:
                dict: Current server and serverThread values
                      Server status will be "busy" or "idle" only
            """
            server_status = self.agent.state.get("server")
            server_thread = self.agent.state.get("serverThread")
            
            # Validate server status if it exists
            if server_status is not None and not self._validate_server_status(server_status):
                return {
                    "server": "idle",  # Default to safe state
                    "serverThread": server_thread,
                    "warning": f"Invalid server status '{server_status}' detected, defaulting to 'idle'"
                }
            
            return {
                "server": server_status,
                "serverThread": server_thread
            }
    
    def uninterrupt(self, task_type: str) -> Dict:
        """
        Get task thread ID for resuming interrupted tasks.
        
        Args:
            task_type (str): Type of task to get thread ID for
            
        Returns:
            dict: Resume information or error message
        """
        thread_id_var = f"{task_type}_thread_id"
        thread_id_value = self.state.get(thread_id_var)
        
        if thread_id_value is not None:
            return {"resumeFrom": thread_id_value}
        else:
            return {"error": "Thread ID not found"}

