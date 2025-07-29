import pandas as pd
import dataframe_pointer


def test_df_pointer_differs_by_df():
    df1 = pd.DataFrame({'a': range(1000)})
    df2 = pd.DataFrame({'a': range(200)})
    df3 = pd.DataFrame({'1234': range(4000)})
    point1 = df1.pointer()
    point2 = df2.pointer()
    point3 = df3.pointer()
    pd.testing.assert_frame_equal(point1.df, df1)
    assert point1 != point2
    assert point2 != point3
    assert point1 != point3
    assert point1 == df1.pointer()
    assert point1 == df1.copy().pointer()


def test_repr_is_unique_and_consistent():
    df1 = pd.DataFrame({'a': range(1000)})
    df2 = pd.DataFrame({'a': range(200)})
    rep1 =  repr(df1.pointer())
    rep2 = repr(df2.pointer())
    assert rep1 != rep2
    assert rep1 == "dataframe pointer: 4d3bd387f6bb937ec791c7bf31b82a45fd56e2da2cbdd98a65ab9439355bd895"
    dataframe_pointer.df_pointers = {}
    assert rep1 == repr(df1.pointer())
    assert rep2 == repr(df2.pointer())