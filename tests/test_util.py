import os

import pandas as pd
import pickle
import pytest

from sports_stats.utils import util


@pytest.fixture()
def result_df():
    with open('tests/resources/JoshAllenGames.pkl', 'rb') as f:
        return pickle.load(f)


@pytest.fixture()
def result_cleaned_columns():
    return [
        'Misc_Date', 'Misc_Team', 'Misc_Opp', 'Misc_Result', 'Passing_Cmp',
        'Passing_Att', 'Passing_Cmp%', 'Passing_Yds', 'Passing_TD',
        'Passing_TD%', 'Passing_Int', 'Passing_Int%', 'Passing_Lng',
        'Passing_Y/A', 'Passing_AY/A', 'Passing_Y/C', 'Passing_Rate',
        'Passing_Sk', 'Passing_Yds.1', 'Passing_Sk%', 'Passing_NY/A',
        'Passing_ANY/A', 'Rushing_Att', 'Rushing_Yds', 'Rushing_TD',
        'Rushing_Lng', 'Rushing_Y/A', 'Misc_Fmb', 'player_Id'
    ]


def test_to_int_pos():
    """Sample pytest test function with the pytest fixture as an argument."""
    assert 7 == util.to_int('7')


def test_to_int_raises():
    with pytest.raises(ValueError, match='Value ".*" cannot be coerced to type integer.'):
        util.to_int('non-integer-fiable string')


def test_table_with_result_clean(result_df, result_cleaned_columns):
    cleaned_df = util.clean_table(result_df, post=True)
    assert list(cleaned_df.columns) == result_cleaned_columns
