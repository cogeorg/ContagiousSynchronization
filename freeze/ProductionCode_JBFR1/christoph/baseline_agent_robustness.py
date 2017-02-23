from xml.etree.ElementTree import Element, SubElement, tostring, Comment
from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):
    rough_string = ElementTree.tostring(elem,'utf-8')
    reparsed = minidom.parseString(rough_string)
    return [reparsed.toprettyxml(indent=" "),reparsed]

def createParameterEntries(root,types,values):
    if (len(types) != len(values) or isinstance(root,Element) != True):
        if (len(types) != len(values)):
            print("each parameter type must have an assigned value.")
        if (isinstance(root,Element) != True):
            print("toot must be of type Element")            
    else:
        for i in range(0,len(types)):
            paramtype = SubElement(root,'parameter')
            paramtype.set('type',types[i])
            paramtype.set('value',str(values[i]))
        

directory = '/Users/christophaymanns/Dropbox/Documents/MATLAB_PYTHON/XML_Files_Co/baseline/'
directory_pretty = '/Users/christophaymanns/Dropbox/Documents/MATLAB_PYTHON/XML_Files_Co/baseline_pretty/'
prettyOutput = True
testing = False 

###########################################################
#
# The following parameters vary
#
###########################################################

nAgents = [5,10,15,20,25,30,35,40,50,75,100]

###########################################################
#
# The following parameters are fixed for all xml files
#
###########################################################

stateParams = ['theta','rho','lamb']
valStateParams = [1,0.0,0.0]
utilParams = ['alpha','beta','gamma']
valUtilParams = [0.01,0.0,0.1]
sigParams = ['signal0_mean','signal0_variance','signal1_mean','signal1_variance']
valSigParams = [0.4,0.1,0.6,0.1]
netParams = ['fixed_network','network_density']
valNetParams = [True,0.1]

if (testing != True):
    
    ###########################################################
    #
    # Produce files for all parameters
    #
    ###########################################################

    for i in range(0,len(nAgents)):
                
        simParams = ['num_sweeps','num_simulations','num_agents']
        valSimParams = [100,100,nAgents[i]]
        
        root = Element('environment')
        title = 'Fig--'+str(valSigParams[0])+'-'+str(valSigParams[2])+'-'+str(valNetParams[1])+'-'+str(nAgents[i])
        #root.set('title','Fig--0.4-0.6-0.01')
        root.set('title',title)
        
        comment = Comment('simulation parameters')
        root.append(comment)
        createParameterEntries(root,simParams,valSimParams)
            
        comment = Comment('state parameters')
        root.append(comment)
        createParameterEntries(root,stateParams,valStateParams)
            
        comment = Comment('utility function parameters ')
        root.append(comment)
        createParameterEntries(root,utilParams,valUtilParams)
            
        comment = Comment('signal parameters')
        root.append(comment)
        createParameterEntries(root,sigParams,valSigParams)
        
        comment = Comment('parameters required to get figures for results')
        root.append(comment)
        createParameterEntries(root,netParams,valNetParams)
        
        
        if prettyOutput:
            prettyRoot = prettify(root)
            prettyRoot[1].writexml(open(directory_pretty+title+'.xml','wb'),indent=" ",newl='\n')
            #print(prettyRoot[0])
        else:
            et = ElementTree.ElementTree(root)
            et.write(directory+title+'.xml')

else:
    
    ###########################################################
    #
    # Test the implemenation with one set of parameters
    #
    ###########################################################
    
    sigParams = ['signal0_mean','signal0_variance','signal1_mean','signal1_variance']
    valSigParams = [0.4,0.1,0.6,0.1]
    netParams = ['fixed_network','network_density']
    valNetParams = [True,0.1]
    
    root = Element('environment')
    title = 'Fig--'+str(valSigParams[0])+'-'+str(valSigParams[2])+'-'+str(valNetParams[1])
    #root.set('title','Fig--0.4-0.6-0.01')
    root.set('title',title)
    
    comment = Comment('simulation parameters')
    root.append(comment)
    createParameterEntries(root,simParams,valSimParams)
        
    comment = Comment('state parameters')
    root.append(comment)
    createParameterEntries(root,stateParams,valStateParams)
        
    comment = Comment('utility function parameters ')
    root.append(comment)
    createParameterEntries(root,utilParams,valUtilParams)
        
    comment = Comment('signal parameters')
    root.append(comment)
    createParameterEntries(root,sigParams,valSigParams)
    
    comment = Comment('parameters required to get figures for results')
    root.append(comment)
    createParameterEntries(root,netParams,valNetParams)
    
    
    if prettyOutput:
        prettyRoot = prettify(root)
        prettyRoot[1].writexml(open(directory_pretty+title+'.xml','wb'),indent=" ",newl='\n')
        #print(prettyRoot[0])
    else:
        et = ElementTree.ElementTree(root)
        et.write(directory+title+'.xml')