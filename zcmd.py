try:
    # Import necessary modules
    import os                  # Operating System functionality
    import importlib
    import subprocess           # Library for importing modules dynamically
    import requests            # Internet
    from tqdm import tqdm      # pxgs progress bar
    print("\n" * 100)
    ######  DEBUG  ######
    developerMode = False
    ######  DEBUG  ######

    # Initialize variables
    currentVersion = 68        # Current version of the application
    importedAddons = {}       # Dictionary to store information about imported addons
    commands = []             # Dictionary to store commands from addons
    helpdata = {"help": ["show help (arg with a command name to see details)"], "pxgs": ["pxgs --install (-i) <pkg name>"," [--version (-v) <version id>]"," --remove (-r) <pkg name>"], "reload": ["reload console (reinstall addons)"]}
    onelinehelpdata = [
        " ---------------------------",
        " - core --------------------",
        " ---------------------------",
        "                            ",
        " | help - shows this message",
        " | pxgs - package manager   ",
        " | reload - reload console  ",
        "                            ",
        " ---------------------------",
        " - addons ------------------",
        " ---------------------------",
        "                            ",
    ]
    def download_files(urls, paths):
        if len(urls) != len(paths):
            raise ValueError("The number of URLs and paths must match.")
    
        total_size = 0
        file_sizes = []
    
        # Calculate the total size of all files
        for url in urls:
            response = requests.head(url)
            size = int(response.headers.get('content-length', 0))
            file_sizes.append(size)
            total_size += size

        overall_progress = tqdm(total=total_size, unit='B', unit_scale=True, desc='Overall Progress')
    
        for url, path, file_size in zip(urls, paths, file_sizes):
            response = requests.get(url, stream=True)
            with open(path, 'wb') as file, tqdm(total=file_size, unit='B', unit_scale=True, desc=f'Downloading {path}') as progress:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    progress.update(len(data))
                    overall_progress.update(len(data))
            tqdm.write(f"Finished downloading {path}")
    
        overall_progress.close()
    
    def createappend(file, text):
        with open(file, "a") as f:
            f.write(text)
    
    ### Simple functions ###
    # Function to dynamically import a class from a Python file
    def get_class_from_file(file_path, class_name):
        # Create a module specification
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        # Create a module based on the specification
        module = importlib.util.module_from_spec(spec)
        # Execute the module in the loader's namespace
        spec.loader.exec_module(module)
        try:
            # Return the specified class from the module
            return getattr(module, class_name)
        except:
            return None
    ###

    ### Main Function ###
    def main():
        ### Get Addons ###
        # Get the path to the 'addons' directory
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "addons")
        # Print a message indicating addon importing
        print("Importing addons...")
    
        # Create 'addons' directory if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)

        # Loop through files in 'addons' directory
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            # Check if file is a regular file and has the correct extension
            if os.path.isfile(filepath) and (filename.endswith('.zad') or filename.endswith(".zad.py")):
                # Initialize addon information
                fileValid = False        # Flag to indicate if the file is valid
                addonName = None         # Name of the addon
                addonId = None           # ID of the addon
                addonVersion = None      # Version of the addon
                addonMinVer = 0          # Minimum version required by the addon
                addonMaxVer = -1         # Maximum version compatible with the addon
                addonDesc = None         # Description of the addon
                addonAuthor = "Unknown"  # Author of the addon

                # Open addon file and read addon metadata
                with open(filepath, "r") as file:
                    for line in file:
                        text = line.strip()
                        # Check for addon metadata and update variables accordingly
                        if text.startswith("#::ADDONTYPE::#"):
                            fileValid = True
                        elif text.startswith("#:AddonName"):
                            addonName = text.split("=", 1)[1].strip()
                        elif text.startswith("#:AddonId"):
                            addonId = text.split("=", 1)[1].strip()
                        elif text.startswith("#:AddonVersion"):
                            addonVersion = int(text.split("=", 1)[1].strip())
                        elif text.startswith("#:AddonMinVer"):
                            addonMinVer = int(text.split("=", 1)[1].strip())
                        elif text.startswith("#:AddonMaxVer"):
                            addonMaxVer = int(text.split("=", 1)[1].strip())
                        elif text.startswith("#:AddonDesc"):
                            addonDesc = text.split("=", 1)[1].strip()
                        elif text.startswith("#:AddonAuthor"):
                            addonAuthor = text.split("=", 1)[1].strip()
                if developerMode:
                    if not fileValid:
                        print("File not valid! Name: " + filepath)
                        print("To validate it use #::ADDONFILE::# at the top of the file ")
                    print("Set up: ")
                    if addonName:
                        print("Addon Name set up! #:AddonName="+addonName)
                    else:
                        print("Addon Name required! Use atleast one line named #:AddonName= Your Addon Name")
                    if addonName:
                        print("Addon ID set up! #:AddonId="+addonId)
                    else:
                        print("Addon ID required! Use atleast one line named #:AddonId= Your Addon Id")
                    if addonVersion:
                        print("Addon Version set up! #:AddonVersion="+addonVersion)
                    else:
                        print("Addon Version required! Use atleast one line named #:AddonVersion= Your Addon Version (single number)")
                    if addonDesc:
                        print("Addon Desc set up! #:AddonDesc="+addonDesc)
                    else:
                        print("Addon Desc required! Use atleast one line named #:AddonDesc= Your Addon Description")
                    if addonAuthor:
                        print("Addon Author set up! #:AddonAuthor="+addonAuthor)
                    else:
                        print("Addon Author is optional, but its easier to recognize your addons! Use #:AddonAuthor=Your Name")
                # Checks if addon exists with same ID
                for i in importedAddons:
                    if importedAddons[i]["id"] == addonId:
                        asertxisting = importedAddons[i]["name"]
                        asertxistingid = importedAddons[i]["id"]
                        print(f"Coliding IDs. Can't import addon: {addonName}. INFO: EXISTENT ID CMP: {addonName} COLLIDES WITH {asertxisting}; {addonId}; {asertxistingid}")
                        fileValid = False
                # If file is valid and compatible with current version, add addon information to importedAddons dictionary
                if fileValid:
                    if addonMinVer <= currentVersion:
                        if addonMaxVer >= currentVersion:
                            if addonName != None and addonId != None and addonVersion != None and addonDesc != None and addonAuthor != None:
                                # Print a message indicating the addon being added
                                print(f"Correct setup on addon: {addonName}! Adding functionality")
                                # Add addon information to importedAddons dictionary
                                importedAddons[len(importedAddons)] = {
                                    "name": addonName, 
                                    "id": addonId, 
                                    "version": addonVersion, 
                                    "minVer": addonMinVer, 
                                    "maxVer": addonMaxVer, 
                                    "desc": addonDesc, 
                                    "author": addonAuthor
                                }
                                # Get class AddonV1 from the file
                                addonClass = get_class_from_file(filepath, "AddonV1")
                                if addonClass:
                                    ac = addonClass()
                                    if ac.Commands:
                                        for com in ac:
                                            if type(addonClass) == type(com):
                                                if com.request_data:
                                                    if com.request_data(addonClass, "help_line"):
                                                        onelinehelpdata.append(" | " + com.request_data(addonClass, "help_line")) 
                                                    if com.request_data(addonClass, "help_info"):
                                                        helpdata[com.request_data(addonClass, "aliases")[0]] = com.request_data(addonClass, "help_info")
                                                if com.execute:
                                                    commands.append({"aliases": com.request_data(addonClass, "aliases"), "execute": com.execute, "self": addonClass})
                                            
        control()
    def control():
        print("\n" * 100)
        print("zcmd version 1.0.3c")
        print("also known as: 69 (nice)")
        while True:
            com = input(" > ")
            if com == "" or com.isspace():
                print("Unknown command! Use 'help' to see available commands!")
                continue
            handler(com)



    def handler(com):
        parts = com.split(" ")
        command = parts[0]
        args = parts[1:]
        if command == "help":
            if args:
                if " ".join(args) in helpdata:
                    print("Info: ")
                    for i in helpdata[" ".join(args)]:
                        print(i)
                    print("Command Name: " + " ".join(args))
            else:
                for i in onelinehelpdata:
                    print(i)
                print()
        elif command == "pxgs":
            version = 'latest'
            name = None
            uninst = False
            for i in range(len(args)):
                if args[i] == "--install" or args[i] == "-i" and len(args) > i + 1:
                    name = args[i + 1]
                if args[i] == "--remove" or args[i] == "-r" and len(args) > i + 1:
                    uninst = True
                    name = args[i + 1]
                if args[i] == "--version" or args[i] == "-v" and len(args) > i + 1:
                    version = args[i + 1]
            if name:
                if uninst:
                    if version == 'latest':
                        uninstall_package(name, None)
                    else:
                        uninstall_package(name, version)
                else:
                    install_package(name, version)
            else:
                print("Please provide a package name!")
        elif command == "reload":
            # Initialize variables
            if True:
                subprocess.Popen("python "+os.path.abspath(__file__))
                exit()
        elif command == "run":
            file_path = " ".join(args)
            with open(file_path, "r") as f:
                for line in f:
                    text = line.strip()
                    handler(text)
        else:
            found = False
            for i in range(len(commands)):
                for j in range(len(commands[i]["aliases"])):
                    if commands[i]["aliases"][j] == command:
                        found = True
                        commands[i]["execute"](commands[i]["self"], args)
                        continue
            if not found:
                print("Unknown command! Use 'help' to see available commands!")
            
            
    def uninstall_package(package_name=None, version=None):
        if package_name:
            thsi = os.listdir(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__))), "addons"))
            for i in range(len(thsi)):
                if version:
                    if thsi[i].startswith(package_name + "@" + version + ".zad.py"):
                        os.remove(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__))), "addons"), thsi[i]))
                        print("Package removed!")
                        return "OK"
                else:
                    if thsi[i].startswith(package_name):
                        os.remove(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__))), "addons"), thsi[i]))
                        print("Package removed!")
                        return "OK"
            print("Could not find package!")
            
            
    def install_package(package_name=None, ver="latest"):
        # Read the host list from file
        host_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "host_list.txt")
        with open(host_list_path, "r") as host_file:
            hosts = [line.strip() for line in host_file if line.strip()]
        matches = 0
        # Check each host for the package
        for host in hosts:
            try:
                if matches < 1:
                    res = requests.get(f"{host}:80/exists/{package_name}/{ver}").text
                    if res.startswith("TRUE"):
                        matches = matches + 1
                        if res.startswith("TRUE@"):
                            actualver = res.split("@", 1)[1]
                            download_files([f"{host}:80/download/{package_name}/{actualver}"], [os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "addons"), package_name+"@"+actualver+".zad.py" )])
                            print("Checking Dependencies...")
                            todownload = []
                            with open(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "addons"), package_name+"@"+actualver+".zad.py" ), "r") as f:
                                for line in f:
                                    acln = line.strip()
                                    if acln.startswith("#:AddonDependencies="):
                                        if acln.split("=",1)[1]:
                                            part1 = acln.split("=",1)[1]
                                            part2 = part1.split(",")
                                            for i in part2:
                                                depVersion = 'latest'
                                                depName = None
                                                if len(i.split("@",1)) == 2:
                                                    depVersion = i.split("@",1)[1]
                                                depName = i.split("@",1)[0] or None
                                                if depName:
                                                    todownload.append({'name': depName, 'version': depVersion})
                            print("Downloading dependencies...")
                            for i in todownload:
                                install_package(i["name"], i["version"])
                        else:
                            actualver = ver
                            download_files([f"{host}:80/download/{package_name}/{actualver}"], [os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "addons"), package_name+"@"+actualver+".zad.py" )])
                            print("Checking Dependencies...")
                            todownload = []
                            with open(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "addons"), package_name+"@"+actualver+".zad.py" ), "r") as f:
                                for line in f:
                                    acln = line.strip()
                                    if acln.startswith("#:AddonDependencies="):
                                        if acln.split("=",1)[1]:
                                            part1 = acln.split("=",1)[1]
                                            part2 = part1.split(",")
                                            for i in part2:
                                                depVersion = 'latest'
                                                depName = None
                                                if len(i.split("@",1)) == 2:
                                                    depVersion = i.split("@",1)[1]
                                                depName = i.split("@",1)[0] or None
                                                if depName:
                                                    todownload.append({'name': depName, 'version': depVersion})
                            print("Downloading dependencies...")
                            for i in todownload:
                                install_package(i["name"], i["version"])
                            print("Installed!")
            except requests.RequestException as e:
                print(f"Failed to contact host {host}: {e}")
        if matches == 0:
            print(f"Package {package_name} not found on any host.")
    
    # Call the main function to execute the script
    main()
except:
    print("An exception occured!")
    input("Press enter to exit... ")
    exit()