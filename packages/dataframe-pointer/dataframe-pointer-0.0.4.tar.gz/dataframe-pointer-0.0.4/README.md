DataFrame pointer
=================

In many cases you may need an element of a pandas DataFrame to represent complex data.
Pandas supports using DataFrames as elements of DataFrames, but doing so breaks a lot of its functionality.
One way to deal with this is to place a string or other identifier as the dataframe element and have a function or dict that maps this identifier onto the data it represents.
However this makes creating new values a pain - you need to name it, create a dataframe for it, and add this dataframe to the lookup function/dict.
If making up new values for e.g. testing purposes, this adds additional steps and imports to each module.

An alternative is to create an object that contains the dataframe but is recognizable as a unique, hashable object by pandas.
dataframe_pointer does this for you using DataFrame accessors.

Simply `import dataframe_pointer` and every dataframe will now have a `.pointer()` method which returns an object that has a .df attribute which is a copy of the original dataframe.
Any two identical dataframes will have the same pointer, as in the following test case to understand what I mean:

```
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
```

`df.pointer(name)` creates a named dataframe pointer. If a pointer for an identical dataframe already exists, that pointer will be returned and not renamed.

For large dataframes this may be prohibitively inefficient, I'm planning some features to deal with those cases.

Planned future features
-----------------------

`df.pointer(name, hash=False)` will use the pointer's name to identify the pointer instead of the dataframe's contents. This will be vastly more efficient for large dataframes, but requires the user to be careful not to create pointers with the same name for multiple dataframes.
Therefore, it will raise an error if the same name is passed twice. Find a pointr by name using `df.pointer.find(name)` or `dataframe_pointer.find(name)`.

`dataframe_pointer.create_pointer(df_initializer, name)` will likewise hash a pointer by name, but can be passed a callable instead of a dataframe.
This callable will return the dataframe in question and will only be evaluated when needed, saving memory and processing time in some cases.

