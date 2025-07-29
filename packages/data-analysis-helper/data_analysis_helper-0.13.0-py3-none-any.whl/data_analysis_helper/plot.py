# SPDX-FileCopyrightText: 2024-present Anfeng Li <anfeng.li@cern.ch>
#
# SPDX-License-Identifier: MIT


def histplot(
    x,
    bins,
    *,
    xlabel: str,
    unit: str | None = None,
    range=None,
    ax=None,
    weights=None,
    histtype="errorbar",
    **kwargs,
):
    import matplotlib.pyplot as plt
    import mplhep
    import numpy as np

    if ax is None:
        fig, ax = plt.subplots()
    if weights is None:
        weights = np.ones(len(x))
    hist, bin_edges = np.histogram(x, bins, range=range, weights=weights)
    hist_sq, _ = np.histogram(x, bin_edges, range=range, weights=weights**2)
    mplhep.histplot(
        hist, bins=bin_edges, w2=hist_sq, histtype=histtype, ax=ax, **kwargs
    )
    ax.set_xlabel(f"{xlabel}" if unit is None else f"{xlabel} ({unit})")
    ax.set_ylabel(
        f"Events / {bin_edges[1] - bin_edges[0]:.2f}"
        if unit is None
        else f"Events / {bin_edges[1] - bin_edges[0]:.2f} ({unit})"
    )
