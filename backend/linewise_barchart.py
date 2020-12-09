import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# st.title("Let's do some performance analysis!")
from prof_file_util import load_line_profile
from linewise_visualize import code_line_visualize

def circling_legend(line_width=20.0, code_panel_width=500.0):
    df = pd.DataFrame({'color': ['blue', 'red', 'brown', 'green', 'yellow'],
                       'text': ['Current Line',
                                'Current Function Block (Non-recursive)',
                                'Current Function Block (Recursive)',
                                'Caller Functions',
                                'Callee Functions'],
                       'width': [2, 3, 3, 3, 3],
                       'pos': list(range(0, 5))})

    df['X2'] = 0
    df['X'] = code_panel_width / 2
    df['Y2'] = (len(df) - df['pos'] - 1) * line_width
    df['Y'] = (len(df) - df['pos']) * line_width
    df['X_mid'] = (df['X'] + df['X2']) / 2
    df['Y_mid'] = (df['Y'] + df['Y2']) / 2

    layer_1 = alt.Chart(df).mark_rect(filled=False).encode(
        alt.X('X:Q', axis=None),
        alt.Y('Y:Q', axis=None),
        alt.X2('X2:Q'),
        alt.Y2('Y2:Q'),
        alt.Color('color:N', legend=None, scale=alt.Scale(domain=['blue', 'red', 'brown', 'green', 'yellow'],
                    range=['blue', 'red', 'brown', 'green', 'yellow'])),
        alt.StrokeWidth('width', legend=None),
    )

    layer_2 = alt.Chart(df).mark_text(size=line_width * 0.8).encode(
        alt.X('X_mid', axis=None),
        alt.Y('Y_mid', axis=None),
        alt.Text('text'),
    )

    return alt.layer(layer_1, layer_2).properties(width=code_panel_width * 0.7, height=line_width * len(df))


def linewise_barchart(df, line_width=20.0, code_panel_width=500.0, use_func_barchart=True):
    
    # with open('demo.c') as f:
    #     st.code(f.read(), language='c')
    # st.write(df)

    func_time = df.groupby('Func')['Time'].sum().reset_index()
    func_time = func_time[func_time['Func'] != '<not sampled>'].sort_values('Time')

    func_selector = alt.selection_single(fields=['Func'])

    func_time_bar = alt.Chart(func_time).mark_bar().encode(
        x=alt.X('Time:Q'),
        y=alt.Y('Func:N', sort='-x'),
        tooltip=alt.TooltipValue('Click for Selected View'),
        color=alt.condition(func_selector, alt.value("steelblue"), alt.value("lightgrey"))
    ).add_selection(
        func_selector
    )

    line_time_bar = alt.Chart(df).mark_bar().encode(
        x=alt.X('Time:Q', scale=alt.Scale(reverse=True)),
        y=alt.Y('Line Number:O', scale=alt.Scale(domain=list(range(0, len(df) + 1))), axis=None),
    )
    
    if use_func_barchart:
        line_time_bar = line_time_bar.transform_filter(
            func_selector
        )

    # Add a grey back ground 
    whole_line_time_bar = alt.Chart(df).mark_bar().encode(
        x=alt.X('Time:Q', scale=alt.Scale(reverse=True)),
        y=alt.Y('Line Number:O', scale=alt.Scale(domain=list(range(0, len(df) + 1))), axis=None),
        color=alt.value('lightgrey'),
        tooltip=[
            alt.Tooltip('Time %', title='Time Percentage'),
            alt.Tooltip('Time', title='Time Usage')
        ]
    )
    line_time_bar = alt.layer(whole_line_time_bar, line_time_bar).properties(height=(len(df) + 1) * line_width)

    # st.markdown('# C Program Function and Line Profiling')
    line_vis, line_selector = code_line_visualize(df, line_width=line_width, code_panel_width=code_panel_width)
    line_combine = (line_time_bar.add_selection(line_selector) | line_vis)

    if use_func_barchart:
        func_time_bar = func_time_bar | circling_legend()
    else:
        func_time_bar = circling_legend()

    as_all = (func_time_bar & line_combine).configure_view(strokeOpacity=0)
    
    return as_all

if __name__ == "__main__":
    st.markdown('# Demo Line by Line CPU Usage')
    df = load_line_profile('demo.c', 'linewise_file')
    st.write(linewise_barchart(df))

