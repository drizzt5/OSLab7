#
# npshVM.py
# 
# CS3070 Shell Behavior labs
#
# Lab 7 start version
#
# created: Winter '16
# updated: Summer '16
# 


import os
import sys
import subprocess     
import pathlib        



class npshVM(object):
    ''' npshVM is the class used to emulate the virtual machine architecture used by shells
        when implementing processes.  We only use this VM class when we will be launching an
        executble program.  Built-in functions are not handled here.'''

##########################################
#Constructor
    def __init__(self, cmd, args, infile, outfile):
        ''' Constructor.
            cmd:     the name of the command to be executed
            args:    arguments passed in to the process to be used during execution
            infile:  None if using the OS's standard input, or the file descriptor for a redirect/pipe
            outfile: None if using the OS's standard output, or the file descriptor for a redirect/pipe'''                
        self.command = cmd
        self.args = args
        self.input = infile
        self.output = outfile
            

##########################################
#public methods

    def executeVM(self):
        '''Executes an outside executable process (command) described by this VM 
           Throws Exceptions to top level upon failure'''

        (infile, outfile) = npshVM.openRedirects(self.input, self.output)

        # this version of subprocess wants the command and arguments together as a string, so we make that string now
        callList = [self.command]
        callList.extend(self.args)
        cmd = ' '.join(callList)
        
        try:
            pass
            #call the external command as a subprocess,
            #   check option will throw an exception is the launch fails
            #   shell option gives us the correct flow thru's to OS display shell vis stdin/stdout when stdin/stdout are None
            #TODO use what you figured out from spDemo.py
        
        except:
            raise       #re-raises the exception so it can be handled in input loop
        
        finally:
            npshVM.closeRedirects()     #ALWAYS close and reset the redirects




############################################
# static methods

    @staticmethod
    def openRedirects(infile, outfile):
        '''If the input/output files have been changed from default, opens them
           does nothing if the input/output file is not used at all -- indicated by None'''

        if infile != None:
            #TODO file exists condition    https://docs.python.org/3/library/pathlib.html 
                try :
                    pass #infile = #TODO open it up
                except IOError:
                    raise IOError("Input file '" + str(infile) + " 'does not exist.")

        if outfile != None:
            try :
                outfile = open(outfile, 'w')#TODO opens file in overwrite mode
            except IOError:
                raise IOError("Output Error: File can't be opened due to permissions")        #re-raises the exception so it can be handled in input loop

        return (infile, outfile)



    @staticmethod
    def closeRedirects():
        ''' If the input/output channels have been changed from default std, close the redirect files/pipe file '''
        
        if sys.stdin != sys.__stdin__:  
            sys.stdin.close()
            sys.stdin = sys.__stdin__
            
        if sys.stdout != sys.__stdout__: 
            sys.stdout.close()
            sys.stdout = sys.__stdout__






