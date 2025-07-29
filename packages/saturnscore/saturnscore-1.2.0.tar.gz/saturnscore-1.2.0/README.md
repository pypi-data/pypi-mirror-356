# Saturn score

## Summary ##
A Python package that computes the Saturn coefficient of a matrix to assess the quality of its UMAP dimensionality reduction.

## Installation ##
You can execute the following command to install this package and its dependencies:

`pip3 install numpy pandas scipy umap-learn scikit-learn saturnscore`

## Example ##
You can run the following Python code to test your package installation:

    import numpy as np
    import pandas as pd
    import scipy
    import umap.umap_ as umap
    from saturnscore import Saturn_coefficient
    from sklearn.preprocessing import StandardScaler

    np.random.seed(0)  # Set random seed for reproducibility
    input_data = np.random.randn(120, 200)  # Generate random matrix X1

    these_n_neighbors = 20
    this_min_dist = 0.01
    these_n_components = 2
    this_metric = 'euclidean'
    this_random_state = 42
    this_n_jobs = 1
    this_n_epochs = 200

    print("these_n_neighbors = ", these_n_neighbors)
    print("this_min_dist = ", this_min_dist)
    print("these_n_components = ", these_n_components)
    print("this_metric = ", this_metric)

    umap_verbose = False
    fit = umap.UMAP(n_neighbors=these_n_neighbors,
    min_dist=this_min_dist,
    n_components=these_n_components,
    metric=this_metric,
    n_jobs=this_n_jobs,
    random_state=this_random_state,
    n_epochs = this_n_epochs,
    verbose=umap_verbose)

    umap_output_layout = fit.fit_transform(input_data)

    result = Saturn_coefficient.SaturnCoefficient(input_data, umap_output_layout)
    print(f" Saturn coefficient =  ", result)

The final command should print something like `Saturn coefficient = 0.11817430122179944` (this value might be different because of the random component of UMAP).

## Contact ##
The `SaturnScore` package was developed by [Davide Chicco](https://www.DavideChicco.it). Questions should be
addressed to davidechicco(AT)davidechicco.it
