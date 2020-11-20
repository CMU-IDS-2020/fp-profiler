import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.title("Let's do some performance analysis!")

from prof_file_util import load_line_profile

df = load_line_profile('demo.c', 'linewise_file')
st.write(df)

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

chart = alt.hconcat(
    func_time_bar,
    line_time_bar,
)

st.write(chart)

