# Experiments on sharpe ratio to calculate as loss or metric
class SharpeRatioTFND(tf.keras.metrics.Metric):

    def __init__(self, name="sharpe_ratio_tf_nd", **kwargs):
        super().__init__(name=name, **kwargs)
        self.sharpe_ratio = 0
        self.df = pd.DataFrame(columns=["TARGET", "PRED", "DATE", "TARGET_1"])

    # @tf.numpy_function(Tout=tf.float32)
    def update_state(self, data, y_pred, sample_weight=None):
        portfolio_size = 10

        y_true = pd.Series(data[:, 0].numpy(), index=data[:, 1].numpy(), name="TARGET")
        y_pred = pd.Series(
            y_pred.numpy().flatten(), index=data[:, 1].numpy(), name="PRED"
        )

        df = pd.concat(
            [y_true, y_pred, stock_data[["DATE", "TARGET_1"]]], join="inner", axis=1
        )
        self.df = pd.concat([self.df, df], axis=0)

        def _calc_spread_return_per_day(df: pd.DataFrame, portfolio_size: int):
            return (
                df.sort_values("PRED", ascending=False)["TARGET_1"].iloc[
                    :portfolio_size
                ]
            ).mean()

        buf = self.df.groupby("DATE").apply(_calc_spread_return_per_day, portfolio_size)

        if buf.shape[0] == 1:
            self.sharpe_ratio = buf.values[0] * (252 / np.sqrt(252))
        else:
            self.sharpe_ratio = (buf.mean() * 252) / (buf.std() * np.sqrt(252))

    def result(self):
        return self.sharpe_ratio

    def reset_states(self):
        self.sharpe_ratio = 0
        self.df = pd.DataFrame(columns=["TARGET", "PRED", "DATES", "TARGET_1"])


@tf.numpy_function(Tout=tf.float32)
def sharpe_ratio_tf_nd(data, y_pred):

    portfolio_size = 10

    y_true = pd.Series(data[:, 0], index=data[:, 1], name="TARGET")
    y_pred = pd.Series(y_pred.flatten(), index=data[:, 1], name="PRED")

    df = pd.concat(
        [y_true, y_pred, stock_data[["DATE", "TARGET_1"]]], join="inner", axis=1
    )

    print(df)

    def _calc_spread_return_per_day(df: pd.DataFrame, portfolio_size: int):
        print(
            df.sort_values("PRED", ascending=False)[
                ["PRED", "TARGET", "TARGET_1"]
            ].head(10)
        )
        return (
            df.sort_values("PRED", ascending=False)["TARGET_1"].iloc[:portfolio_size]
        ).mean()

    buf = df.groupby("DATE").apply(_calc_spread_return_per_day, portfolio_size)

    if buf.shape[0] == 1:
        sharpe_ratio = buf.values[0] * (252 / np.sqrt(252))
    else:
        sharpe_ratio = (buf.mean() * 252) / (buf.std() * np.sqrt(252))
    print(buf, sharpe_ratio)
    return sharpe_ratio


def sharpe_ratio_tf(data, y_pred):

    portfolio_size = 10
    # unscale
    y_true = data[:, 0]
    indexes = data[:, 1]

    dates = stock_data[["DATE", "TARGET_1"]].iloc[indexes]
    dates = tf.convert_to_tensor(dates)
    dates = tf.dtypes.cast(dates, tf.float32)

    y_true, y_pred = unscale_tf(y_true, y_pred)
    y_true = tf.dtypes.cast(y_true, tf.float32)
    y_pred = tf.dtypes.cast(y_pred, tf.float32)
    y_true = tf.reshape(y_true, y_pred.shape)

    # concat and sort by pred
    print(y_pred, y_true, dates)
    tensor = tf.concat([y_pred, y_true, dates], axis=1)
    tensor_ordered = tf.gather(
        tensor, tf.argsort(tensor[:, 0], direction="DESCENDING"), axis=0
    )

    # groupby and reduce with mean of 10 first elements per date groups.
    def init_func(_):
        return (0.0, 0.0)

    def reduce_func(state, value):
        print(state, value)
        if state[1] < portfolio_size:
            return (state[0] + value[3], state[1] + 1)
        else:
            return state

    def finalize_func(s, n):
        return s / n

    reducer = tf.data.experimental.Reducer(init_func, reduce_func, finalize_func)

    def key_f(row):
        print(row)
        return tf.dtypes.cast(row[2], tf.int64)

    ds_transformation_func = tf.data.experimental.group_by_reducer(
        key_func=key_f, reducer=reducer
    )
    print(tensor_ordered, tensor_ordered.shape)
    slices = tf.slice(tensor_ordered, [0, 0], [-1, -1])
    print(slices)
    ds = tf.data.Dataset.from_tensor_slices(slices)
    buf = ds.apply(ds_transformation_func)
    # ds = ds.batch(10)

    # print(ds.as_numpy_iterator())
    # iterator = iter(ds)
    # buf = iterator
    print(buf)
    # sharpe calcul
    sharpe_ratio = (K.mean(buf) * 252) / (K.std(buf) * K.sqrt(252))
    print(sharpe_ratio)
    return sharpe_ratio
