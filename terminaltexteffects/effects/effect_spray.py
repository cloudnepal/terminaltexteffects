"""Sprays the characters from a single point.

Classes:
    Spray: Sprays the characters from a single point.
    SprayConfig: Configuration for the Spray effect.
    SprayIterator: Iterates over the effect. Does not normally need to be called directly.
"""

from __future__ import annotations

import random
import typing
from dataclasses import dataclass
from enum import Enum, auto

import terminaltexteffects.utils.argvalidators as argvalidators
from terminaltexteffects.engine.base_character import EffectCharacter, EventHandler
from terminaltexteffects.engine.base_effect import BaseEffect, BaseEffectIterator
from terminaltexteffects.utils import easing
from terminaltexteffects.utils.argsdataclass import ArgField, ArgsDataClass, argclass
from terminaltexteffects.utils.geometry import Coord
from terminaltexteffects.utils.graphics import Color, Gradient


def get_effect_and_args() -> tuple[type[typing.Any], type[ArgsDataClass]]:
    return Spray, SprayConfig


@argclass(
    name="spray",
    help="Draws the characters spawning at varying rates from a single point.",
    description="spray | Draws the characters spawning at varying rates from a single point.",
    epilog=f"""{argvalidators.EASING_EPILOG}    
Example: terminaltexteffects spray --final-gradient-stops 8A008A 00D1FF FFFFFF --final-gradient-steps 12 --spray-position e --spray-volume 0.005 --movement-speed 0.4-1.0 --movement-easing OUT_EXPO""",
)
@dataclass
class SprayConfig(ArgsDataClass):
    """Configuration for the Spray effect.

    Attributes:
        final_gradient_stops (tuple[Color, ...]): Tuple of colors for the final color gradient. If only one color is provided, the characters will be displayed in that color.
        final_gradient_steps (tuple[int, ...] | int): Tuple of the number of gradient steps to use. More steps will create a smoother and longer gradient animation. Valid values are n > 0.
        final_gradient_direction (Gradient.Direction): Direction of the final gradient.
        spray_position (typing.Literal["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"]): Position for the spray origin. Valid values are n, ne, e, se, s, sw, w, nw, center.
        spray_volume (float): Number of characters to spray per tick as a percent of the total number of characters. Valid values are 0 < n <= 1.
        movement_speed (tuple[float, float]): Movement speed of the characters. Valid values are n > 0.
        movement_easing (easing.EasingFunction): Easing function to use for character movement."""

    final_gradient_stops: tuple[Color, ...] = ArgField(
        cmd_name=["--final-gradient-stops"],
        type_parser=argvalidators.ColorArg.type_parser,
        nargs="+",
        default=(Color("8A008A"), Color("00D1FF"), Color("FFFFFF")),
        metavar=argvalidators.ColorArg.METAVAR,
        help="Space separated, unquoted, list of colors for the character gradient (applied from bottom to top). If only one color is provided, the characters will be displayed in that color.",
    )  # type: ignore[assignment]
    "tuple[Color, ...] : Tuple of colors for the final color gradient. If only one color is provided, the characters will be displayed in that color."

    final_gradient_steps: tuple[int, ...] | int = ArgField(
        cmd_name=["--final-gradient-steps"],
        type_parser=argvalidators.PositiveInt.type_parser,
        nargs="+",
        default=12,
        metavar=argvalidators.PositiveInt.METAVAR,
        help="Space separated, unquoted, list of the number of gradient steps to use. More steps will create a smoother and longer gradient animation.",
    )  # type: ignore[assignment]
    "tuple[int, ...] | int : Int or Tuple of ints for the number of gradient steps to use. More steps will create a smoother and longer gradient animation."

    final_gradient_direction: Gradient.Direction = ArgField(
        cmd_name="--final-gradient-direction",
        type_parser=argvalidators.GradientDirection.type_parser,
        default=Gradient.Direction.VERTICAL,
        metavar=argvalidators.GradientDirection.METAVAR,
        help="Direction of the final gradient.",
    )  # type: ignore[assignment]
    "Gradient.Direction : Direction of the final gradient."

    spray_position: typing.Literal["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"] = ArgField(
        cmd_name="--spray-position",
        choices=["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"],
        default="e",
        help="Position for the spray origin.",
    )  # type: ignore[assignment]
    "typing.Literal['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'] : Position for the spray origin."

    spray_volume: float = ArgField(
        cmd_name="--spray-volume",
        type_parser=argvalidators.PositiveFloat.type_parser,
        default=0.005,
        metavar=argvalidators.PositiveFloat.METAVAR,
        help="Number of characters to spray per tick as a percent of the total number of characters.",
    )  # type: ignore[assignment]
    "float : Number of characters to spray per tick as a percent of the total number of characters."

    movement_speed: tuple[float, float] = ArgField(
        cmd_name="--movement-speed",
        type_parser=argvalidators.PositiveFloatRange.type_parser,
        default=(0.4, 1.0),
        metavar=argvalidators.PositiveFloatRange.METAVAR,
        help="Movement speed of the characters.",
    )  # type: ignore[assignment]
    "tuple[float, float] : Movement speed of the characters."

    movement_easing: easing.EasingFunction = ArgField(
        cmd_name="--movement-easing",
        type_parser=argvalidators.Ease.type_parser,
        default=easing.out_expo,
        help="Easing function to use for character movement.",
    )  # type: ignore[assignment]
    "easing.EasingFunction : Easing function to use for character movement."

    @classmethod
    def get_effect_class(cls):
        return Spray


class SprayIterator(BaseEffectIterator[SprayConfig]):
    class SprayPosition(Enum):
        N = auto()
        NE = auto()
        E = auto()
        SE = auto()
        S = auto()
        SW = auto()
        W = auto()
        NW = auto()
        CENTER = auto()

    def __init__(self, effect: "Spray") -> None:
        super().__init__(effect)
        self.pending_chars: list[EffectCharacter] = []
        self.character_final_color_map: dict[EffectCharacter, Color] = {}
        self.build()

    def build(self) -> None:
        self._spray_position = {
            "n": SprayIterator.SprayPosition.N,
            "ne": SprayIterator.SprayPosition.NE,
            "e": SprayIterator.SprayPosition.E,
            "se": SprayIterator.SprayPosition.SE,
            "s": SprayIterator.SprayPosition.S,
            "sw": SprayIterator.SprayPosition.SW,
            "w": SprayIterator.SprayPosition.W,
            "nw": SprayIterator.SprayPosition.NW,
            "center": SprayIterator.SprayPosition.CENTER,
        }.get(self.config.spray_position, SprayIterator.SprayPosition.E)
        final_gradient = Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.canvas.top, self.terminal.canvas.right, self.config.final_gradient_direction
        )
        for character in self.terminal.get_characters():
            self.character_final_color_map[character] = final_gradient_mapping[character.input_coord]
        spray_origin_map = {
            SprayIterator.SprayPosition.CENTER: (self.terminal.canvas.center),
            SprayIterator.SprayPosition.N: Coord(self.terminal.canvas.right // 2, self.terminal.canvas.top),
            SprayIterator.SprayPosition.NW: Coord(self.terminal.canvas.left, self.terminal.canvas.top),
            SprayIterator.SprayPosition.W: Coord(self.terminal.canvas.left, self.terminal.canvas.top // 2),
            SprayIterator.SprayPosition.SW: Coord(self.terminal.canvas.left, self.terminal.canvas.bottom),
            SprayIterator.SprayPosition.S: Coord(self.terminal.canvas.right // 2, self.terminal.canvas.bottom),
            SprayIterator.SprayPosition.SE: Coord(self.terminal.canvas.right - 1, self.terminal.canvas.bottom),
            SprayIterator.SprayPosition.E: Coord(self.terminal.canvas.right - 1, self.terminal.canvas.top // 2),
            SprayIterator.SprayPosition.NE: Coord(self.terminal.canvas.right - 1, self.terminal.canvas.top),
        }

        for character in self.terminal.get_characters():
            character.motion.set_coordinate(spray_origin_map[self._spray_position])
            input_coord_path = character.motion.new_path(
                speed=random.uniform(self.config.movement_speed[0], self.config.movement_speed[1]),
                ease=self.config.movement_easing,
            )
            input_coord_path.new_waypoint(character.input_coord)
            character.event_handler.register_event(
                EventHandler.Event.PATH_ACTIVATED, input_coord_path, EventHandler.Action.SET_LAYER, 1
            )
            character.event_handler.register_event(
                EventHandler.Event.PATH_COMPLETE, input_coord_path, EventHandler.Action.SET_LAYER, 0
            )
            droplet_scn = character.animation.new_scene()
            spray_gradient = Gradient(
                random.choice(final_gradient.spectrum), self.character_final_color_map[character], steps=7
            )
            droplet_scn.apply_gradient_to_symbols(spray_gradient, character.input_symbol, 20)
            character.animation.activate_scene(droplet_scn)
            character.motion.activate_path(input_coord_path)
            self.pending_chars.append(character)
        random.shuffle(self.pending_chars)
        self._volume = max(int(len(self.pending_chars) * self.config.spray_volume), 1)

    def __next__(self) -> str:
        if self.pending_chars or self.active_characters:
            if self.pending_chars:
                for _ in range(random.randint(1, self._volume)):
                    if self.pending_chars:
                        next_character = self.pending_chars.pop()
                        self.terminal.set_character_visibility(next_character, True)
                        self.active_characters.append(next_character)

            self.update()
            return self.frame
        else:
            raise StopIteration


class Spray(BaseEffect[SprayConfig]):
    """Sprays the characters from a single point.

    Attributes:
        effect_config (SprayConfig): Configuration for the effect.
        terminal_config (TerminalConfig): Configuration for the terminal.
    """

    _config_cls = SprayConfig
    _iterator_cls = SprayIterator

    def __init__(self, input_data: str) -> None:
        """Initialize the effect with the provided input data.

        Args:
            input_data (str): The input data to use for the effect."""
        super().__init__(input_data)
