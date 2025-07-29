# init

__version__ = "2025.06.18.4"

#####################
# Message verbosity
#####################

print_verbosity=2
log_verbosity = 1


##################################
# matplotlib presets
##################################


def conf_matplolib(
    reset=False,
    legend_marker_scale=2,
    grid=True,
    grid_alpha=0.3,
    fig_autolayout=True,
    labelsize=16,
    labelpad=14,
    font_size=12,
    fig_size=(8, 6),
):
    """Configure matplotlib plot style.

    Parameters
    ----------
    reset : bool
            Whether or not to reset the plot
            layout before configuring.
    fig_size : tuple of int
               The size of the figure.
    fig_autolayout : bool
                     To turn on the figure autolayout
                     or not.
    grid : bool
           Turn grid on or off.
    grid_alpha : float
                 The transparency level of the
                 grid.
    labelsize : int
                The axes label size.
    labelpad : int
               The axes label pad.
    legend_marker_scale : int
                          The legend marker scale.
    """

    import matplotlib.pyplot as plt

    if reset:
        reset_matplotlib()

    plt.rcParams.update({"font.size": font_size})
    plt.rcParams.update({"figure.figsize": fig_size})
    plt.rcParams.update({"axes.grid": grid})
    plt.rcParams.update({"axes.labelpad": labelpad})
    plt.rcParams.update({"axes.labelsize": labelsize})
    plt.rcParams.update({"figure.autolayout": fig_autolayout})
    plt.rcParams.update({"grid.alpha": grid_alpha})
    plt.rcParams.update({"legend.markerscale": legend_marker_scale})


def reset_matplotlib():
    import matplotlib

    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
