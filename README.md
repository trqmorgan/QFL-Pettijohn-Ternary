# qfl_tern
Ternary plotting but specifically aimed at those working in geology who want to plot petrograpic data. Quartz, feldspar and lithic data derived from petrographic analysis can be plotted on a QFL diagram as per Pettijohn (1977) to gain an idea of their petrographic classification. Recently added the Dickenson (1983) classification diagram.

This repo includes a [notebook](https://github.com/trqmorgan/qfl_tern/blob/master/QFL%20notebook.ipynb) to demonstrate
the use of the QFL ternary as well as the file to run the plotting.

 classified_data, makefig.plot = plot_qfl(data, top=quartz, left=fsp, right=lithic, matrix=matrix, plottype='Pettijohn_1977'
                                     , toplab='Q', leftlab='F', rightlab='L', grid=True, color='r', size=15)
                        
**Parameters:**	    
    
    data: dataframe
    pandas data frame containing the data to which classifications can be appended
    
    top, left, right: str or array-like
    the three paramaters to plot. Commonly these will be 1D arrays, but can also be strings referencing columns in the
    dataframe
    
    matrix: str or array-like, optional, default=None
    if plotting petrographic data clay matrix values can be included. Commonly this will be a 1D array, but can also be
    a string referencing a column in the dataframe
    
    plottype: str, optional, default='blank'
    The background on which to plot the data, options are 'Dickinson_1983', 'Pettijohn_1977' or 'blank'.
                                       
    toplab, leftlab, rightlab: str, optional
    The apex labels as strings
        
    grid: bool, optional, default=False
    To plot grid and axis ticks
     
    color: color, optional
    The marker color
    
    size: scaler, optional
    The marker size   
    
    
**Returns:**

    final_data: dataframe
    The original dataframe with classifications column added, returns None if blank backgound
    
    fig: pyploy figure
    Shown with plt.show()
