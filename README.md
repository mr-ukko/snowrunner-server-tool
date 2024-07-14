# SnowRunner Server Tool

This tool provides a web-based control panel for managing your SnowRunner game server. From current map aproves first 3 contracts of each provider. It is built using Python and can be accessed via the PC's IP address. 


## Features

- User-friendly web interface
- Autonomous Contract approval every ten minutes
- Change map from webpage

## Requirements

- Python 3.2 or higher
- Seperate account with a copy of SnowRunner
- Internet connection 

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/mr-ukko/snowrunner-server-tool.git
    cd snowrunner-server-tool
    ```

2. **Install the required Python packages:**

    ```sh
    pip install pyperclip vgamepad pywinauto pygetwindow
    ```

## Usage

1. **Start the SnowRunner co-op:**

	When starting Snowrunner co-op remeber change to Migichan for map change to work correctly  
2. **Start the python server**
    ```sh
    python atonomoysServer.py
    ```

3. **Access the control panel:**

    Open your web browser and go to `http://<server-ip>:8080`.

4. **Control the SnowRunner server:**

    Use the web interface to see invitation code and change the map

## Troubleshooting
 ### Common Issues
   - Server not starting
     - check if all required python packages are installed
     - Remember webpage usually takes more than 15 seconds to show up

   - Web interface not accessible
     - Verify the IP address and port number are correct
     - Ensure no other application is using the same port
     - Make sure that python has rights in firewall to create the site in your network
- Server is in another network
    - Use applications like [ngrok](https://ngrok.com/download)   
