#
# npshParser.py
# 
# CS3070 Shell Behavior labs
#
# Lab 6/7 complete version
#
# created: Winter '16
# updated: Winter '17
#

import sys
##import subprocess     


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
# methods
    
def parse(line):
    ''' Parse through the command line and split into separate tokenized commands
    Post-processes the tokenized commands to mechanically specify pipes between commands'''
    
    parsedCommandList = []

    #TODO do any setup that needs completing before parsing a single command line
   

    #None passed into the process call library indicates we have no redirection parsed
    outputStream = None
    inputStream = None
    
    commandsToParse = line.split('|')
    #print(commandsToParse)
    
    i = 0
    while i < len(commandsToParse):
    	commandsToParse[i] = commandsToParse[i].strip()
    	i += 1
    
    count = 0 
    for eachCommand in commandsToParse:
        args = []
        command = None 

        item = eachCommand.split(" ")
        command, remainder1 = __doState1or7__(item)
        
        if command in redirects:
        	raise RuntimeError('Redirect cannot directly follow a pipe.')
        
        args, remainder2 = __doState2or8__(remainder1)

        if len(remainder2) > 0:
        
            redirect, remainder3 = __parseRedirectSymbol__(remainder2)

            if redirect == '<':
                if count > 0:
                    raise RuntimeError('Cannot redirect input after a pipe.')
                else:
                    inputStream, remainder4 = __doState3and4__(remainder3)
                        
                    if '>' in remainder4[0]: 
                        redirect, remainder5 = __parseRedirectSymbol__(remainder4)   
                        outputStream = __doState5and6__(remainder5)

            elif redirect == '>':
                outputStream = __doState5and6__(remainder3)

         #TODO  implement logic to drive the rest of the state evaluation,
        #      calling the below functions as required
        # 
        #      note the constants and class private variables above. ###          
        #
        #      you will finish having provided values for the variables: command, args, inputStream, outputStream
        #      and the provided code picks up from there
        count += 1
        parsedCommand = [command, args, inputStream, outputStream]
        parsedCommandList.append(parsedCommand)
        pipeProcessed = True  # next command parsed this line will be after a pipe, by definition

    #EOL is reached when there are no more commands left in commandsToParse
    parsedCommandList = __resolvePipes__(parsedCommandList)
    
    return parsedCommandList



##########################################
#private methods


def __doState1or7__(components):
    ''' state 1/7 do the same thing and pull the command no matter what,
        we return the command and a list with the remainder of the unparsed text'''   
    return (components[0], components[1:])


def __doState2or8__(components):
    ''' now we gather args (if any) no matter what.

        returns a tuple comprised of (args, remainder of the unparsed text)
        if there are no arguments, args will be an empty list '''
    args = []

    i = 0
    while i < len(components):
        if components[i] not in redirects:
            args.append(components[i])
            i+=1
        else:
    	    break 

    components = components[i:]	

    #TODO implement state logic, and provide what is needed to be returned in the tuple
        
    return (args, components)



def __doState3and4__(components):
    ''' state 3 is always directly followed by state 4.
        if in state 3 we return the input file name (as the result of state 4) and a list with
        the remainder of the unparsed text'''
    
    # input redirect in support of 3a
    return (components[0], components[1:])


def __doState5and6__(components):
    ''' state 5 is always directly followed by state 6, and always processes a redirect output situation.
        we return the output file name as the result of state 6,
        or we blow up if there are any additional tokens left on the line because that is illegal '''
    
    #TODO implement state logic, and provide what is needed to be returned in the tuple
    
    if len(components) > 1:

           #use this error statement in the appropriate place
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

    redirect = components[0]

    if len(components) < 2:
        raise RuntimeError('expected a redirect and additional content on line, actually saw:', redirect, components)

    if redirect == '|': 
        raise RuntimeError('parsed a pipe symbol, this should never happen here')

    return (redirect, components[1:])



def __resolvePipes__(parsedCmdList):
    ''' Post-process the list of commands and provide pipe names to properly allow OUT and IN to be connected.

         -parsedCmdList is the fully parsed list of commands

         returns the command list with pipe names properly placed
           
        These are simplified pipes, they do not dynamically read/write from both ends. In cmd A | cmd B they
        take output from cmdA and after cmdA completes they are read by cmdB for input.'''

    #sub-task 3b
    #by definition every command pair has a pipe between them, so we don't need to think too hard
    #  no pipe IN for the first command and no pipe OUT for the last command

    #TODO implement pipe creation logic,
    #    modify parsedCmdList by adding the correct pipe names in the correct places
    #    pipes have the naming pattern pipe$$$_xx  where xx are digits ordered from 01 to as high as necessary

    

    if len(parsedCmdList) > 1:
    	for i in range(0, len(parsedCmdList)-1):
    		parsedCmdList[i][OUT] = 'pipe$$$_' + str(i) 
    		parsedCmdList[i+1][IN] = 'pipe$$$_' + str(i) 
            

    return parsedCmdList











