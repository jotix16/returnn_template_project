#!/usr/bin/env python3
# checked mikel
import os

def sysexecVerbose(*args, **kwargs):
    """ Prints and then executes a shell comand given by *args """
    print("sysexec: %s" % (args,))
    import subprocess
    res = subprocess.call(args, shell=False, **kwargs)
    if res != 0:
        raise Exception("exit code %s" % res)
  
sysexecVerbose("git", "submodule", "init")
try:
	sysexecVerbose("git", "submodule", "update")
except Exception as e:
	print("%s. Try to continue though, maybe still works." % e)

sysexecVerbose("git", "submodule", "foreach", "git", "config", "credential.helper", "store")
sysexecVerbose("git", "submodule", "foreach", "git", "checkout", "-B", "master", "origin/master")

print("> Change into tools-multistep %s" % "tools-multisetup/")
os.chdir("tools-multisetup/")
sysexecVerbose("git", "submodule", "init")
sysexecVerbose("git", "submodule", "update")
