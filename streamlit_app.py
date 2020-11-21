import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.title("Let's do some performance analysis!")

from prof_file_util import load_line_profile
from linewise_visualize import code_line_visualize

with open('demo.c') as f:
    st.code(f.read(), language='c')

df = load_line_profile('demo.c', 'linewise_file')
# st.write(df)

func_time = df.groupby('Func')['Time'].sum().reset_index()
func_time = func_time[func_time['Func'] != '<not sampled>'].sort_values('Time')

func_selector = alt.selection_single(fields=['Func'])

func_time_bar = alt.Chart(func_time).mark_bar().encode(
    x=alt.X('Time:Q'),
    y=alt.Y('Func:N', sort='-x'),
).add_selection(
    func_selector
)

line_time_bar = alt.Chart(df).mark_bar().encode(
    x=alt.X('Time:Q'),
    y=alt.Y('Line Number:N'),
    tooltip=('Source'),
).transform_filter(
    func_selector
)

chart = alt.vconcat(
    func_time_bar,
    line_time_bar,
)

st.markdown('# C Program Function and Line Profiling')
chart_1 = code_line_visualize(df)
st.write((chart | chart_1).configure_view(strokeOpacity=0))

