import matplotlib.pyplot as mpp

# SUBPLOTS #####################################################################

class PlotContext:
    def __init__(self, rows: int, cols: int, zoom: iter=(4, 4), meta: bool=True, **kwargs) -> None:
        self._rows = rows
        self._cols = cols
        self._zoom = zoom
        self._meta = meta
        self._args = dict(kwargs)
        self._size = (zoom[0] * cols, zoom[-1] * rows)

    def __enter__(self) -> tuple:
        __figure, __axes = mpp.subplots(nrows=self._rows, ncols=self._cols, figsize=self._size, **self._args)
        # toggle the lines
        for __a in __figure.axes:
            __a.get_xaxis().set_visible(self._meta)
            __a.get_yaxis().set_visible(self._meta)
        # return to the execution env
        return (__figure, __axes)

    def __exit__(self, exc_type: any, exc_value: any, traceback: any) -> None:
        mpp.tight_layout()
        mpp.show()
