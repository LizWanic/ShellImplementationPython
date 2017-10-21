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

# global builtins 

# builtins = {
#                 'man' : self.__man__,
#                'help' : self.__help__,
#                  'cd' : self.__cd__,
#                'echo' : self.__echo__,
#                'exit' : self.__exit__,
#                  'ls' : self.__ls__,
#              'parent' : self.__parent__,
#                 'pid' : self.__pid__,
#                 'pwd' : self.__pwd__,
#                  'rm' : self.__rm__
#         }

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

        # this version of subprocess wants the command and arguments together as a string,
        #    so we make that string now
        callList = [self.command]
        callList.extend(self.args)
        cmd = ' '.join(callList)
        
        try:
            #call the external command as a subprocess,
            #   check option will throw an exception is the launch fails
            #   shell option gives us the correct flow thru's to OS shell via parent shells
            #   STDIN/STDOUT when stdin/stdout are set to None
            #TODO use what you figured out from spDemo.py
            subprocess.run(cmd, stdin=infile, stdout=outfile, shell=True, check=True) 
            
            
        #TODO properly re-raise any exception so it can be handled in shell input loop and not
        #        crash whole shell
        except RuntimeError as re:
            print('Error:', re)
        except IOError as ioe:
            print('Error:', ioe)
        except subprocess.CalledProcessError as cpe:
            print('Error:', cpe)
        
        finally:
            #TODO ALWAYS close and reset the redirects
            npshVM.closeRedirects()
            




############################################
# static methods

    @staticmethod
    def openRedirects(infile, outfile):
        '''If the input/output files have been changed from default, opens them
           does nothing if the input/output file is not used at all -- indicated by None'''

        if infile != None:
            if pathlib.Path(infile).exists():
            #TODO file exists condition    https://docs.python.org/3/library/pathlib.html
            #   you can do this without pathlib, but it is easier to do it with pathlib
            #     (plus you get transparent cross-platform-ability, making it easier to share code in-group)
                
                try :
                    #if self.command in builtins.keys():
                    infile = open(infile, 'r')
                    #else:
                        #infile = open(infile, 'r') #TODO open it up
                except IOError as ioe:
                    print('Error:', ioe)     #re-raises the exception so it can be handled in input loop
 
            else:
                raise IOError("Input file '" + str(infile) + " ' does not exist.")

        if outfile != None:
            #sys.stdout = outfile 
            try :
                outfile = open(outfile, 'w') #TODO opens file in overwrite mode
                #print("HEYYYYYYYYYY")
            except IOError as ioe:
                    print('Error:', ioe)      #re-raises the exception so it can be handled in input loop

        return (infile, outfile)



    @staticmethod
    def closeRedirects():
        ''' If the input/output channels have been changed from default std, close the redirect files/pipe file
            this method is complete.

            It does illustrate some of the two-step naming conventions associated
            with managing the interface between sys.stdin (standard in's channel within Python)
            and sys.__stdin__ (which is Python's variable name bound to the system provided STDIN buffer.)'''
        
        if sys.stdin != sys.__stdin__:  
            sys.stdin.close()
            sys.stdin = sys.__stdin__
            
        if sys.stdout != sys.__stdout__: 
            sys.stdout.close()
            sys.stdout = sys.__stdout__






