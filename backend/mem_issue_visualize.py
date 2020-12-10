from prof_file_util import load_source
from valgrind import extract_valgrind_result
import streamlit as st
import altair as alt
import pandas as pd

def mem_issue_visualize(source_path, uninitialised_buffer, invalid_write_buffer,\
    mem_leak_dic, line_width=20.0, code_panel_width=500.0):
    source_list = load_source(source_path)
    df = pd.DataFrame({'Source': source_list, 'Line Number': list(range(1, len(source_list) + 1))})
    df['Y'] = (len(df) - df['Line Number'] + 1) * line_width
    df['X'] = code_panel_width
    df['X2'] = -code_panel_width
    df['Y2'] = (len(df) - df['Line Number']) * line_width
    df['Y_mid'] = (df['Y'] + df['Y2']) / 2.0

    text_plot = alt.Chart(df).mark_text(align='left', size=line_width * 0.8).encode(
        alt.X('X2:Q', axis=None),
        alt.Y('Y_mid:Q', axis=None),
        alt.Text('Source'),
    )

    line_num_buffer  = []
    type_buffer = []
    mem_leak_bytes = []

    line_num_buffer.extend(uninitialised_buffer)
    type_buffer.extend(['uninitialized'] * len(uninitialised_buffer))
    mem_leak_bytes.extend(['not this type'] * len(uninitialised_buffer))
    line_num_buffer.extend(invalid_write_buffer)
    type_buffer.extend(['invalid write'] * len(invalid_write_buffer))
    mem_leak_bytes.extend(['not this type'] * len(invalid_write_buffer))
    line_num_buffer.extend(list(mem_leak_dic.keys()))
    type_buffer.extend(['memleak'] * len(mem_leak_dic))
    mem_leak_bytes.extend(list(mem_leak_dic.values()))

    # issue, multiple rects.
    issue_df = pd.DataFrame({'Line Number': line_num_buffer, 'Type': type_buffer, 'Leak Bytes': mem_leak_bytes})
    issue_df['Y'] = (len(df) - issue_df['Line Number'] + 1) * line_width
    issue_df['X'] = code_panel_width
    issue_df['X2'] = -code_panel_width
    issue_df['Y2'] = (len(df) - issue_df['Line Number']) * line_width
    issue_df['Y_mid'] = (issue_df['Y'] + issue_df['Y2']) / 2.0


    issue_selector = alt.binding_select(options=['uninitialized','invalid write','memleak'])

    issue_selection = alt.selection_single(fields=['Type'], bind=issue_selector, name='Choose_Memory_Issue')

    rect_plot = alt.Chart(issue_df).mark_rect(color='red').encode(
        alt.X('X:Q', axis=None),
        alt.Y('Y:Q', axis=None),
        alt.X2('X2:Q'),
        alt.Y2('Y2:Q'),
        tooltip=[alt.Tooltip('Type:N', title='Memory Issue'),
                 alt.Tooltip('Line Number:Q', title='At Line'),
                 alt.Tooltip('Leak Bytes:N', title='Leaked Memory in Bytes'),],
    ).add_selection(issue_selection).transform_filter(issue_selection)
    
    return alt.layer(rect_plot, text_plot).properties(width=code_panel_width, height=(len(df) + 1) * line_width)

if __name__ == "__main__":
    uninitialised_buffer, invalid_write_buffer = extract_valgrind_result("other", "valgrind.txt")
    
    print(uninitialised_buffer, invalid_write_buffer)
    chart = mem_issue_visualize("valgrind.c", uninitialised_buffer, invalid_write_buffer, {1:10, 7:90})
    st.write(chart)
