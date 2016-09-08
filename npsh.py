#
# npsh.py
#
# CS3070 Shell Behavior labs
#
# Lab 6/7 complete version
#
# created: Winter '16
# updated: Summer '16
# 


import os
from npshParser import *
from npshVirtualMachineManager import *                              #for Lab 7
import subprocess                                                    #for Lab 7

class npsh(object):
    ''' npsh is the main class used to hold the state of the shell
    and cause shell behaviors to be invoked.

    There are five main sub-tasks of the shell:
      1) Runs a continuous loop looking for command line input from the user
      2) Once input is received, it is parsed for individual commands.
      3) Virtual machines inputs are generated
         a) file redirection resolved
         b) piping resolved
      4) Commands are marshaled and delegated for execution:
 	a) input and output file redirections are verified valid
        b) some commands are built-in and execute in the shell's environment directly
        c) others are invoked thru individual virtual machines and each VM is executed in sequential order.
      5) Restore default state after execution is complete

      this program must be launched on the command line using 'python3 npsh.py'
       in order to properly have access to stdin and std out.  Launching from other launch points such as IDLE
       will cause VAST headaches with psuedo-input/psuedo-output files which do not work with subprocess calls
       -don't forget to CD into the correct source directory first
      '''

   
##########################################
#Constructor    
    def __init__(self, devMode):
        self.prevCommands = []  #all previously entered command are stored for reuse purposes (as lines)
        
        self.exitCalled = False
        self.devMode = devMode   

        self.promptSymbol = ":> "
        self.currentPathName = os.getcwd()

        self.setPathName( os.path.dirname(os.path.abspath(__file__)) )
        
        self.vmm = npshVirtualMachineManager(self)                    #for Lab 7




    def start(self):
        '''just like it says, main input loop is contained within'''
        
        print( " Welcome to nps shell. \n" )

        # 1) loop looking for command line input
        while (not self.exitCalled):
            
            line = input(self.prompt)
            
            if len(line) > 0:                     #gracefully discard with empty lines
                self.prevCommands.append(line)    # for dev tracking

                try:
                    # 2&3) parse for individual commands, each command is a list entry
                    commandsThisLine = parse(line)
                    if(commandsThisLine[0][0] == "exit"): self.setExit()

                    # 4) marshal and delegate commands for execution
                    for command in commandsThisLine:
                        #print ('gonna execute command:', command)     #for Lab 6
                        self.vmm.executeCommand(command)              #for Lab 7

                except RuntimeError as re:
                    print('Error:', re)
                except IOError as ioe:
                    print('Error:', ioe)
                except subprocess.CalledProcessError as cpe:
                    print('Error:', cpe)
                

            # 5) Restore default state
            self.vmm.cleanup()                                        #for Lab 7
            commandsThisLine = []
            line = ''
            

        
        #final output, for testing only
        if(self.devMode):
            print("\nClosing nps shell, prompt was:", self.prompt )
            print("\n======================================================================\n")
            print("All previous commands:\n")
            for command in self.prevCommands :
                print(command)
        
    

    def setExit(self):
        '''just like it says, tells the shell to not do any more lines of input'''
        self.exitCalled = True
        

    def setPathName(self, pathname):
        '''Updates the current directory for managing files, also causes the shell to update the prompt'''
        os.chdir(pathname)
        self.currentPathName = os.getcwd()
        shortPathName = self.currentPathName.split('/')[-1:][0]
        self.prompt = shortPathName + self.promptSymbol

        
    def getCD(self):
        '''returns the shells current directory'''
        return self.currentPathName



##############################################################################
##############################################################################
##############################################################################
## This is where we begin the actual execution

if __name__ == '__main__':

    #launch with a -d will set devMode True
    from optparse import OptionParser
    op = OptionParser()
    op.add_option("-d", action="store_true", dest="devMode")
    (options,args) = op.parse_args()

    shell = npsh(options.devMode)
    shell.start()
    


