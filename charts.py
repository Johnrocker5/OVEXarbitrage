import data
import altair as alt
import datetime
from vega_datasets import data
import plotly.figure_factory as ff
import numpy as np
import scipy


def get_chart_spread(source):
    hover = alt.selection_single(
        fields=["Time"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(source, title="Spread history")
        .mark_line()
        .encode(
            x="Time",
            y="Spread",
            color='Type'
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(source)
        .mark_rule()
        .encode(
            x="Time",
            y="Spread",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Time", title="Time"),
                alt.Tooltip("Spread", title="Spread (%)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


def get_chart_rates(source):
    hover = alt.selection_single(
        fields=["Time"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(source, title="Exchange rate history")
        .mark_line()
        .encode(
            x="Time",
            y="Exchange rate",
            color='Market'
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(source)
        .mark_rule()
        .encode(
            x="Time",
            y="Exchange rate",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Time", title="Time"),
                alt.Tooltip("Exchange rate", title="Exchange rate"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()

def real_rate_chart(source):
    chart = get_chart_rates(source=source)
    minimum = min(source['Exchange rate'])
    maximum = max(source['Exchange rate'])
    chart = chart.encode(alt.Y('Exchange rate',
                               scale=alt.Scale(domain=(round(minimum - 0.05, 1),
                                                       round(maximum + 0.05, 1)))))
    return chart

def get_dist_chart(source):
    spot_spread = np.array(source['Spot spread'])
    fx_spread = np.array(source['FX spread'])
    hist_data = [spot_spread, fx_spread]
    group_labels = ['Spot spread', 'FX Spread']
    fig = ff.create_distplot(hist_data,
                             group_labels,
                             bin_size=[.1, .25, .5],
                             curve_type='normal')
    return fig


def get_day_charts(source, hours):

    ln = len(source.index)

    if hours == 'all':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if ln == 7:
            sort = days
        elif ln != 7:
            if ln == 5:
                sort = ['Monday', 'Tuesday', 'Wednesday', 'Saturday', 'Sunday']
            if ln == 6:
                sort = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday']

    if hours == 'business':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if ln == 5:
            sort = days
        elif ln != 5:
            if ln == 3:
                sort = ['Monday', 'Tuesday', 'Wednesday']
            if ln == 4:
                sort = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']

    chart1 = alt.Chart(source, title='Mean')\
        .mark_bar()\
        .encode(x=alt.X('Day:N', axis=alt.Axis(title=''), sort=sort),
                y=alt.Y('Mean:Q', axis=alt.Axis(title='')),
                color=alt.Color('Day:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Day:N', 'Mean:Q']) \
        .properties(width=200) \
        .interactive()

    chart2 = alt.Chart(source, title='Median')\
        .mark_bar()\
        .encode(x=alt.X('Day:N', axis=alt.Axis(title=''), sort=sort),
                y=alt.Y('Median:Q', axis=alt.Axis(title='')),
                color=alt.Color('Day:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Day:N', 'Median:Q']) \
        .properties(width=200) \
        .interactive()

    chart3 = alt.Chart(source, title='90th percentile')\
        .mark_bar()\
        .encode(x=alt.X('Day:N', axis=alt.Axis(title=''), sort=sort),
                y=alt.Y('90th percentile:Q',
                axis=alt.Axis(title='')),
                color=alt.Color('Day:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Day:N', '90th percentile:Q']) \
        .properties(width=200) \
        .interactive()

    chart4 = alt.Chart(source, title='95th percentile')\
        .mark_bar()\
        .encode(x=alt.X('Day:N', axis=alt.Axis(title=''), sort=sort),
                y=alt.Y('95th percentile:Q',
                axis=alt.Axis(title='')),
                color=alt.Color('Day:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Day:N', '95th percentile:Q']) \
        .properties(width=200) \
        .interactive()

    chart5 = alt.Chart(source, title='99th percentile')\
        .mark_bar()\
        .encode(x=alt.X('Day:N', axis=alt.Axis(title=''), sort=sort),
                y=alt.Y('99th percentile:Q',
                axis=alt.Axis(title='')),
                color=alt.Color('Day:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Day:N', '99th percentile:Q']) \
        .properties(width=200) \
        .interactive()

    chart6 = alt.Chart(source, title='Maximum')\
        .mark_bar()\
        .encode(x=alt.X('Day:N', axis=alt.Axis(title=''), sort=sort),
                y=alt.Y('Maximum:Q', axis=alt.Axis(title='')),
                color=alt.Color('Day:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Day:N', 'Maximum:Q']) \
        .properties(width=200) \
        .interactive()

    chart7 = alt.hconcat(chart1, chart2, chart3)
    chart8 = alt.hconcat(chart4, chart5, chart6)
    chart9 = alt.vconcat(chart7, chart8)

    return chart9


def get_time_charts(source, hours):

    if hours == 'all':
        sort = ['Between 00:00 and 01:00', 'Between 01:00 and 02:00', 'Between 02:00 and 03:00',
                'Between 03:00 and 04:00', 'Between 05:00 and 05:00', 'Between 05:00 and 06:00',
                'Between 06:00 and 07:00', 'Between 07:00 and 08:00', 'Between 08:00 and 09:00',
                'Between 09:00 and 10:00', 'Between 10:00 and 11:00', 'Between 11:00 and 12:00',
                'Between 12:00 and 13:00', 'Between 13:00 and 14:00', 'Between 14:00 and 15:00',
                'Between 15:00 and 16:00', 'Between 16:00 and 17:00', 'Between 17:00 and 18:00',
                'Between 18:00 and 19:00', 'Between 19:00 and 20:00', 'Between 20:00 and 21:00',
                'Between 21:00 and 22:00', 'Between 22:00 and 23:00', 'Between 23:00 and 24:00']

    if hours == 'business':
        sort = ['Between 08:00 and 09:00', 'Between 09:00 and 10:00', 'Between 10:00 and 11:00',
                'Between 11:00 and 12:00', 'Between 12:00 and 13:00', 'Between 13:00 and 14:00',
                'Between 14:00 and 15:00', 'Between 15:00 and 16:00', 'Between 16:00 and 17:00']

    chart1 = alt.Chart(source, title='Mean')\
        .mark_bar()\
        .encode(x=alt.X('Time:N', axis=alt.Axis(title='', labels=False), sort=sort),
                y=alt.Y('Mean:Q', axis=alt.Axis(title='')),
                color=alt.Color('Time:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Time:N', 'Mean:Q']) \
        .properties(width=300) \
        .interactive()

    chart2 = alt.Chart(source, title='Median')\
        .mark_bar()\
        .encode(x=alt.X('Time:N', axis=alt.Axis(title='', labels=False), sort=sort),
                y=alt.Y('Median:Q', axis=alt.Axis(title='')),
                color=alt.Color('Time:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Time:N', 'Median:Q']) \
        .properties(width=300) \
        .interactive()

    chart3 = alt.Chart(source, title='90th percentile')\
        .mark_bar()\
        .encode(x=alt.X('Time:N', axis=alt.Axis(title='', labels=False), sort=sort),
                y=alt.Y('90th percentile:Q',
                axis=alt.Axis(title='')),
                color=alt.Color('Time:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Time:N', '90th percentile:Q']) \
        .properties(width=300) \
        .interactive()

    chart4 = alt.Chart(source, title='95th percentile')\
        .mark_bar()\
        .encode(x=alt.X('Time:N', axis=alt.Axis(title='', labels=False), sort=sort),
                y=alt.Y('95th percentile:Q',
                axis=alt.Axis(title='')),
                color=alt.Color('Time:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Time:N', '95th percentile:Q']) \
        .properties(width=300) \
        .interactive()

    chart5 = alt.Chart(source, title='99th percentile')\
        .mark_bar()\
        .encode(x=alt.X('Time:N', axis=alt.Axis(title='', labels=False), sort=sort),
                y=alt.Y('99th percentile:Q',
                axis=alt.Axis(title='')),
                color=alt.Color('Time:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Time:N', '99th percentile:Q']) \
        .properties(width=300) \
        .interactive()

    chart6 = alt.Chart(source, title='Maximum')\
        .mark_bar()\
        .encode(x=alt.X('Time:N', axis=alt.Axis(title='', labels=False), sort=sort),
                y=alt.Y('Maximum:Q', axis=alt.Axis(title='')),
                color=alt.Color('Time:N', sort=sort, scale=alt.Scale(scheme='tableau20')),
                tooltip=['Time:N', 'Maximum:Q'])\
        .properties(width=300)\
        .interactive()

    chart7 = alt.hconcat(chart1, chart2)
    chart8 = alt.hconcat(chart3, chart4)
    chart9 = alt.hconcat(chart5, chart6)
    chart10 = alt.vconcat(chart7, chart8, chart9)

    return chart10