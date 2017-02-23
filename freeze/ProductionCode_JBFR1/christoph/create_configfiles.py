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
        

directory = '/Users/christophaymanns/Dropbox/Documents/MATLAB_PYTHON/XML_Files_Co/'
directory_pretty = '/Users/christophaymanns/Dropbox/Documents/MATLAB_PYTHON/XML_Files_Co/pretty/'
prettyOutput = True
testing = False 

###########################################################
#
# The following parameters are fixed for all xml files
#
###########################################################
simParams = ['num_sweeps','num_simulations','num_agents']
valSimParams = [100,100,50]
stateParams = ['theta','rho','lamb']
valStateParams = [1,0.0,0.0]
utilParams = ['alpha','beta','gamma']
valUtilParams = [0.01,0.0,0.1]

###########################################################
#
# The following parameters vary 
#
###########################################################

# signal structures

sig0Mean = [0.25,0.4,0.49]
sig1Mean = [0.75,0.6,0.51]
# signal 0 and signal 1 always have equal variance
sigVars = [0.02,0.1,0.25]

# network densities
networkDensities = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,
0.16,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.3,0.35,0.4,0.45,0.5,0.6,0.7,0.8,0.9,0.96,0.97,0.98,0.99,1.0]

if (testing != True):
    
    ###########################################################
    #
    # Produce files for all parameters
    #
    ###########################################################

    for i in range(0,len(sig0Mean)):
        
        for j in range(0,len(sigVars)):
            
            for k in range (0,len(networkDensities)):
    
                sigParams = ['signal0_mean','signal0_variance','signal1_mean','signal1_variance']
                valSigParams = [sig0Mean[i],sigVars[j],sig1Mean[i],sigVars[j]]
                netParams = ['fixed_network','network_density']
                valNetParams = [True,networkDensities[k]]
                
                root = Element('environment')
                if (sigVars[j] == 0.02 or sigVars[j] == 0.25):
                    title = 'Fig--'+str(valSigParams[0])+'-'+str(valSigParams[2])+'-'+str(sigVars[j])+'-'+str(valNetParams[1])   
                else: 
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