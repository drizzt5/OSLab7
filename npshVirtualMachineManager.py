#
# npshVirtualMachineManager.py
# 
# CS3070 Shell Behavior labs
#
# Lab 7 start version
#
# created: Winter '16
# updated: Summer '16
#

import os
import subprocess

from npshParser import *    #for CMD, ARGS, IN, OUT
from npshVM import *

class npshVirtualMachineManager(object):
    ''' npshVirtualMachineManager manages launching and redirecting I/O for
        the virtual machine architecture used by shells when implementing processes.  '''


##########################################
#Constructor

    def __init__(self, shell):

        self.shell = shell

        #function call map
        self.builtins = {
                'man' : self.__man__,
               'help' : self.__help__,
                 'cd' : self.__cd__,
               'echo' : self.__echo__,
               'exit' : self.__exit__,
                 'ls' : self.__ls__,
             'parent' : self.__parent__,
                'pid' : self.__pid__,
                'pwd' : self.__pwd__,
                 'rm' : self.__rm__
        }
        


##########################################
#public methods


    def executeCommand(self, command):
        '''exeute an individual shell command by either:
            invoking the built-in function    or
            constructing and telling the virtual machine to run'''

        theCommand = command[CMD]
        toCall = self.builtins.get(theCommand)  #gets a function name if a built-in,
                                                #  None (which resolves to False) if an executable

        # 4a) for built-in function commands 
        if toCall:
            toCall(command[ARGS], command[IN], command[OUT])
            
        # 4b) for executable commands
        else:
            callList = [command[CMD]]
            callList.extend(command[ARGS])  # extend adds each argument element to list indifvidually
            cmd = ' '.join(callList)
            subprocess.run(cmd, stdin=command[IN], stdout=command[OUT], shell=True, check=True)




    def cleanup(self):
        ''' handles managing external stuff to ready shell for the next line '''
        self.__deletePipes__()



##########################################
#private methods



    def __deletePipes__(self):
        ''' If command line required a pipe file(s) with the special naming pattern, clean it(them) up'''
        
        # get the shells current directory, not where an app may have left us in directory tree

        currentPath = str(pathlib.Path( self.shell.getCD() ))
        #TODO set up a loop to go thru the applicable directory        https://docs.python.org/3/library/pathlib.html
        files = os.listdir(currentPath.replace("\\","\\\\"))
        for file in files:
            if file.find('pipe$$$_') > -1 and os.path.isfile(os.path.join(currentPath, file)):
                os.remove(file)




    def __getDocstring__(self, dummy):
        return dummy.__doc__



    #######################################
    # Built-in commands                   #
    #######################################


    def __man__(self, command, unused, outFile):
        '''Usage: man [command] 
           Outputs the docstring for built-in commands to show basic usage
           When used without argument 'command', prints all available built-in commands.'''

        npshVM.openRedirects(None, outFile)
                
        if len(command) == 1:
            result = self.builtins.get(command[0])
            if (result):
                #called man <built-in function> so print our docstring
                print( self.__getDocstring__(result) )
            else:
                #call native man
                vm = npshVM('man', command, None, None)
                vm.executeVM()
            
        else:
            print("The following built-in functions are defined within this shell")
            commands = iter(self.builtins.keys())
            for each in commands:
                print(" ", each)

        npshVM.closeRedirects()

        
            

    def __help__(self, command, unused, outFile):
        '''Usage: help [command]
           Outputs the docstring for built-in commands to show basic usage
           When used without argument 'command', prints all available built-in commands. 
           Same as 'man' command'''
        
        npshVM.openRedirects(None, outFile)
        self.__man__(command)
        npshVM.closeRedirects()
        

    def __cd__(self, args, unused, unused2):
        '''Usage: cd [path]
           Change the current working directory to an absolute or relative path'''

        #TODO functionality  - remember the npsh class itself needs to know about this, look in there before
        #                      writing your code here



    def __echo__(self, args, unused, outFile):
        '''Usage: echo [args] 
           Repeat args to the output'''
        npshVM.openRedirects(None, outFile)

        #TODO functionality
            
        npshVM.closeRedirects()

        

    def __exit__(self, unused, unused2, unused3):
        '''Usage: exit [] 
           Exit the shell'''
        
        self.shell.setExit()        
        print("Exiting nps shell")


      
    def __ls__(self, unused, unused2, outFile):
        '''Usage: ls [] 
           Output the contents of the current directory in alphabetical order'''
        npshVM.openRedirects(None, outFile)
        
        #TODO functionality, see os module
        
        npshVM.closeRedirects()            


    def __parent__(self, unused, unused2, outFile):
        '''Usage: parent [] 
           Output the process ID of the nps shell parent'''
        npshVM.openRedirects(None, outFile)
         
        #TODO functionality, see os module
        
        npshVM.closeRedirects()        

            
    def __pid__(self, unused, unused2, outFile):
        '''Usage: pid [] 
           Output the nps shell process ID'''
        npshVM.openRedirects(None, outFile)
        
        #TODO functionality, see os module
        if outFile:
            outFile.write(os.getpid())
        else:
            print(os.getpid())
        
        npshVM.closeRedirects()


        
    def __pwd__(self, unused, unused2, outFile):
        '''Usage: pwd [] 
           Output the current working directory'''
        npshVM.openRedirects(None, outFile)
        
        #TODO functionality, see os module
        
        npshVM.closeRedirects()

        
        
    def __rm__(self, args, unused, unused2):
        '''Usage: rm [file] 
           Remove the designated file'''
        #TODO functionality, see os module
        




