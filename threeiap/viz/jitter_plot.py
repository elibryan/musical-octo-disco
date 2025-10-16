
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

from threeiap.util.colors import adjust_lightness
from threeiap.util.util import get_in
from threeiap.viz.style import style_default


def set_lims(ax, **kwargs):
    xlim = kwargs.get('xlim')
    ylim = kwargs.get('ylim')
    if xlim is not None:
        ax.set_xlim(xlim[0], xlim[1])

    if ylim is not None:
        ax.set_ylim(ylim[0], ylim[1])


def set_labels(ax, **kwargs):
    xlabel = kwargs.get('xlabel')
    ylabel = kwargs.get('ylabel')
    title = kwargs.get('title')
    if (xlabel is not None):
        ax.set_xlabel(xlabel)

    if (ylabel is not None):
        ax.set_ylabel(ylabel)

    if (title is not None):
        ax.set_title(title)


def jitter_plot(df, x, alpha=.5, style=style_default, **kwargs):
    y = kwargs.get('y')
    dot_size = kwargs.get('dot_size', 5)
    palette = kwargs.get('palette', get_in(style, ["colors"]))
    width_in = kwargs.get('width_in', get_in(style, ["target_chart_dims"])[0])
    height_in = kwargs.get('height_in', get_in(style, ["target_chart_dims"])[1])
    ref_line_value_fn = kwargs.get('ref_line_value_fn', lambda df_values, **kwargs: df_values.mean())
    order_value_fn = kwargs.get('order_value_fn', lambda df_values, **kwargs: df_values.mean())
    ascending = kwargs.get('ascending', False)
    ref_line_value_format_fn = kwargs.get('ref_line_value_format_fn', lambda v: round(v, 2))
    benchmark_range = kwargs.get('benchmark_range', None)
    fig = kwargs.get('fig', None)
    ax = kwargs.get('ax', None)
    hue = kwargs.get('hue')
    dodge = kwargs.get('dodge', True)
    jitter = kwargs.get('jitter', 0.3)
    show_ref_line_label = kwargs.get('show_ref_line_label', True)
    global_dpi = get_in(style, ["chart_dpi"])

    # additional arguments that get passed to seaborn
    strip_extra_args = {}

    # create an axis if needed
    if (fig is None or ax is None):
        fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=global_dpi, constrained_layout=True)

    y_values_ordered = None
    row_count = 1

    if (y is not None):
        y_values = df[y].unique()
        row_count = len(y_values)
        y_values = [v for v in y_values if v is not None]

        def sort_fn(cur_y):
            cur_df = df[df[y] == cur_y]
            cur_values = cur_df[x]
            return order_value_fn(cur_values, y_value=cur_y, x=x, df=cur_df)

        y_values_ordered = sorted(y_values, key=sort_fn, reverse=not ascending)

        strip_extra_args['y'] = y
        strip_extra_args['order'] = y_values_ordered

    # setup for multiple hues
    hue_values = None
    hue_count = 1
    if hue is not None:
        hue_values = df[hue].unique()
        hue_count = len(hue_values)
        palette = palette[:hue_count]

        strip_extra_args['palette'] = palette
        strip_extra_args['hue'] = hue
        strip_extra_args['dodge'] = dodge
    else:
        palette = palette[:1]

    # Draw the main plot
    g = sns.stripplot(ax=ax,
                      data=df,
                      x=x,
                      alpha=alpha,
                      size=dot_size,
                      jitter=jitter,
                      **strip_extra_args
                      )

    # Don't show legend
    ax.legend([], [], frameon=True)

    set_lims(ax, **{k: kwargs.get(k) for k in ['xlim', 'ylim']})
    set_labels(ax, **{k: kwargs.get(k) for k in ['xlabel', 'ylabel', 'title']})

    # Draw reference lines for each y_value + hue combo
    for row_index in range(row_count):
        for hue_index in range(hue_count):
            cur_df = df

            y_value = None
            if y is not None:
                y_value = y_values_ordered[row_index]
                cur_df = cur_df[cur_df[y] == y_value]

            if hue is not None:
                hue_value = hue_values[hue_index]
                cur_df = cur_df[cur_df[hue] == hue_value]

            ################################
            # Draw the reference lines
            ref_line_value = ref_line_value_fn(cur_df[x], df=cur_df, x=x, y=y, y_value=y_value)
            # I can't remember where .8 comes from.. maybe the jitter setting for seaborn?
            row_height = .8;
            hue_row_height = .8 * row_height / hue_count
            hue_row_spacing = .2 * row_height / hue_count
            # middle of the row, offset to top of the row, offset by hue row
            y_ref_line_top = row_index + (-row_height * .5 + hue_row_spacing * .5) + (
                    hue_index * (hue_row_height + hue_row_spacing))

            # Draw the line itself
            ax.plot(
                [ref_line_value, ref_line_value],
                [y_ref_line_top, y_ref_line_top + hue_row_height],
                c=adjust_lightness(palette[hue_index], .5),
                zorder=3)

            # draw the label

            if show_ref_line_label:
                ax.text(ref_line_value,
                        y_ref_line_top,
                        ref_line_value_format_fn(ref_line_value),
                        horizontalalignment='center',
                        va='bottom',
                        size='x-small',
                        color=get_in(style, ['colors', 'black'], 'black'),
                        )

            if benchmark_range is not None:
                bm_rect = matplotlib.patches.Rectangle((benchmark_range[0], row_index - .4,),
                                                       benchmark_range[1] - benchmark_range[0], .8,
                                                       color=get_in(style, ['colors', 'benchmark_bg'], '#F2F2F2'),
                                                       alpha=0.1,
                                                       zorder=-3)

                ax.add_patch(bm_rect)

                ax.plot([benchmark_range[0], benchmark_range[0]], [row_index - .4, row_index + .4],
                        c=get_in(style, ['colors', 'benchmark_bg'], '#F2F2F2'),
                        lw=.5,
                        ls="--",
                        zorder=3)

                ax.plot([benchmark_range[1], benchmark_range[1]], [row_index - .4, row_index + .4],
                        c=get_in(style, ['colors', 'benchmark_bg'], '#F2F2F2'),
                        lw=.5,
                        ls="--",
                        zorder=3)
