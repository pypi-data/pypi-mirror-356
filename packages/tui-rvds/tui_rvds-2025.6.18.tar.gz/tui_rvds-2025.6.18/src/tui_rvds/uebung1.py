import numpy as np
import pandas as pd
from checkmarkandcross import image


# TODO prüfen, ob Spalten überhaupt im df sind, um Exceptions zu vermeiden


def aufgabe1_1(df_raw: pd.DataFrame):
    if len(df_raw) != 2076 or len(df_raw.columns) != 196:
        return image(False)

    for col in df_raw.columns:
        if col not in ('lfdn', 'duration') and not col.startswith('v_'):
            return image(False)

    return image(True)


def aufgabe1_2(df: pd.DataFrame):
    if len(df) != 2076 or len(df.columns) != 196:
        return image(False)

    for col in df.columns:
        if col.startswith('v_'):
            return image(False)

    for required in ('int_techdevre1', 'meus_government1', 'act_contactpoliticans1'):
        if required not in df.columns:
            return image(False)

    return image(True)


def aufgabe2_1(df: pd.DataFrame):
    if len(df.columns) != 10:
        return image(False)

    for col in [
        'duration1',
        'age1',
        'sex1',
        'edu1',
        'federalstate1',
        'int_pol1',
        'int_enccpol1',
        'int_ccresearch1',
        'int_techdevre1',
        'int_techdevhyd1',
    ]:
        if col not in df.columns:
            return image(False)

    return image(True)


def aufgabe2_2(df: pd.DataFrame):
    for col in df.columns:
        if df[col].dtype != np.int64:
            return image(False)

    return image(True)


def aufgabe3_1(df: pd.DataFrame):
    if len(df['sex1'].unique()) != 3:
        return image(False)

    for val in [None, 1.0, 2.0]:
        if val not in df['sex1'].unique():
            return image(False)

    return image(True)


def aufgabe3_2(df: pd.DataFrame):
    if len(df['region1'].unique()) != 5:
        return image(False)

    if ((df['federalstate1'] == 5) & (df['region1'] != 'Nord')).any():
        return image(False)
    if ((df['federalstate1'] == 8) & (df['region1'] != 'Ost')).any():
        return image(False)

    return image(True)


def aufgabe3_3(df: pd.DataFrame):
    return image(len(df['age1_grp'].unique()) == 4 and None not in df['age1_grp'].unique())


def aufgabe3_4(df: pd.DataFrame):
    if len(df['edu1_grp'].unique()) != 3:
        return image(False)

    for x, y in [
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 4),
        (3, 5),
    ]:
        if len(df[(df['edu1'] == x) | (df['edu1'] == y)]['edu1_grp'].unique()) != 2:
            return image(False)

    for x, y in [
        (1, 2),
        (4, 4),
    ]:
        if len(df[(df['edu1'] == x) | (df['edu1'] == y)]['edu1_grp'].unique()) != 1:
            return image(False)

    return image(True)


def aufgabe3_5(df: pd.DataFrame):
    cols = ['int_pol1', 'int_enccpol1', 'int_ccresearch1', 'int_techdevre1', 'int_techdevhyd1']

    for col in cols:
        if col not in df.columns:
            return image(False)

    for col in cols:
        if len(df[(df[col] == 1) | (df[col] == 2)][f'{col}_grp'].unique()) != 1:
            return image(False)

        if len(df[df[col] == 3][f'{col}_grp'].unique()) != 1:
            return image(False)

        if len(df[(df[col] == 4) | (df[col] == 5)][f'{col}_grp'].unique()) != 1:
            return image(False)

        if len(df[df[col] == 99][f'{col}_grp'].unique()) != 1:
            return image(False)

        if df[f'{col}_grp'].isna().any():
            return image(False)

    return image(True)


def aufgabe4_1(df: pd.DataFrame):
    # cols
    if df.isna().all().any():
        return image(False)

    # rows
    if df.isna().all(axis=1).any():
        return image(False)

    return image(True)


def aufgabe4_2(df: pd.DataFrame):
    if df['duration1'].isna().any():
        return image(False)

    if (df['duration'] < 360).any():
        return image(False)

    if len(df) != 1907:
        return image(False)

    return image(True)


__all__ = ['aufgabe1_1', 'aufgabe1_2',
           'aufgabe2_1', 'aufgabe2_2',
           'aufgabe3_1', 'aufgabe3_2', 'aufgabe3_3', 'aufgabe3_4', 'aufgabe3_5',
           'aufgabe4_1', 'aufgabe4_2']
