import matplotlib as plt
from matplotlib.axes import Axes
import numpy as np
import pandas as pd

from matplotlib.axes import Axes

from indicators.base import Indicator, PlotStyle, PlotPosition


class RSI(Indicator):

    plot_position = PlotPosition.under

    def __init__(
        self,
        period: int = 14,
        col: str = 'close',
    ):
        self.period = period
        self.col = col

        # кажется, это не нужно
        self.style = PlotStyle(
            color='purple',
            position=PlotPosition.under,
            levels=None,
            minmax=(0, 100),
        )

    def build(self, data: pd.DataFrame, name: str = 'rsi') -> pd.DataFrame:
        delta = data[self.col].diff()

        up = delta.copy()
        up[up < 0] = 0  # type: ignore
        up = pd.Series.ewm(up, alpha=1 / self.period).mean()

        down = delta.copy()
        down[down > 0] = 0  # type: ignore
        down *= -1
        down = pd.Series.ewm(down, alpha=1 / self.period).mean()

        rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

        result = pd.Series(np.round(rsi, 2))
        result.index = data.index

        return result.to_frame('rsi')

    @property
    def name(self) -> str:
        return f'RSI {self.period}'

    def plot(self, data: pd.DataFrame, axes: Axes) -> None:
        axes.plot(
            range(len(data['rsi'])),
            data['rsi'],
            label=self.name,
            color='purple',
        )

        axes.axhline(y=100, color='white')
        axes.axhline(y=0, color='white')

        axes.set_ylabel(self.name)
        axes.legend()
