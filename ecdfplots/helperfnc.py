from statsmodels.distributions.empirical_distribution import ECDF
from statsmodels.distributions import empirical_distribution as emp_dist


def ecdf_CI(x):
    cdf_x = ECDF(x)
    x.sort()
    F_x = cdf_x(x)
    low_x, up_x = emp_dist._conf_set(F_x)
    return x, F_x, low_x, up_x
