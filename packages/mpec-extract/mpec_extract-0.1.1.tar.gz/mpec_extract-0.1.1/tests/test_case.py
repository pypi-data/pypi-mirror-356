import sys
import os

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from mpec_extract import extract_end_to_end  # will look like an import error, but should be fine if src is in syspath

import pandas as pd


def create_outputs_to_extract_df(save_to_csv=False):
    import pandas as pd

    # Create the data frame from the CSV data
    data = {
        'Output': ['Overall', 'Monthly', 'Monthly', 'Monthly', 'Monthly ', 'Monthly ', 'Monthly ', 'Monthly ',
                   'Monthly', 'Monthly ', 'Monthly ', 'Monthly ', 'Monthly '],

        'Label': ['Initial Dist CD4 VHI', 'Transmission', 'HIV+undetected', 'HIV+unlinked', 'HIV+incare', 'HIV+LTFU',
                  'HIV+RTC', 'CHRM7_Death', 'PWH_Deaths_HIV+undetected', 'PWH_Deaths_HIV+unlinked',
                  'PWH_Deaths_HIV+incare', 'PWH_Deaths_HIV+LTFU ', 'PWH_Deaths_HIV+RTC'],

        'Section': ['INITIAL DISTRIBUTIONS', '', '', '', '', '', '', '', '', '', '', '', ''],

        'TextID': ['CD4 Count Level', 'Self Transmission Rate Multiplier', '#Alive', '#Alive', '#Alive', '#Alive',
                   '#Alive', 'Total Dths w. CHRM6', 'Age-Stratified Outputs', 'Age-Stratified Outputs',
                   'Age-Stratified Outputs', 'Age-Stratified Outputs', 'Age-Stratified Outputs'],

        'RowOffset': [1, 2, 2, 3, 4, 5, 6, 6, 4, 6, 8, 10, 12],
        'ColLetter': ['C', 'J', 'C', 'C', 'C', 'C', 'C', 'AF', 'Q', 'Q', 'Q', 'Q', 'Q'],
        'Months': ['', '1-5', '1-10', '1, 2, 3', '1, 2, 4', '1, 2, 5', '1, 2, 6', '1, 2, 7', '1, 2, 8', '1, 2, 9',
                   '1, 2, 10', '1, 2, 11', '1, 2, 12']
    }

    df = pd.DataFrame(data)

    # optional, save  as a csv file:
    if save_to_csv:
        df.to_csv('output_data.csv', index=False)

    return df


def write_single_output_to_csv(result, output_label, filepath):
    import pandas as pd

    rows = []
    for month, run_dict in result.get(output_label, {}).items():
        for run_name, value in run_dict.items():
            rows.append({
                "run_name": run_name,
                "month": month,
                "value": value
            })

    df = pd.DataFrame(rows)
    df.to_csv(filepath, index=False)


def is_equal_monthly_vs_gui_output(lib_df, gui_df):
    """
    :param lib_df: has columns: output, mth, run, val
    :param gui_df: index is "Month {i} {output}", columns are runs
    :return:
    """

    # look at monthly outputs only
    gui_df = gui_df[gui_df.index.str.startswith("Month")]

    # reformat gui_df to match lib_df structure
    # bring gui's "Month {i} {output}" into a column
    gui_df_reset = gui_df.reset_index().melt(id_vars=['index'], var_name='run', value_name='val')
    gui_df_reset[['mth_str', 'output']] = gui_df_reset['index'].str.extract(r'Month (\d+)\s+(.+)')
    gui_df_reset['mth'] = gui_df_reset['mth_str'].astype(int)
    gui_df_reset = gui_df_reset.drop(columns=['index', 'mth_str'])

    # rearranged to same column order as lib_df
    gui_df_reorder = gui_df_reset[['output', 'mth', 'run', 'val']]

    # convert val to float
    lib_df['val'] = lib_df['val'].astype(float)
    gui_df_reorder['val'] = gui_df_reorder['val'].astype(float)

    # sort both dfs
    lib_df_sorted = lib_df.sort_values(by=['output', 'mth', 'run']).reset_index(drop=True)
    gui_df_sorted = gui_df_reorder.sort_values(by=['output', 'mth', 'run']).reset_index(drop=True)

    # compare
    are_equal = lib_df_sorted.equals(gui_df_sorted)
    print("Are the outputs equal?", are_equal)

    if not are_equal:
        lib_df_sorted.to_csv("debug_lib_df_sorted.csv")
        gui_df_sorted.to_csv("debug_gui_df_sorted.csv")

    return are_equal


def run_extraction():

    data_filepath = r"./50d_new.out_data"
    all_outfiles_dir = r"./20plus_outfiles"
    desired_outputs = create_outputs_to_extract_df()

    # extract overall outputs
    extract_end_to_end(data_filepath, desired_outputs, all_outfiles_dir, overall=True,
                       save_as_csv='./df_to_csv_overall_python.csv')

    # extract monthly outputs
    mth_out = extract_end_to_end(data_filepath, desired_outputs, all_outfiles_dir,
                                 monthly=True, save_as_csv='./mth_outputs.csv')

    write_single_output_to_csv(mth_out, "CHRM7_Death", "./dict_to_csv_mth_python.csv")


def test_monthly_extract_is_wrong():

    lib_df = pd.read_csv('./mth_outputs_wrong.csv')  # has columns: output, mth, run, val
    gui_df = pd.read_csv('./20plus_mct_out.extract_out', index_col=0, sep='\t')  # index is "Month {i} {output}", columns are runs

    assert not is_equal_monthly_vs_gui_output(lib_df, gui_df)


def test_monthly_extract():

    run_extraction()

    lib_df = pd.read_csv('./mth_outputs.csv')  # has columns: output, mth, run, val
    gui_df = pd.read_csv('./20plus_mct_out.extract_out', index_col=0, sep='\t')  # index is "Month {i} {output}", columns are runs

    assert is_equal_monthly_vs_gui_output(lib_df, gui_df)






