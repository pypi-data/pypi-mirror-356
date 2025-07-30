# def _get_weekly_return(y_true, y_pred):
#     df = pd.concat([y_true, y_pred, stock_data[['YEARWEEK', 'STOCK', 'TARGET_1']]], join='inner', axis=1)
#     df['PRED'] += 1
#     df['TARGET'] += 1
#     return df[['YEARWEEK', 'STOCK', 'PRED', 'TARGET']].groupby(['YEARWEEK', 'STOCK']).prod().reset_index()

# def _calc_spread_return_per_week(df, portfolio_size):
#     return (df.sort_values('PRED', ascending=False)['TARGET_1'][:portfolio_size] - 1).mean()

# def sharpe_ratio_weekly(y_true, y_pred, portfolio_size:int=10):
#     df = _get_weekly_return(y_true, y_pred)
#     buf = df.groupby('YEARWEEK').apply(_calc_spread_return_per_week, portfolio_size)
#     sharpe_ratio = (buf.mean() * 52) / (buf.std() * np.sqrt(52))
#     buf += 1
#     cumulated_roi = buf.prod() - 1
#     cagr = buf.prod() ** (1 / (buf.shape[0]/52) ) - 1
#     return sharpe_ratio, cumulated_roi, cagr


def sharpe_ratio_daily(y_true, y_pred, portfolio_size: int = 10):
    df = pd.concat(
        [y_true, y_pred, stock_data[["DATE", "TARGET_1"]]], join="inner", axis=1
    )

    def _calc_spread_return_per_day(df: pd.DataFrame, portfolio_size: int):
        # print(df.sort_values('PRED', ascending=False)[['PRED', 'TARGET', 'TARGET_1']].head(10))
        return (
            df.sort_values("PRED", ascending=False)["TARGET_1"].iloc[:portfolio_size]
        ).mean()

    buf = df.groupby("DATE").apply(_calc_spread_return_per_day, portfolio_size)

    sharpe_ratio = (buf.mean() * 252) / (buf.std() * np.sqrt(252))
    buf += 1
    cumulated_roi = buf.prod() - 1
    cagr = buf.prod() ** (1 / (buf.shape[0] / 252)) - 1
    return sharpe_ratio, cumulated_roi, cagr
