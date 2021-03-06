# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pickle
from pytplot import data_quants, tplot_opt_glob

def tplot_save(names, filename=None):
    """
    This function will save tplot variables into a single file by using the python "pickle" function.
    This file can then be "restored" using tplot_restore.  This is useful if you want to end the pytplot session,
    but save all of your data/options.  All variables and plot options can be read back into tplot with the 
    "tplot_restore" command.  
    
    Parameters:
        names : str/list
            A string or a list of strings of the tplot variables you would like saved.  
        filename : str, optional
            The filename where you want to save the file.  
            
    Returns:
        None
    
    Examples:
        >>> # Save a single tplot variable
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pytplot.ylim('Variable1', 2, 4)
        >>> pytplot.save('Variable1', filename='C:/temp/variable1.pytplot')

    """
    
    if not isinstance(names, list):
        names = [names]
    
    #Check that we have all available data
    for name in names: 
        if isinstance(data_quants[name].data, list):
            for data_name in data_quants[name].data:
                if data_name not in names:
                    names.append(data_name)
    
    #Pickle it up
    to_pickle =[]
    for name in names:    
        if name not in data_quants.keys():
            print("That name is currently not in pytplot") 
            return
        to_pickle.append(data_quants[name])
    
    num_quants = len(to_pickle)
    to_pickle = [num_quants] + to_pickle
    temp_tplot_opt_glob = tplot_opt_glob
    to_pickle.append(temp_tplot_opt_glob)
    
    if filename==None:
        filename='var_'+'-'.join(names)+'.pytplot'
    
    pickle.dump(to_pickle, open(filename, "wb"))
    
    return