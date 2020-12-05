import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# st.title("Let's do some performance analysis!")
from prof_file_util import load_line_profile
from linewise_visualize import code_line_visualize


def linewise_barchart(df, line_width=20.0, code_panel_width=500.0):
    
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
        x=alt.X('Time:Q'),
        y=alt.Y('Line Number:N'),
    ).transform_filter(
        func_selector
    )

    # Add a grey back ground 
    whole_line_time_bar = alt.Chart(df).mark_bar().encode(
        x=alt.X('Time:Q'),
        y=alt.Y('Line Number:N'),
        color=alt.value('lightgrey'),
        tooltip=[
            alt.Tooltip('Time %', title='Time Percentage'),
            alt.Tooltip('Time', title='Time Usage')
        ]
    )
    line_time_bar = alt.layer(whole_line_time_bar, line_time_bar).properties(height=line_width * len(df))

    # st.markdown('# C Program Function and Line Profiling')
    line_vis = code_line_visualize(df, line_width=line_width, code_panel_width=code_panel_width)
    line_combine = (line_time_bar | line_vis)

    as_all = (func_time_bar & line_combine).configure_view(strokeOpacity=0)
    
    return as_all

if __name__ == "__main__":
    st.markdown('# Demo Line by Line CPU Usage')
    df = load_line_profile('demo.c', 'linewise_file')
    st.write(linewise_barchart(df))

