'''
*
* _setup
* GEOVAR SETUP SUPPORT MODULE
*
* Module designed to delegate "setup" functions that serve the GEOVAR class
*
* VERSION: 0.0.1

* KNOWN ISSUES:
*   - Nada atm.
*
*
* AUTHOR                    :   Mohammad Odeh, Fluvio L. Lobo Fenoglietto
* DATE                      :   Jan. 10th, 2019 Year of Our Lord
*
'''

from    platform                    import  system                                                  # Running platform info
import  os, re                                                                                      # Dir/path manipulation, extract numerics from strings
from    datetime                    import  datetime                                                # Get date and time


# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def setup_input_directory( self ):
    '''
    Locates the path to the input files;
        - The repository structure
        - On a Windows OS
    '''
    print( '\n' )
    print( "SETUP INPUT DIR..." )
    dir_list = os.listdir()                                                                         # List elements within current directory
    dir_len  = len(dir_list)
    test_string = 'input'
    test_string_len = len(test_string)
    for i in range( 0, dir_len ):
        if len( dir_list[i] ) >= test_string_len:
            if dir_list[i][0:test_string_len] == test_string:
                print( ">> FOUND" + '\t' + "DIR ...geovar\\" + dir_list[i] )
                match_index = i
                break

    current_dir = os.getcwd()
    input_dir = current_dir + '\\' + dir_list[match_index] + '\\'
    print( ">> CURRENT" + '\t' + "DIR: " + current_dir )
    print( ">> INPUT" + '\t' + "DIR: " + input_dir )

    self.input = input_dir                                                                           # Passing tetgen path to the .self structure
           
# ------------------------------------------------------------------------

def setup_tetgen_directory( self ):
    '''
    Locates the path to the tetgen application within;
        - The repository structure
        - On a Windows OS
    '''
    print( '\n' )
    print( "SETUP TETGEN DIR..." )
    dir_list = os.listdir()                                                                         # List elements within current directory
    dir_len  = len(dir_list)
    test_string = 'tetgen'
    test_string_len = len(test_string)
    for i in range( 0, dir_len ):
        if len( dir_list[i] ) >= test_string_len:
            if dir_list[i][0:test_string_len] == test_string:
                print( ">> FOUND" + '\t' + "DIR ...geovar\\" + dir_list[i] )
                match_index = i
                break

    current_dir = os.getcwd()
    tetgen_dir = current_dir + '\\' + dir_list[match_index] + '\\build\\Debug\\'
    print( ">> CURRENT" + '\t' + "DIR: " + current_dir )
    print( ">> TETGEN" + '\t' + "DIR: " + tetgen_dir )

    self.tet = tetgen_dir                                                                           # Passing tetgen path to the .self structure
           
# ------------------------------------------------------------------------

def setup_directories( self ):
    '''
    Create output folder and point to
    location of compiled TetGen program
    '''

    # ------ UNIX systems ------
    if( system()=='Linux' ):
        src      = os.getcwd()
        self.dst = "{}/output/{}/".format( src,
                                           datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )
        self.tet = args.tetgen_dir                                                                  # Setup tetgen directory

        try:
            os.makedirs( self.dst )
        except OSError:
            print( "FAILED to create directory. Check permissions" )
            quit()
        else:
            print( "Created {}".format(self.dst) )

    # ----- Windows system -----
    elif( system()=='Windows' ):
        # Define useful paths
        src             = os.getcwd()
        self.input      = "{}\\input\\".format( src )                                                    # Setup input directory
        self.doc_def    = self.input + 'doc_def.txt'
        self.dst        = "{}\\output\\{}\\".format( src,
                                                     datetime.now().strftime("%Y-%m-%d__%H_%M_%S") )

        setup_input_directory( self )
        setup_tetgen_directory( self )                                                                  

        try:
            os.makedirs( self.dst )
        except WindowsError:
            print( "FAILED to create directory. Check permissions" )
            quit()
##        else:
##            print( "Created {}".format(self.dst) )

# ------------------------------------------------------------------------

def read_doc( self, filename = 'doc_def.txt' ):
    '''
    READ DOC FILE
        Function responsible for reading and extracting information from
        the "doc" input file
    '''
    print( '' )
    print( "READ DOC FILE..." )
    filepath = self.input + filename
    _doc = open( filepath, 'r' )
    for line in _doc:
        if line[0] == '>':
            address = line
            self.address = address[1:]                                                              # Store the url/web address of the onshape part/document
            break

    address = address.split("/")
    for i in range( 0, len( address ) ):
        if address[i] == 'documents':
            self.did = address[i+1]                                                                 # Store the document id
        elif address[i] == 'w':
            self.wid = address[i+1]                                                                 # Store the workspace id
        elif address[i] == 'e':
            self.eid = address[i+1]                                                                 # Store the element id

    print( ">> DOCUMENT" + '\t' + "ID: " + self.did )
    print( ">> WORKSPACE" + '\t' + "ID: " + self.wid )
    print( ">> ELEMENT" + '\t' + "ID: " + self.eid )

    _doc.close()
    
# ------------------------------------------------------------------------
