import pandas as pd, numpy as np
from assignment_verify import verify_data

def our_ols(data, target):
    X, y, cols = verify_data(data, target)
    betas = np.dot(np.dot(np.linalg.inv(np.dot(X.transpose(), X)),X.transpose()), y)
    y_hat = np.dot(X, betas)
    e = y - y_hat
    sigma_squared = np.dot(e.transpose(), e) / (X.shape[0] - X.shape[1] - 1)
    var_betas = sigma_squared * np.linalg.inv(np.dot(X.transpose(), X)).diagonal()

    
    betas_se = np.sqrt(var_betas)
    betas_low = betas - 1.96*betas_se
    betas_high = betas + 1.96*betas_se
    results = [betas, betas_se, betas_low, betas_high]
    print(pd.DataFrame(results, index=['coef', 'std err', '[0.025', '0.975]'], columns=cols).T)