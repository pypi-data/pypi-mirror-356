import pandas as pd

from matplotlib.axes import Axes

from .base import Indicator, PlotPosition
from .rsi import RSI

class StochasticRSI(Indicator):

    plot_position = PlotPosition.under

    def __init__(self, period: int = 14, k: int = 3, d: int = 3, col: str = 'close'):
        self.period = period
        self.k = k
        self.d = d
        self.col = col

    def build(self, data: pd.DataFrame) -> pd.DataFrame:
        rsi = RSI(self.period).build(data)
        stochastic_rsi = (
            100
            * (rsi - rsi.rolling(self.period).min())
            / (rsi.rolling(self.period).max() - rsi.rolling(self.period).min())
        )

        k_values = stochastic_rsi.rolling(self.k).mean()

        result = pd.Series(k_values.rolling(self.d).mean()['rsi'])
        result.index = data.index

        return result.to_frame('stoch_rsi')

    @property
    def name(self) -> str:
        return f'StochRSI {self.d} {self.k}'

    def plot(self, data: pd.DataFrame, axes: Axes) -> None:
        axes.plot(
            range(len(data['stoch_rsi'])),
            data['stoch_rsi'],
            label=self.name,
            color='blue',
        )

        axes.axhline(y=100, color='white')
        axes.axhline(y=0, color='white')
        axes.axhline(y=80, color='gray', linestyle='--', linewidth=0.9)
        axes.axhline(y=20, color='gray', linestyle='--', linewidth=0.9)

        axes.set_ylabel(self.name)
        axes.legend()
