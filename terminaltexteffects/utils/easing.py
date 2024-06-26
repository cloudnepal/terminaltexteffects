"""This module contains functions for easing calculations.

Functions:
    linear: Linear easing function.
    in_sine: Ease in using a sine function.
    out_sine: Ease out using a sine function.
    in_out_sine: Ease in/out using a sine function.
    in_quad: Ease in using a quadratic function.
    out_quad: Ease out using a quadratic function.
    in_out_quad: Ease in/out using a quadratic function.
    in_cubic: Ease in using a cubic function.
    out_cubic: Ease out using a cubic function.
    in_out_cubic: Ease in/out using a cubic function.
    in_quart: Ease in using a quartic function.
    out_quart: Ease out using a quartic function.
    in_out_quart: Ease in/out using a quartic function.
    in_quint: Ease in using a quintic function.
    out_quint: Ease out using a quintic function.
    in_out_quint: Ease in/out using a quintic function.
    in_expo: Ease in using an exponential function.
    out_expo: Ease out using an exponential function.
    in_out_expo: Ease in/out using an exponential function.
    in_circ: Ease in using a circular function.
    out_circ: Ease out using a circular function.
    in_out_circ: Ease in/out using a circular function.
    in_back: Ease in using a back function.
    out_back: Ease out using a back function.
    in_out_back: Ease in/out using a back function.
    in_elastic: Ease in using an elastic function.
    out_elastic: Ease out using an elastic function.
    in_out_elastic: Ease in/out using an elastic function.
    in_bounce: Ease in using a bounce function.
    out_bounce: Ease out using a bounce function.
    in_out_bounce: Ease in/out using a bounce function.
"""

from __future__ import annotations

import math
import typing

# EasingFunction is a type alias for a function that takes a float between 0 and 1 and returns a float between 0 and 1.
EasingFunction = typing.Callable[[float], float]
"EasingFunctions are Callable[[float], float] functions that take a float between 0 and 1 and return a float between 0 and 1."


def linear(progress_ratio: float) -> float:
    """
    Linear easing function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return progress_ratio


def in_sine(progress_ratio: float) -> float:
    """
    Ease in using a sine function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return 1 - math.cos((progress_ratio * math.pi) / 2)


def out_sine(progress_ratio: float) -> float:
    """
    Ease out using a sine function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return math.sin((progress_ratio * math.pi) / 2)


def in_out_sine(progress_ratio: float) -> float:
    """
    Ease in/out using a sine function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """

    return -(math.cos(math.pi * progress_ratio) - 1) / 2


def in_quad(progress_ratio: float) -> float:
    """
    Ease in using a quadratic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """

    return progress_ratio**2


def out_quad(progress_ratio: float) -> float:
    """
    Ease out using a quadratic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value

    """
    return 1 - (1 - progress_ratio) * (1 - progress_ratio)


def in_out_quad(progress_ratio: float) -> float:
    """
    Ease in/out using a quadratic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value

    """
    if progress_ratio < 0.5:
        return 2 * progress_ratio**2
    else:
        return 1 - (-2 * progress_ratio + 2) ** 2 / 2


def in_cubic(progress_ratio: float) -> float:
    """
    Ease in using a cubic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return progress_ratio**3


def out_cubic(progress_ratio: float) -> float:
    """
    Ease out using a cubic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return 1 - (1 - progress_ratio) ** 3


def in_out_cubic(progress_ratio: float) -> float:
    """
    Ease in/out using a cubic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 representing the percentage of the current waypoint speed to apply to the
        character
    """
    if progress_ratio < 0.5:
        return 4 * progress_ratio**3
    else:
        return 1 - (-2 * progress_ratio + 2) ** 3 / 2


def in_quart(progress_ratio: float) -> float:
    """
    Ease in using a quartic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 representing the percentage
        of the current waypoint speed to apply to the character
    """
    return progress_ratio**4


def out_quart(progress_ratio: float) -> float:
    """
    Ease out using a quartic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return 1 - (1 - progress_ratio) ** 4


def in_out_quart(progress_ratio: float) -> float:
    """
    Ease in/out using a quartic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    if progress_ratio < 0.5:
        return 8 * progress_ratio**4
    else:
        return 1 - (-2 * progress_ratio + 2) ** 4 / 2


def in_quint(progress_ratio: float) -> float:
    """
    Ease in using a quintic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return progress_ratio**5


def out_quint(progress_ratio: float) -> float:
    """
    Ease out using a quintic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return 1 - (1 - progress_ratio) ** 5


def in_out_quint(progress_ratio: float) -> float:
    """
    Ease in/out using a quintic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    if progress_ratio < 0.5:
        return 16 * progress_ratio**5
    else:
        return 1 - (-2 * progress_ratio + 2) ** 5 / 2


def in_expo(progress_ratio: float) -> float:
    """
    Ease in using an exponential function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    if progress_ratio == 0:
        return 0
    else:
        return 2 ** (10 * progress_ratio - 10)


def out_expo(progress_ratio: float) -> float:
    """
    Ease out using an exponential function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    if progress_ratio == 1:
        return 1
    else:
        return 1 - 2 ** (-10 * progress_ratio)


def in_out_expo(progress_ratio: float) -> float:
    """
    Ease in/out using an exponential function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    if progress_ratio == 0:
        return 0
    elif progress_ratio == 1:
        return 1
    elif progress_ratio < 0.5:
        return 2 ** (20 * progress_ratio - 10) / 2
    else:
        return (2 - 2 ** (-20 * progress_ratio + 10)) / 2


def in_circ(progress_ratio: float) -> float:
    """
    Ease in using a circular function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return 1 - math.sqrt(1 - progress_ratio**2)


def out_circ(progress_ratio: float) -> float:
    """
    Ease out using a circular function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    return math.sqrt(1 - (progress_ratio - 1) ** 2)


def in_out_circ(progress_ratio: float) -> float:
    """
    Ease in/out using a circular function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    if progress_ratio < 0.5:
        return (1 - math.sqrt(1 - (2 * progress_ratio) ** 2)) / 2
    else:
        return (math.sqrt(1 - (-2 * progress_ratio + 2) ** 2) + 1) / 2


def in_back(progress_ratio: float) -> float:
    """
    Ease in using a back function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * progress_ratio**3 - c1 * progress_ratio**2


def out_back(progress_ratio: float) -> float:
    """
    Ease out using a back function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (progress_ratio - 1) ** 3 + c1 * (progress_ratio - 1) ** 2


def in_out_back(progress_ratio: float) -> float:
    """
    Ease in/out using a back function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    c1 = 1.70158
    c2 = c1 * 1.525
    if progress_ratio < 0.5:
        return ((2 * progress_ratio) ** 2 * ((c2 + 1) * 2 * progress_ratio - c2)) / 2
    else:
        return ((2 * progress_ratio - 2) ** 2 * ((c2 + 1) * (progress_ratio * 2 - 2) + c2) + 2) / 2


def in_elastic(progress_ratio: float) -> float:
    """
    Ease in using an elastic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """

    c4 = (2 * math.pi) / 3
    if progress_ratio == 0:
        return 0
    elif progress_ratio == 1:
        return 1
    else:
        return -(2 ** (10 * progress_ratio - 10)) * math.sin((progress_ratio * 10 - 10.75) * c4)


def out_elastic(progress_ratio: float) -> float:
    """
    Ease out using an elastic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 representing the percentage of the current waypoint speed to apply to the character
    """
    c4 = (2 * math.pi) / 3
    if progress_ratio == 0:
        return 0
    elif progress_ratio == 1:
        return 1
    else:
        return 2 ** (-10 * progress_ratio) * math.sin((progress_ratio * 10 - 0.75) * c4) + 1


def in_out_elastic(progress_ratio: float) -> float:
    """
    Ease in/out using an elastic function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 representing the percentage of the current waypoint speed to apply to the character
    """
    c5 = (2 * math.pi) / 4.5
    if progress_ratio == 0:
        return 0
    elif progress_ratio == 1:
        return 1
    elif progress_ratio < 0.5:
        return -(2 ** (20 * progress_ratio - 10) * math.sin((20 * progress_ratio - 11.125) * c5)) / 2
    else:
        return (2 ** (-20 * progress_ratio + 10) * math.sin((20 * progress_ratio - 11.125) * c5)) / 2 + 1


def in_bounce(progress_ratio: float) -> float:
    """
    Ease in using a bounce function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 representing the percentage of the current waypoint speed to apply to the character
    """
    return 1 - out_bounce(1 - progress_ratio)


def out_bounce(progress_ratio: float) -> float:
    """
    Ease out using a bounce function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    n1 = 7.5625
    d1 = 2.75
    if progress_ratio < 1 / d1:
        return n1 * progress_ratio**2
    elif progress_ratio < 2 / d1:
        return n1 * (progress_ratio - 1.5 / d1) ** 2 + 0.75
    elif progress_ratio < 2.5 / d1:
        return n1 * (progress_ratio - 2.25 / d1) ** 2 + 0.9375
    else:
        return n1 * (progress_ratio - 2.625 / d1) ** 2 + 0.984375


def in_out_bounce(progress_ratio: float) -> float:
    """
    Ease in/out using a bounce function.

    Args:
        progress_ratio (float): the ratio of the current step to the maximum steps

    Returns:
        float: 0 <= n <= 1 eased value
    """
    if progress_ratio < 0.5:
        return (1 - out_bounce(1 - 2 * progress_ratio)) / 2
    else:
        return (1 + out_bounce(2 * progress_ratio - 1)) / 2
