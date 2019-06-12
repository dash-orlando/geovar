'''
*
* _febio
* GEOVAR FEBio MODULE
*
* Module designed to delegate "febio-specific" functions or operations
* Most of these functions deal with reading/writing/operating/executing FEBio config files
*
*
* AUTHOR                    :   Fluvio L. Lobo Fenoglietto
* DATE                      :   May 31st, 2019
*
'''

import  numpy                       as      np
from    lxml                        import  etree

# ************************************************************************
# FUNCTIONS =============================================================*
# ************************************************************************

def read_febio_file( febio_filename ):
    '''
    READ FEBio FILE
    '''

    print( '\n' )
    print( "READ FEBio INFO..." )
    #file = self.input + febio_filename
    file = febio_filename
    print(file)

    febio_doc       = etree.parse( file )
    febio_root      = febio_doc.getroot()

    root_len = len(febio_root)
    print( root_len )
    for i in range( 0, root_len ):
        if febio_root[i].tag == 'Geometry':
            geo_index = i


    # extracting parts from the geometry section
    geo = febio_root[geo_index]
    geo_len = len( geo )
    

    #return febio_doc, febio_root, geo, geo_index, geo_len
    #self.febio_doc  = febio_doc
    #self.febio_root = febio_root

    return geo, febio_doc, febio_root

# ------------------------------------------------------------------------------------------------------------ #

def write_febio_file( febio_filename ):
    '''
    WRITE FEBio FILE
    '''

    

# ------------------------------------------------------------------------------------------------------------ #

def get_febio_data( geo ):
    '''
    EXTRACT FEBio FILE DATA
    '''

    print( '\n' )
    print( "EXTRACT FEBio INFO..." )

    # the inputs of this program should be the XML components of interest (e.g.: Geometry)
    geo_len = len(geo)

    fdata                                           = {}
    fdata['baseline']                               = {}
    fdata['baseline']['geo']                        = {}
    fdata['baseline']['geo']['nodes']               = {}
    fdata['baseline']['geo']['nodes']['id']         = []
    fdata['baseline']['geo']['nodes']['text']       = []
    fdata['baseline']['geo']['elements']            = {}
    fdata['baseline']['geo']['elements']['id']      = []
    fdata['baseline']['geo']['elements']['text']    = []
    fdata['baseline']['geo']['nodeset']             = {}

    for i in range( 0, geo_len ):

        #print( i )
        #print( geo[i].tag )

        if geo[i].tag == 'Nodes': # -------------------------------------------------------------------------- #
            print( "> Gathering Nodes..." )
            fdata, nodes_array      = get_nodes(        geo, i, fdata )

        if geo[i].tag == 'Elements': # ----------------------------------------------------------------------- #
            print( "> Gathering Elements..." )
            fdata, elements_array   = get_elements(     geo, i, fdata )
            
        if geo[i].tag == 'NodeSet': # ------------------------------------------------------------------------ #
            print( "> Gathering NodeSet(s)..." )
            fdata                   = get_nodeset(      geo, i, fdata )
                    

    # update structure
    fdata['baseline']['geo']['nodes']['array']          = nodes_array
    fdata['baseline']['geo']['elements']['array']       = elements_array
    
    return fdata, nodes_array, elements_array   

# ------------------------------------------------------------------------------------------------------------ #

def get_nodes( geo, index, fdata ):
    '''
    GET NODE DATA
    '''
    nodes               = geo[index]
    nodes_len           = len( nodes )

    # initializing numpy arrays
    nodes_array         = np.zeros(( nodes_len, 3 ), dtype=float)
    
    for j in range( 0, nodes_len ):           

        # extracting raw data
        ## extracting nodes
        fdata['baseline']['geo']['nodes']['id'].append(         nodes[j].attrib['id'] )
        fdata['baseline']['geo']['nodes']['text'].append(       nodes[j].text )
        
        # tranform into numeric values for proper manipulation
        nodes_array[j]  = nodes[j].text.split(',')

    return fdata, nodes_array

# ------------------------------------------------------------------------------------------------------------ #

def get_elements( geo, index, fdata ):
    '''
    GET ELEMENT DATA
    '''
    elements            = geo[index]
    elements_len        = len( elements )

    # using attributes to ensure proper extraction
    # this will be implemented now and should be standard in the future
    if elements.attrib['type'] == 'tet4':
        print( ">> The mesh uses tets of 4 nodes" )
        nodes_per_tet = 4

    # initializing numpy arrays
    elements_array      = np.zeros(( elements_len, nodes_per_tet ), dtype=int)
    
    for j in range( 0, elements_len ):           

        # extracting raw data
        ## extracting elements
        fdata['baseline']['geo']['elements']['id'].append(      elements[j].attrib['id'] )
        fdata['baseline']['geo']['elements']['text'].append(    elements[j].text )
        
        # tranform into numeric values for proper manipulation
        elements_array[j] = elements[j].text.split(',')

    return fdata, elements_array

# ------------------------------------------------------------------------------------------------------------ #

def get_nodeset( geo, index, fdata ):
    '''
    GET NODESET DATA
    '''
    nodeset = geo[index]
    nodeset_len = len(nodeset)

    # using the attributes
    nodeset_type = nodeset.attrib['name']
    nodeset_len = len(nodeset)

    if nodeset_type[:-2] == 'FixedDisplacement': # ----------------------------------------------------------- #
        label_str = 'fixdisp{}'.format(nodeset_type[len(nodeset_type)-2:])
        fdata['baseline']['geo']['nodeset'][label_str]          = {}
        fdata['baseline']['geo']['nodeset'][label_str]['id']    = []
        for j in range( 0, nodeset_len ):
            fdata['baseline']['geo']['nodeset'][label_str]['id'].append( nodeset[j].attrib['id'] )

    if nodeset_type[:-2] == 'PrescribedDisplacement': # ------------------------------------------------------ #
        label_str = 'presdisp{}'.format(nodeset_type[len(nodeset_type)-2:])
        fdata['baseline']['geo']['nodeset'][label_str]          = {}
        fdata['baseline']['geo']['nodeset'][label_str]['id']    = []
        for j in range( 0, nodeset_len ):
            fdata['baseline']['geo']['nodeset'][label_str]['id'].append( nodeset[j].attrib['id'] )

    elif nodeset_type[:-2] != 'FixedDisplacement' and nodeset_type[:-2] != 'PrescribedDisplacement':
        message = "The current version of GEOVAR does not support FEBio's NoseSet:Type {}".format( nodeset_type )
        print( message )

    return fdata
