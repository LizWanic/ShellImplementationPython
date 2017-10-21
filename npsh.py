# Joshua Fisher, Ryan Smith, Dan Salazar, Elizabeth Wanic
# npsh.py
#
# CS3070 Shell Behavior labs
#
# Lab 6/7 complete version
#
# created: Winter '16
# updated: Winter '17
# 

Lab6 = False  #set to False for Lab 7

import os
import pathlib

from npshParser import *

if not Lab6:
    from npshVirtualMachineManager import *                              
    import subprocess                                                    

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
        self.setPathName( os.getcwd() )
        
        if not Lab6:
            self.vmm = npshVirtualMachineManager(self)                    



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
                    #print(commandsThisLine)
                    if commandsThisLine[0][3] != None:
                        self.__createPipe__(commandsThisLine[0][3])

                    # 4) marshal and delegate commands for execution
                    for command in commandsThisLine:
                        if Lab6:
                            print ('this is where we will execute command:', command)     
                        else:
                            self.vmm.executeCommand(command)              

                except RuntimeError as re:
                    print('Error:', re)
                except IOError as ioe:
                    print('Error:', ioe)
                except subprocess.CalledProcessError as cpe:
                    print('Error:', cpe)
                
            # 5) Restore default state
            if not Lab6:
                self.__deletePipes__()     
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


    def __createPipe__(self, pipePathName):
        ''' this will physically create the output pipe for a command if one is required.

            These are simplified pipes, they do not dynamically read/write from both ends. In cmd A | cmd B they
            take output from cmdA and after cmdA completes they are read by cmdB for input.'''

        #pass
        #TODO Lab 7: physically create the files used as pipes,  make sure you NEVER overwrite
        #   a file that does not have the pipe name pattern

        if 'pipe$$$_' in pipePathName:
        	file = open(pipePathName, "w+")
 

    def __deletePipes__(self):
        ''' If command line required a pipe file(s) with the special naming pattern, clean it(them) up'''

        for file in os.listdir( self.currentPathName ):
            if 'pipe$$$_' in file:
                os.remove(file)
        	#file.close()
        #TODO Lab 7: get shells CD, not where an app may have left us in directory tree
 

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
    


