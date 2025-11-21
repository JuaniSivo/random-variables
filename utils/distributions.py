from distributions.uniform_dist import uniform_ui, uniform_sample
from distributions.gaussian_dist import gaussian_ui, gaussian_sample
from distributions.lognormal_dist import lognormal_ui, lognormal_sample
from distributions.triangular_dist import triangular_ui, triangular_sample

DIST_UI_SAMPLE = {
    "Uniform": (uniform_ui, uniform_sample),
    "Gaussian": (gaussian_ui, gaussian_sample),
    "Lognormal": (lognormal_ui, lognormal_sample),
    "Triangular": (triangular_ui, triangular_sample)
}