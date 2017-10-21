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
            #TODO build and call the VM for execution
            vm = npshVM(command[CMD], command[ARGS], command[IN], command[OUT])
            vm.executeVM()



##########################################
#private methods


    def __getDocstring__(self, dummy):
        return dummy.__doc__


    def __doBuiltinRedirects__(self, inFile, outFile):
        (inRedir, outRedir) = npshVM.openRedirects(inFile, outFile)

        if inRedir:
            sys.stdin = inRedir
        if outRedir:
            sys.stdout = outRedir


    def __closeRedirects__(self):
        npshVM.closeRedirects()
        


    #######################################
    # Built-in commands                   #
    #######################################


    def __man__(self, command, unused, outFile):
        '''Usage: man [command] 
           Outputs the docstring for built-in commands to show basic usage
           When used without argument 'command', prints all available built-in commands.'''

        self.__doBuiltinRedirects__(None, outFile)
                
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

        self.__closeRedirects__()

        
    def __help__(self, command, unused, outFile):
        '''Usage: help [command]
           Outputs the docstring for built-in commands to show basic usage
           When used without argument 'command', prints all available built-in commands. 
           Same as 'man' command'''
        
        self.__doBuiltinRedirects__(None, outFile)
        self.__man__(command, unused, outFile)
        self.__closeRedirects__()


    def __exit__(self, unused, unused2, unused3):
        '''Usage: exit [] 
           Exit the shell'''
        
        #TODO functionality - cause the shell to exit
        self.shell.setExit()
        print("Exiting nps shell")


    def __cd__(self, args, unused, unused2):
        '''Usage: cd [path]
           Change the current working directory to an absolute or relative path'''

        #TODO functionality  - remember the npsh class itself needs to know about this, look in there before
        #                      writing your code here
        
        if len(args) < 1:
            self.shell.setPathName("/")
        else:
            self.shell.setPathName(args[0])
        

    def __echo__(self, args, unused, outFile):
        '''Usage: echo [args] 
           Repeat args to the output'''
        self.__doBuiltinRedirects__(None, outFile)

        #TODO functionality
        for item in args:
            print(item)
            
        self.__closeRedirects__()

      
    def __ls__(self, unused, unused2, outFile):
        '''Usage: ls [] 
           Output the contents of the current directory in alphabetical order'''
        self.__doBuiltinRedirects__(None, outFile)
        
        #TODO functionality, see os module
        #get list of file in directory
        fileList = os.listdir( self.shell.currentPathName ) 
    
        #get size of trminal window
        columns, lines = os.get_terminal_size()
        #find number of files in directory
        listLen = len(fileList)
        #find file with max character size
        maxFileNameLen = max(len(item) for item in os.listdir( self.shell.currentPathName ) ) + 6 # 6 = buffer space
        
        
        #find number of coulmns to print
        numCol = columns//(maxFileNameLen) 
        numRows = listLen//numCol
  
        count = 0
        for item in fileList:
            print(item.ljust(maxFileNameLen), end = " " )
            count+=1
            if count %numCol==0:
                count = 0
                print()
        print("\n")                

        
        self.__closeRedirects__()


    def __parent__(self, unused, unused2, outFile):
        '''Usage: parent [] 
           Output the process ID of the nps shell parent'''
        self.__doBuiltinRedirects__(None, outFile)
         
        #TODO functionality, see os module
        print(os.getppid())
        
        self.__closeRedirects__()

            
    def __pid__(self, unused, unused2, outFile):
        '''Usage: pid [] 
           Output the nps shell process ID'''
        self.__doBuiltinRedirects__(None, outFile)
        
        #TODO functionality, see os module
        print(os.getpid())
        
        self.__closeRedirects__()


        
    def __pwd__(self, unused, unused2, outFile):
        '''Usage: pwd [] 
           Output the current working directory'''
        self.__doBuiltinRedirects__(None, outFile)
        
        #TODO functionality, see os module
        print(os.getcwd())
        
        self.__closeRedirects__()

        
        
    def __rm__(self, args, unused, unused2):
        '''Usage: rm [file] 
           Remove the designated file'''
        #TODO functionality, see os module
        os.remove(args[0])
        




