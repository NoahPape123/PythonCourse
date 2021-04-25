import pandas as pd, numpy as np

def verify_data(data, target):
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Please provide data in a Pandas DataFrame.")
    data.dropna(inplace=True)
    if data.shape[0] == 0:
        raise ValueError("Unable to perform regression. No observations remain after list-wise deletion.")
    try:
        y = data[target]
    except:
        print("Please explictly identify the target variable by using the proper header.")
    
    X=data.drop(target, axis=1)
    cols = X.columns
    X=X.values
    y=y.values
    return X, y, cols

def test(which):
    if which == 'not_df':
        verify_data('cheese', 'pizza')
    elif which == 'all_nan':
        verify_data(pd.DataFrame([[None, 2, 3],[1, None, 3], [1, 2, None]], columns=['x', 'y', 'z']), 'z')
    elif which == 'bad_target':
        verify_data(pd.DataFrame([[1, 2, 3],[1, 2, 3], [1, 2, 3]], columns=['x', 'y', 'z']), 'pizza')
    