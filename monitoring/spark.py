# -*- coding: utf-8 -*-

"""
spark.py
~~~~~~~~

A port of @holman's spark project for Python.
"""

import sys

ticks = u'_▁▂▃▄▅▆▇█'


def spark_string(ints, fit_min=False):
    """Returns a spark string from given iterable of ints.

    Keyword Arguments:
    fit_min: Matches the range of the sparkline to the input integers
             rather than the default of zero. Useful for large numbers with
             relatively small differences between the positions
    """
    min_range = min(ints) if fit_min else 0
    step_range = max(ints) - min_range
    step = (step_range / float(len(ticks) - 1)) or 1
    return u''.join(ticks[int(round((i - min_range) / step))] for i in ints)


def spark_print(ints, stream=None, fit_min=False):
    """Prints spark to given stream."""
    if stream is None:
        stream = sys.stdout
    stream.write(spark_string(ints, fit_min=fit_min))
