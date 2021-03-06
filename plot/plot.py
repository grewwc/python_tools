import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.axes_grid1 import make_axes_locatable


def _show(action, data, rows, cols, xdata=None, inch=None, shuffle=True,
          xlim=None, ylim=None, labels=None, **kwargs):
    data = data.copy()
    n = rows * cols

    if len(data) < n:
        n = len(data)
        rows = int(n / cols) + 1
        if rows == 1:
            cols = n
    indices = np.arange(n)
    if shuffle:
        indices = np.random.choice(np.arange(len(data)), n, replace=False)

    if isinstance(data, list):
        data = np.r_[data]
    if isinstance(xdata, list):
        xdata = np.r_[xdata]

    data = data[indices]
    if labels is not None:
        labels = labels[indices]
    if xdata is not None:
        xdata = xdata[indices]
    else:
        xdata = np.array([np.arange(len(data[0])) for _ in range(len(data))])

    fig, axes = plt.subplots(rows, cols)
    if rows == 1:  # rows == 1, axes is 1-d array
        axes = np.array([axes])
    if cols == 1:  # same as above
        axes = np.array([axes]).reshape(-1, 1)
    # fig.tight_layout()
    if inch is None:
        inch = 5.0
    x_inches = cols * inch
    y_inches = rows * inch
    fig.set_size_inches(x_inches, y_inches)
    count = 0
    for i in range(rows):
        for j in range(cols):
            if count >= n:
                return
            if xlim is not None:
                axes[i, j].set_xlim(*xlim)
            if ylim is not None:
                axes[i, j].set_ylim(*ylim)
            # axes[i, j].plot(data[count], '.', **kwargs, ms=2.5)
            # img is None if action != 'imshow'
            img = _do(axes[i, j], action, data[count],
                      xdata=xdata[count], **kwargs)
            if action == 'imshow':  # to add colorbar for each ax
                divider = make_axes_locatable(axes[i, j])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                fig.colorbar(img, cax=cax, orientation='vertical')
            if labels is not None:
                axes[i, j].set_title(labels[count])
            else:
                axes[i, j].set_title(f'#[{indices[count]}]')

            count += 1


def _do(ax, action, data, xdata=None, **kwargs):
    try:
        if xdata is None:
            xdata = np.arange(len(data))
        if action == 'imshow':
            getattr(ax, 'set_axis_off')()
            return getattr(ax, action)(data, **kwargs)
        else:
            getattr(ax, action)(xdata, data, **kwargs)

    except AttributeError as e:
        print(e)


def plot1d(data, rows, cols, shuffle=True, inch=None, xlim=None, ylim=None, **kwargs):
    """
    :param data: as the name
    :param rows: # of rows to plot
    :param cols: # of columns to plot
    :param shuffle: if not shuffle, plot data[0] -> data[rows*cols-1]
    :param inch: size of image in rows (inch unit)
    :param kwargs: dictionary to pass to ax.plot()
    :return: None
    """
    set_attr_default(kwargs, '', 'ls', 'linewidth')
    set_attr_default(kwargs, '.', 'marker')
    set_attr_default(kwargs, "1.0", 'ms')
    _show('plot', data, rows, cols, xlim=xlim, ylim=ylim,
          shuffle=shuffle, inch=inch, **kwargs)


def set_attr_default(kwargs, default="", *attrs):
    for arg in attrs:
        if hasattr(kwargs, arg):
            break
    else:
        kwargs.setdefault(attrs[0], default)


def plot(x, y, rows, cols, shuffle=True, inch=None, xlim=None, ylim=None, **kwargs):
    """
        :param data: as the name
        :param rows: # of rows to plot
        :param cols: # of columns to plot
        :param shuffle: if not shuffle, plot data[0] -> data[rows*cols-1]
        :param inch: size of image in rows (inch unit)
        :param kwargs: dictionary to pass to ax.plot()
        :return: None
        """
    set_attr_default(kwargs, "", 'ls', 'linestyle')
    set_attr_default(kwargs, '.', 'marker')
    set_attr_default(kwargs, "1.0", 'ms')
    _show('plot', y, rows, cols, xdata=x, shuffle=shuffle, inch=inch,
          xlim=xlim, ylim=ylim, **kwargs)


def imshow(data, rows, cols, labels=None, shuffle=True, inch=None, **kwargs):
    _show('imshow', data, rows, cols, shuffle=shuffle, inch=inch, labels=labels,
          **kwargs)
