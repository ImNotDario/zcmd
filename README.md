# zcmd
simple command line

# Creating Addons
Creating addons for zcmd is easy!
## Creating the addon file
Name the file's extension .zad or .zad.py
The first line of the file should be `#::ADDONTYPE::#`
Then begins formatting
## Formatting your addon
### `#:AddonName`
`#:AddonName=Testing Addon`
Name your addon
### `#:AddonAuthor`
`#:AddonAuthor=zegs32`
Name yourself in the addon
### `#:AddonId`
`#:AddonId=test`
The id of your addon.
MUST BE DISTINCT FROM OTHER ADDONS
### `#:AddonDesc`
`#:AddonDesc=Testing addon made for testing... addons`
Describe your addon

## Version Control
Make your addon more organised! Version control is required!
### `#:AddonVersion`
`#:AddonVersion=12`
The addon's current version
### `#:AddonMinVer`
`#:AddonMinVer=0`
0 to support any older version of zcmd.
The minimum version of zcmd required.
### `#:AddonMaxVer`
`#:AddonMaxVer=79`
Set to `-1` to support any newer version of zcmd
The maximum version of zcmd required.

## Coding your addon
zcmd addons are based on python.
Begin with
```py
class AddonV1:
```
Then make commands!
Example:
```py
class AddonV1: # begin addon
    class Commands: # commands
        class test: # name the class the first alias of the command
            def request_data(self, dataName): # data required to add command
                if dataName == "aliases":     # aliases
                    return ["test", "aliastest"] # aliases, first alias is the main command name
                if dataName == "help_info":   # info when ran with  help <name of command>
                    return [                  # each string in the list = one line
                        "test <text>",
                        "Echo but its test",
                        "USAGE: ",
                        "<text> - text to echo out"
                    ]
                if dataName == "help_line":  # what shows up when help is ran without args
                    return "test <text> - echo but its test (one line test)"
                return -1
            def execute(self, args):         # when command is executed, args is the list of arguments
                printout = " ".join(args)
                print(printout)
                return
  ### REQUIRED DEPENDENCY! ###
  def __iter__(self):
    return iter(self.Commands.__dict__.values())  # this is required for the addon work
```
Make sure to include the last 3 lines!
## Publishing your addon
If your addon requires any other addon to work, add this line at the top
### `#:AddonDependencies`
`#:AddonDependencies=Essentials@1,Vault@3,Local`
Split by `,` and add @ next to the addon name to limit to version

**Now you can upload your addon to an addon host!**

# Modifying the source code
You may modify and publish your own version as long as it's open source.
