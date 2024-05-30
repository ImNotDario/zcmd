#::ADDONTYPE::#
#:AddonName=Default Commands
#:AddonId=main
#:AddonVersion=69
#:AddonMinVer=41
#:AddonMaxVer=69
#:AddonDesc=Default Commands for zcmd.
#:AddonAuthor=zegs32
import os, subprocess, requests, base64
def save_connection_details(name, ip, port,password):
    filename = "saved_connections.txt"
    if password:
        with open(filename, "a") as file:
            file.write(f"{name},{ip},{port},{password}\n")
    else:
        with open(filename, "a") as file:
            file.write(f"{name},{ip},{port}\n")

def get_saved_connection(name):
    filename = "saved_connections.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 4 and parts[0] == name:
                    return {"ip": parts[1], "port": int(parts[2]), "password": parts[3]}
                elif len(parts) == 3 and parts[0] == name:
                    return {"ip": parts[1], "port": int(parts[2]), "password": None}
    return None

class AddonV1:
    class Commands:
        class test:
            def request_data(self, dataName):
                if dataName == "aliases": 
                    return ["test"] # aliases, first alias is the main command name
                if dataName == "help_info":
                    return [
                        "Hello, world!"
                    ]
                if dataName == "help_line":
                    return "test - Hello, world!"
                return -1
            def execute(self, args):
                print("Hello, world!")
        class echo:
            def request_data(self, dataName):
                if dataName == "aliases": 
                    return ["echo"] # aliases, first alias is the main command name
                if dataName == "help_info":
                    return [
                        "echo <text>",
                        "USAGE: ",
                        "Echoes out <text>",
                        "<text> - text to echo out"
                    ]
                if dataName == "help_line":
                    return "echo <text> - prints out text"
                return -1
            def execute(self, args):
                print(" ".join(args))
        class python:
            def request_data(self, dataName):
                if dataName == "aliases": 
                    return ["python", "py", "py3", "python3"] # aliases, first alias is the main command name
                if dataName == "help_info":
                    return [
                        "python3 - subprocess python3 (must have python3)"
                    ]
                if dataName == "help_line":
                    return "python3 - subprocess python3"
                return -1
            def execute(self, args):
                subprocess.Popen("python3 " + " ".join(args))

        class connect:
            def request_data(self, dataName):
                if dataName == "aliases": 
                    return ["connect"] # aliases, first alias is the main command name
                if dataName == "help_info":
                    return [
                        "connect --ip <ip> [--port <port> --password <password> --save <savename> --to <savename>",
                        "ip - ip to connect (or url)",
                        "port - port to connect to",
                        "password - use a password or save to a save file",
                        "savename - savename for a save file",
                        "--to savename - load a save file and connect"
                    ]
                if dataName == "help_line":
                    return "connect --ip <ip> - use 'help connect' for more info"
                return -1
            def execute(self, args):
                        ip = None
                        port = 535  # Default port
                        password = None
                        save_connection = False
                        connect_to_saved = None
                        for i in range(len(args)):
                            if args[i] == "--ip" or args[i] == "-i" and i + 1 < len(args):
                                ip = args[i + 1]
                            if args[i] == "--password" or args[i] == "-pwd" and i + 1 < len(args):
                                password = args[i + 1]
                            if args[i] == "--port" or args[i] == "-p" and i + 1 < len(args):
                                port = int(args[i + 1])
                            if args[i] == "--save" or args[i] == "-s" and i + 1 < len(args):
                                save_connection = True
                                saved_name = args[i + 1]
                            if args[i] == "--to" or args[i] == "-l" and i + 1 < len(args):
                                connect_to_saved = args[i + 1]
                        if save_connection:
                            if ip:
                                if password:
                                    save_connection_details(saved_name, ip, port, password)
                                else:
                                    save_connection_details(saved_name, ip, port, None)
                                print("Saved as " + saved_name)
                            else:
                                print("No ip provided! Could not save!")
                        elif connect_to_saved:
                            connecti = get_saved_connection(connect_to_saved)
                            if connecti:
                                print("Connecting to "+connect_to_saved+"...")
                                if connecti['password']:
                                    connect_to_server(connecti['ip'], connecti['port'], connecti['password'])
                                else:
                                    connect_to_server(connecti['ip'], connecti['port'], None)
                            else:
                                print("No saved connection named "+ connect_to_saved)
                        elif ip:
                            if password:
                                connect_to_server(ip, port, password)
                            else:
                                connect_to_server(ip, port)

                        else:
                            print("Please provide an ip!")
        class msg:
            def request_data(self, dataName):
                if dataName == "aliases": 
                    return ["msg", "message"] # aliases, first alias is the main command name
                if dataName == "help_info":
                    return [
                        "msg --ip <ip> [--port <port>] --message <msg>",
                        "--message MUST ALWAYS BE THE LAST ARGUMENT, ",
                        "EVERYTHING AFTER IT WILL BE SENT IN THE MESSAGE!",
                    ]
                if dataName == "help_line":
                    return "msg --ip <ip> - use 'help msg' to get more info"
                return -1
            def execute(self, args):
                if len(args) == 0:
                    print("msg --ip <ip> [--port <port>] --message <msg>")
                    print("--message MUST ALWAYS BE THE LAST ARGUMENT, ")
                    print("EVERYTHING AFTER IT WILL BE SENT IN THE MESSAGE!")
                ip = None
                port = 535
                message = "No message specified"
                for i in range(len(args)):
                    if args[i] == "--ip" and i + 1 < len(args):
                        ip = args[i + 1]
                    if args[i] == "--port" and i + 1 < len(args):
                        port = int(args[i + 1])
                    if args[i] == "--message" and i + 1 < len(args):
                        message = " ".join(args[i+1:])
                if ip:
                    sendMessageTo(ip, port, message)
                else:
                    print("No IP specified. Please specify an IP.")
    ### REQUIRED DEPENDENCY! ###
    def __iter__(self):
        return iter(self.Commands.__dict__.values()) 
def connect_to_server(ip, port, password=None):
    mangx = f'http://{ip}:{port}'
    try:
        outxmh = requests.get(mangx + '/checkforauth/nul').text
        if outxmh == "TRUE":
            if password:
                passw = password
            else:
                passw = input("Password? ")
            outsx = requests.get(mangx + "/authenticate/" + base64.b64encode(passw.encode("utf-8")).decode('utf-8')).text
            if outsx == "INCORRECT":
                print("Incorrect password! ")
                raise "jkh"
            elif outsx == "SUCCESS":
                print("Use 'disconnect' to disconnect from the server!")
                while True:
                    prompt = requests.get(mangx + "/readprompt/nul").text
                    outxs = input(prompt)
                    if outxs == "disconnect":
                        print("Sending EXIT packet...")
                        requests.get(mangx + "/logoff/nul")
                        print("Disconnecting!")
                        break
                    else:
                        response = requests.get(mangx + "/run_command/" + base64.b64encode(outxs.encode('utf-8')).decode('utf-8'))
                        print(response.text)  
            else:
                print("Incorrect response from server!")
        elif outxmh == "FALSE":
            print("Use 'disconnect' to disconnect from the server!")
            while True:
                prompt = requests.get(mangx + "/readprompt/nul").text
                outxs = input(prompt)
                if outxs == "disconnect":
                    print("Disconnecting!")
                    break
                else:
                   response = requests.get(mangx + "/run_command/" + base64.b64encode(outxs.encode('utf-8')).decode('utf-8'))
                   print(response.text)
        else:
            print("Server does not exist!")
            raise "Servejhtgt exist"
    except requests.exceptions.RequestException as e:
        print("Error connecting to server:", e)
    except:
        print("Could not connect!")
        
def sendMessageTo(ip, port, message):
    try:
        print("Attempting to send message to " + ip)
        sendto = f"http://{ip}:{port}/message/"
        resp = requests.get(sendto + base64.b64encode(message.encode('utf-8')).decode('utf-8'))
        if resp.text == "SHOWN":
            print("Successfully sent message!")
        elif resp.text == "DISABLED":
            print("Target server disabled messages!")
        else:
            print("Server does not exist!")
            raise "nikod"
    except requests.exceptions.RequestException as e:
        print("Error connecting to server:", e)
    except:
        print("Could not connect!")
