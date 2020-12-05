from prof_file_util import load_line_profile
import streamlit as st
import altair as alt
import pandas as pd

def code_line_visualize(df, line_width=20.0, code_panel_width=500.0):
    '''
    Data Frame()
    'Line Number': line_numbers,
    'Source': code_lines,
    'Time %': time_percentage,
    'Time': self_seconds,
    'Func': func_names
    '''
    df['Y'] = (len(df) - df['Line Number']) * line_width
    df['X'] = code_panel_width
    df['X2'] = 0.0
    df['Source'] = df['Line Number'].astype(str) + '\t\t' + df['Source']
    rect_plot = alt.Chart(df).mark_bar(color=alt.Value('red')).encode(
        alt.X('X:Q', axis=None),
        alt.Y('Line Number:O', axis=None),
        alt.Opacity('Time %:Q', scale=alt.Scale(type='log',\
            domain=(1, 100), range=(0,1))),
        tooltip=[
            alt.Tooltip('Time %', title='Time Percentage'),
            alt.Tooltip('Time', title='Time Usage')
        ]
    ).properties(width=code_panel_width,\
        height=line_width * len(df))

    text_plot = alt.Chart(df).mark_text(align='left', size=line_width * 0.8).encode(
        alt.X('X2:Q', type='quantitative', axis=None),
        alt.Y('Line Number:O', axis=None),
        alt.Text('Source'),
        tooltip=[
            alt.Tooltip('Time %', title='Time Percentage'),
            alt.Tooltip('Time', title='Time Usage')
        ]
    ).properties(width=code_panel_width,\
        height=line_width * len(df))

    # st.write(alt.layer(rect_plot, text_plot).configure_view(strokeOpacity=0))
    return alt.layer(rect_plot, text_plot)

if __name__ == "__main__":
    st.markdown('# Demo Line by Line CPU Usage')
    df = load_line_profile('demo.c', 'linewise_file')
    code_line_visualize(df)
