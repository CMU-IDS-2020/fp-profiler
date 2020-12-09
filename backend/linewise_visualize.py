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
    df['Y'] = (len(df) - df['Line Number'] + 1) * line_width
    df['X'] = code_panel_width
    df['X2'] = 0.0
    df['Y2'] = (len(df) - df['Line Number']) * line_width
    df['Y_mid'] = (df['Y'] + df['Y2']) / 2.0
    
    rect_plot = alt.Chart(df).mark_rect(color=alt.Value('red')).encode(
        alt.X('X:Q', axis=None),
        alt.Y('Y:Q', axis=None),
        alt.X2('X2:Q'),
        alt.Y2('Y2:Q'),
        alt.Opacity('Time %:Q', scale=alt.Scale(type='log',\
            domain=(1, 100), range=(0,1))),
        tooltip=[
            alt.Tooltip('Time %', title='Time Percentage'),
            alt.Tooltip('Time', title='Time Usage')
        ]
    )

    # aggregate the functions to form the whole rect plot and single rect plot,
    # for frame line highlight
    func_block_agg_df = df.groupby('Func').agg({'Line Number': ['min', 'max']}).reset_index()
    func_block_agg_df = func_block_agg_df[func_block_agg_df['Func'] != '<not sampled>']
    func_block_agg_df = func_block_agg_df.rename(columns={'': 'Func',\
        'min': 'minLine', 'max': 'maxLine'})
    func_block_agg_df.columns = func_block_agg_df.columns.droplevel(0)
    func_block_agg_df['Y1'] = (len(df) - func_block_agg_df['maxLine']) * line_width
    func_block_agg_df['Y2'] = (len(df) - func_block_agg_df['minLine'] + 1) * line_width
    func_block_agg_df['Y3'] = (len(df) - func_block_agg_df['minLine']) * line_width
    func_block_agg_df['X1'] = 0.0
    func_block_agg_df['X2'] = code_panel_width
    # whole block frame
    rect_whole_plot = alt.Chart(func_block_agg_df).mark_rect(filled=False).encode(
        alt.Y('Y2:Q', axis=None),
        alt.Y2('Y1:Q'),
        alt.X('X2:Q', axis=None),
        alt.X2('X1:Q'),
        color=alt.value('red'),
        opacity=alt.value(0),
        strokeWidth = alt.value(3),
    )
    #single block frame
    rect_single_plot = alt.Chart(func_block_agg_df).mark_rect(filled=False).encode(
        alt.Y('Y3:Q', axis=None),
        alt.Y2('Y2:Q'),
        alt.X('X2:Q', axis=None),
        alt.X2('X1:Q'),
        color=alt.value('green'),
        opacity=alt.value(0),
        strokeWidth = alt.value(3),
    )
    
    text_plot = alt.Chart(df).mark_text(align='left', size=line_width * 0.8).encode(
        alt.X('X2:Q', axis=None),
        alt.Y('Y_mid:Q', axis=None),
        alt.Text('Source'),
        tooltip=[
            alt.Tooltip('Time %', title='Time Percentage'),
            alt.Tooltip('Time', title='Time Usage')
        ]
    )

    # trans layer for colored highlight, adding selection.
    line_selector = alt.selection_single(on='mouseover', fields=['Line Number'], empty='none')
    transparent_plot = alt.Chart(df).mark_rect(color=alt.Value('blue'), filled=False).encode(
        alt.X('X:Q', axis=None),
        alt.Y('Y:Q', axis=None),
        alt.X2('X2:Q'),
        alt.Y2('Y2:Q'),
        strokeOpacity=alt.condition(line_selector, alt.value(1), alt.value(0)),
        strokeWidth = alt.value(2),
    )

    # transparent layer for selection
    selection_layer = alt.Chart(df).mark_rect().encode(
        alt.X('X:Q', axis=None),
        alt.Y('Y:Q', axis=None),
        alt.X2('X2:Q'),
        alt.Y2('Y2:Q'),
        opacity=alt.value(0),
        tooltip=[
            alt.Tooltip('Time %', title='Time Percentage'),
            alt.Tooltip('Time', title='Time Usage')
        ]
    ).add_selection(line_selector)


    # st.write(alt.layer(rect_plot, text_plot).configure_view(strokeOpacity=0))
    return alt.layer(rect_plot, rect_whole_plot, rect_single_plot, text_plot,\
        transparent_plot, selection_layer,).properties(width=code_panel_width, height=(len(df) + 1) * line_width), line_selector

if __name__ == "__main__":
    st.markdown('# Demo Line by Line CPU Usage')
    df = load_line_profile('demo.c', 'linewise_file')
    st.write(code_line_visualize(df)[0])
