import numpy as np
import scipy.interpolate as interp
from scipy.optimize import linear_sum_assignment

def band_matrix(window: int, N):
    '''
    return NxN band matrix so that matrices multiplied by band matrix retain a +/- window on each side of diagonal element and discard points outside

    '''

    a = np.zeros((N,N))
    i,j = np.indices(a.shape)
    for n in range(window+1):
        a[i==j] = 1.
        a[i==j+n] = 1.
        a[i==j-n] = 1.
    a[a==0]='nan'
    return a

def reorder(A, B, window):
    '''
    apply reordering algorithm to series B to optimally match series A,
    within allowed window of days

    threshold_type 'lower' - match high temperature extremes
    threshold_type 'upper' - match low temperature extremes
    '''
    
    N = len(A) # total number of days
    #if isinstance(B, list):
    #    cost_matrix = np.median([np.absolute(A[:, None] - this_B[None, :]) for this_B in B], axis=0)
    #else:
    #    assert len(A) == len(B)
    cost_matrix = (A[:, None] - B[None, :])**2 
    exclude_cost = cost_matrix.max()*10 # set arbitrarily high cost to prevent reordering of these points

    b = band_matrix(window, N)
    banded_cost_matrix = cost_matrix * b
    banded_cost_matrix[np.isnan(banded_cost_matrix)] = exclude_cost

    row_index, column_index = linear_sum_assignment(np.abs(banded_cost_matrix)) # find assignent of rows to columns with minimum cost
    
    if isinstance(B, list):
        Bs_matched = [
            [this_B[i] for i in column_index]
            for this_B in B
        ]
        return Bs_matched
        
    B_matched = [B[i] for i in column_index]
    return B_matched

def rmse(A, B):
    '''
    root mean sq error
    '''
    return ((A-B)**2).mean()**0.5

def threshold_cost(A, B, threshold, threshold_type):
    '''
    calculate rmse cost of B wrt A above/below specified threshold
    threshold_type = "lower" - evaluate for points where A > threshold
    threshold_type = "upper" - evaluate for points where A < threshold
    '''

    if threshold_type == 'none':
        include_indices = [i for i in range(len(A))]

    elif threshold_type == 'lower':
        exclude_indices = [i for i in range(len(A)) if A[i] < threshold]
        include_indices = [i for i in range(len(A)) if A[i]>= threshold]

    elif threshold_type == 'upper':
        include_indices = [i for i in range(len(A)) if A[i] < threshold]
        exclude_indices = [i for i in range(len(A)) if A[i]>= threshold]

    else:
        print("select threshold 'none', 'lower', 'upper'")

    A_selected = np.array(A)[include_indices]    
    B_selected = np.array(B)[include_indices]

    cost = rmse(A_selected, B_selected)

    return cost

def reordering_cost(A, B, window, threshold, threshold_type):
    '''
    reorder + calculate cost
    threshold_type = 'none', 'lower', 'upper'
    '''
    B_matched = reorder(A, B, window)
    cost = threshold_cost(A, B_matched, threshold, threshold_type)
    return cost