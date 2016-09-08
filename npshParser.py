#
# npshParser.py
# 
# CS3070 Shell Behavior labs
#
# Lab 7 complete version
#
# created: Winter '16
# updated: Summer '16
#

import sys
import subprocess     


''' npshParser is the file used to parse text into commands that can be invoked.
    -a single line of text commands are delimited by pipes and based on this they
     parsed into a list of individual command elements.
     
     a command element looks like: [command, [arg, *], infile, outfile]
     
    -input and output redirects are processed and assigned into the list command elements
    -after all command elements are parsed, pipes are post-processed and constructed
     between each command element pair, pipe names appropriately assigned to the input
     and output channels

     - stdin and stdout channels are represented by the value None in infile/outfile
       as per subprocess module documentation '''
    

###############################
#constants
redirects = '|<>'
CMD = 0
ARGS = 1
IN = 2
OUT = 3


###############################
#module private variables
__pipeProcessed = False
__firstInputRedirect = True
__outputRedirected = False

 
def parse(line):
    ''' Parse through the command line and split into separate tokenized commands
    Post-processes the tokenized commands to mechanically specify pipes between commands'''
    
    global __firstInputRedirect, __outputRedirected, __pipeProcessed
    parsedCommandList = []  #reset
    __pipeProcessed = False
    __firstInputRedirect = True
    __outputRedirected = False

    #None passed into the process call library indicates we have no redirection parsed
    outputStream = None
    inputStream = None
    
    commandsToParse = line.split('|')
    i = 1
    nbrCmd = len(commandsToParse)
    for eachCommand in commandsToParse:

        command, remainder = __doState1or7__(eachCommand)

        args, remainder = __doState2or8__(remainder)

        inputStream, remainder = __doState3and4__(remainder)

        outputStream = __doState5and6__(remainder)

        if outputStream != None and i < nbrCmd:
            raise RuntimeError("Pipes cannot follow an output redirect.")

        i += 1
        __firstInputRedirect = False


        #TODO  implement logic to drive the rest of the state evaluation,
        #calling the below functions as required
        
            ###  note the constants and module private variables above. ###          

            #use this error statement in the appropriate place
            #   raise RuntimeError('Pipes cannot follow an output redirect.')


            #you will finish having provided values for the variables: command, args, inputStream, outputStream
            #  and the provided code picks up from there
        
        parsedCommand = [command, args, inputStream, outputStream]
        parsedCommandList.append(parsedCommand)
        __pipeProcessed = True  # next command parsed this line will be after a pipe, by definition

    #EOL is reached when there are no more commands left in commandsToParse
    parsedCommandList = __resolvePipes__(parsedCommandList)
    
    return parsedCommandList



##########################################
#private methods


def __doState1or7__(components):
    ''' state 1/7 do the same thing and pull the command no matter what,
        we return the command and a list with the remainder of the unparsed text'''
    components = components.replace("<", " < ")
    components = components.replace(">", " > ")
    components = " ".join(components.split())
    components = components.split(' ')

    if components == []:
        raise RuntimeError("No command to execute")
    elif components[0] == '-' or components[0] == '/' or components[0] == '<' or components[0] == '>':
        raise RuntimeError("Command missing")
    else:
        return (components[0], components[1:])

def __doState2or8__(components):
    ''' now we gather args (if any) no matter what.
        if there are no args we return an empty args list and a list with
        the remainder of the unparsed text'''
    i = 0
    args = []
    for eachArg in components:
        if eachArg == '>' or eachArg == '<': break
        args.append(eachArg)
        i += 1


    #TODO implement state logic, and provide what is needed to be returned in the tuple
        
    return (args, components[i:])

def __doState3and4__(components):
    ''' state 3 is always directly followed by state 4. if in state 3 we
        return the input file name (as the result of state 4) and a list with
        the remainder of the unparsed text'''
    global __firstInputRedirect, __pipeProcessed


    #TODO implement state logic, and provide what is needed to be returned in the tuple

    if components == []:
        return (None, [])
    elif components[0] == '<':
        if not __firstInputRedirect:
            raise RuntimeError('Cannot redirect input after piping')
        for el in components[1:]:
            if el == '<': raise RuntimeError('Cannot redirect input twice in one command line')
        if len(components[1:]) == 0:
            raise RuntimeError('Redirect input not specified')
        elif components[1] == '>':
            raise RuntimeError('Redirect input not specified')
        else:
            components = [components[1], components[2:]]
    else:
        components = [None, components]

    # input redirect in support of 3a
    return (components[0], components[1])

def __doState5and6__(components):
    ''' state 5 is always directly followed by state 6, and always processes a redirect output situation.
        we return the output file name as the result of state 6,
        or we blow up if there are any additional tokens left on the line because that is illegal '''
    
    #TODO implement state logic, and provide what is needed to be returned in the tuple

    if components == []:
        return None
    elif components[0] == '>':
        if len(components[1:]) == 0:
            raise RuntimeError('Redirect output not specified')
        elif components[1] == '>' or components[1] == '<':
            raise RuntimeError('Redirect output not specified')
        else:
            components = components[1:]
    else:
        raise RuntimeError('Redirect output was expected, found different command.')

    if len(components[1:]) > 0:
        raise RuntimeError('Additional commands or redirects cannot follow an output redirect.')

    # output redirect symbol
    return components[0]

def __parseRedirectSymbol__(components):
    ''' parse the redirect symbol (if any), this call will always follow the parsing of argument tokens,
        if there is a redirect symbol we strip it from the list of components and 
        return the redirect and a list with the remainder of the unparsed text.
        
        if there is no redirect symbol we should only see an EOL, otherwise something is wrong someplace,
           we don't care exactly what the problem is, just blow up and throw an error.
           
        if we found a redirect it should never be a pipe symbol, those should have been all consumed in
        the original line split operation '''
    
    #TODO implement state logic, and provide what is needed to be returned in the tuple

           #use this error statement in the appropriate place
           #   raise RuntimeError('expected a redirect and additional content on line, actually saw:', redirect, components)

           #use this error statement in the appropriate place
           #   raise RuntimeError('parsed a pipe symbol, this should never happen here')
    
    return (redirect, components[1:])



def __resolvePipes__(parsedCmdList):
    ''' Post-process the list of commands and provide pipe names to properly allow OUT and IN to be connected.

         -parsedCmdList is the fully parsed list of commands; returns that list modified, with the pipes appropriately annotated
           in IN and OUT fields of the command data structure.
           
        These are simplified pipes, they do not dynamically read/write from both ends. In cmd A | cmd B they
        take output from cmdA and after cmdA completes they are read by cmdB for input.'''

    #sub-task 3b
    #by definition every command pair has a pipe between them, so we don't need to think too hard
    #  no pipe IN for the first command and no pipe OUT for the last command

    ###TODO implement pipe creation logic,
    #    modify parsedCmdList by adding the correct pipe names in the correct places
    #    pipes have the naming pattern pipe$$$_xx  where xx are digits ordered from 01 to as high as necessary

        #ensure you physically create the pipe file(s) with this provided snippet
    if len(parsedCmdList) > 1:
        i = 0
        parsedCmdList[0][3] = "pipe$$$_" + str(i)
        for command in parsedCmdList[1:-1]:
            command[2] = "pipe$$$_" + str(i)
            i += 1
            command[3] = "pipe$$$_" + str(i)
            file = open(command[2], 'w')
            file.close()
        parsedCmdList[-1][2] = "pipe$$$_" + str(i)

    if(parsedCmdList[0][2] != None):
        file = open(parsedCmdList[0][2], 'w')
        file.close()

    if(parsedCmdList[-1][2] != None):
        file = open(parsedCmdList[-1][2], 'w')
        file.close()

    return parsedCmdList











