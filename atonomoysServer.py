import pyperclip as clipboard
import vgamepad as vg
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import json
import pygetwindow as gw
from pywinauto import Application

selected_key = 10
app_name = "SnowRunner"  #Application name
gamepad = vg.VX360Gamepad()
start_region = 0
my_string = "SnowRunner Invite Code"

# Search for the exact window title containing 'SnowRunner'
windows = gw.getAllTitles()
for window in windows:
    if 'SnowRunner' in window:
        app_name = window
        break

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        # Check if the requested path is the index.html
        if self.path == '/index.html':
            try:
                # Open and read the HTML file
                with open('index.html', 'r') as file:
                    html_content = file.read()
                # Replace the placeholder with the actual string
                html_content = html_content.replace('{{SnowRunner Invite Code}}', my_string)
                # Send the HTTP response
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                # Write the modified HTML content
                self.wfile.write(html_content.encode('utf-8'))
            except Exception as e:
                self.send_error(404, f"File not found: {self.path}{e}")
        else:
            # Serve other files as usual
            return SimpleHTTPRequestHandler.do_GET(self)
    # Mapchange operation from webpage
    def do_POST(self):
        global selected_key
        if self.path == '/keypress':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            key = data.get('key')
            if key:
                selected_key = key
                send_key_to_application(key, app_name)
                response = {'message': f'Pressed {key} key in {app_name}'}
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Bad Request'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
#Map change in Application
def send_key_to_application(keys, app_name):
    """
    Send a key press to a specific application window.
    :param key: The key to press
    :param app_name: The name of the application window
    """
    #map names Add if you add it to dropdawn in website
    key_map = {
        "michigan": 0,
        "alaska": 1,
        "taymyr": 2,
        "kola-peninsula": 3,
        "yukon": 4,
        "wisconsin": 5,
        "amur": 6,
        "don": 7,
        "maine": 8,
        "tennessee": 9,
        "glades": 10,
        "ontario": 11,
        "br-columbia": 12,
        "scandinavia": 13,
        "north-carolina": 14,
        "almaty-region": 15
    }
    try:
        # Find the window
        app_window = gw.getWindowsWithTitle(app_name)[0]
        app = Application().connect(handle=app_window._hWnd)
        app_window.activate()
        auto_press_event.clear()
        time.sleep(0.5)
        if isinstance(keys, int) != True:
            global start_region
            selected_map = key_map.get(keys)
            #check for is change of map needed
            if selected_map != start_region:
                #open map
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                gamepad.update()
                time.sleep(0.5)  # Keep the 'Y' button pressed for 0.5 second
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                gamepad.update()
                #go map in right from now selected map
                if selected_map > start_region:
                    for x in range(selected_map - start_region):
                        time.sleep(0.5)
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                        gamepad.update()
                        time.sleep(0.5)  # Keep the button 'RIGHT_SHOULDER' button  for 0.5 second
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                        gamepad.update()
                #go map in Left from now selected map
                elif selected_map < start_region:
                    for x in range(start_region - selected_map):
                        time.sleep(0.5)
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                        gamepad.update()
                        time.sleep(0.5)  # Keep the 'LEFT_SHOULDER' button pressed for 0.5 second
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                        gamepad.update()
                #Select map an goto it
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                gamepad.update()
                time.sleep(0.5)  # Keep the 'X' button pressed for 0.5 second
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                gamepad.update()
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.update()
                time.sleep(0.5)  # Keep the 'A' button pressed for 0.5 second
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.update()
                #remember what region is changed
                start_region = selected_map
                time.sleep(20)
                auto_press_event.set()
        print(f"Pressed {keys} key in {app_name}")
    except IndexError:
        print(f"No window with title '{app_name}' found.")
    except Exception as e:
        print(f"Error sending key to application: {e}")

def press_key_every_10_minutes(event, key, app_name, interval=600):
    """
    Press a specific key every specified interval in a specific application.
    :param event: controlls if this is active
    :param key: The key to press
    :param app_name: The name of the application window
    :param interval: Time interval in seconds (default is 600 seconds for 10 minutes)
    """
    try:
        while True:
            event.wait()
            if key:
                #goes to contracts in local map to accept
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
                gamepad.update()
                time.sleep(0.5)  # Keep the 'BACK' button pressed for 0.5 second
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
                gamepad.update()
                time.sleep(0.5)
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                gamepad.update()
                time.sleep(0.5)  # Keep the 'RIGHT_SHOULDER' button pressed for 0.5 second
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                gamepad.update()
                time.sleep(0.5)
                #do this for each contract giver
                for x in range(3):
                    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                    gamepad.update()
                    time.sleep(0.5)  # Keep the 'A' button pressed for 0.5 second
                    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                    gamepad.update()
                    time.sleep(0.5)
                    for x in range(3):#accept first three contracts
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                        gamepad.update()
                        time.sleep(0.5)  # Keep the 'A' button pressed for 0.5 second
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                        gamepad.update()
                        time.sleep(0.5)
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
                        gamepad.update()
                        time.sleep(0.5)  # Keep the 'DPAD_RIGHT' button pressed for 0.5 second
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
                        gamepad.update()
                        time.sleep(0.5)
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                        gamepad.update()
                        time.sleep(0.5)  # Keep the 'B' button pressed for 0.5 second
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                        gamepad.update()
                        time.sleep(0.5)
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
                        gamepad.update()
                        time.sleep(0.5)  # Keep the 'DPAD_DOWN' button pressed for 0.5 second
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
                        gamepad.update()
                        time.sleep(0.5)
                    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                    gamepad.update()
                    time.sleep(0.5)  # Keep the 'B' button pressed for 0.5 second
                    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                    gamepad.update()
                    time.sleep(0.5)
                    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
                    gamepad.update()
                    time.sleep(0.5)  # Keep the 'DPAD_DOWN' button pressed for 0.5 second
                    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
                    gamepad.update()
                    time.sleep(0.5)
                #back to garage
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                gamepad.update()
                time.sleep(0.5)  # Keep the 'B' button pressed for 0.5 second
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                gamepad.update()
                time.sleep(0.5)
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                gamepad.update()
                time.sleep(0.5)  # Keep the 'B' button pressed for 0.5 second
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                gamepad.update()
                time.sleep(0.5)
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                gamepad.update()
                time.sleep(0.5)  # Keep the 'B' button pressed for 0.5 second
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                gamepad.update()
                time.sleep(0.5)
            time.sleep(interval)  # Delay for the specified interval
    except KeyboardInterrupt:
        print("Program terminated.")

def run_server(port=8080):
    """
    Run a simple HTTP server on the specified port.

    :param port: The port number to run the server on (default is 8080)
    """
    handler = CustomHandler
    httpd = HTTPServer(('0.0.0.0', port), handler)
    print(f"Serving HTTP on all network interfaces at port {port}")
    httpd.serve_forever()

def server_invite_code(app_name):
    try:
        # Find the window
        app_window = gw.getWindowsWithTitle(app_name)[0]
        app = Application().connect(handle=app_window._hWnd)
        app_window.activate()
        time.sleep(0.5)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        gamepad.update()
        time.sleep(0.5)  # Keep the 'LEFT_SHOULDER' button pressed for 0.5 second
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        gamepad.update()
        time.sleep(0.5)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        gamepad.update()
        time.sleep(0.5)  # Keep the 'START' button pressed for 0.5 second
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        gamepad.update()
        time.sleep(0.5)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        gamepad.update()
        time.sleep(0.5)  # Keep the 'Y' button pressed for 0.5 second
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        gamepad.update()
        time.sleep(0.5)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        gamepad.update()
        time.sleep(0.5)  # Keep the 'X' button pressed for 0.5 second
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        gamepad.update()
        global my_string
        my_string = clipboard.paste()
        time.sleep(0.5)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        time.sleep(0.5)  # Keep the 'B' button pressed for 0.5 second
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        time.sleep(0.5)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        time.sleep(0.5)  # Keep the 'B' button pressed for 0.5 second
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        #back to garage
    except IndexError:
        print(f"No window with title '{app_name}' found.")
    except Exception as e:
        print(f"Error sending key to application: {e}")

if __name__ == "__main__":
    # Start the HTTP server in a separate thread
    server_invite_code(app_name)
    time.sleep(10)
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    auto_press_event = threading.Event()
    auto_press_event.set()

    # Start pressing the key every 10 minutes
    automatic_key = 10  # DO NOT Change this
    auto_press_thread = threading.Thread(target=press_key_every_10_minutes, args=(auto_press_event, automatic_key, app_name))
    auto_press_thread.daemon = True
    auto_press_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)  # Delay in the main thread loop
    except KeyboardInterrupt:
        print("Program terminated.")
