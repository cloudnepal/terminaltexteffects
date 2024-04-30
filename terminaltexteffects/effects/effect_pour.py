"""Pours the characters back and forth from the top, bottom, left, or right.

Classes:
    Pour: Pours the characters back and forth from the top, bottom, left, or right.
    PourConfig: Configuration for the Pour effect.
    PourIterator: Iterates over the frames of the Pour effect. Does not normally need to be called directly.
"""

import typing
from dataclasses import dataclass
from enum import Enum, auto

import terminaltexteffects.utils.argvalidators as argvalidators
from terminaltexteffects.engine.base_character import EffectCharacter
from terminaltexteffects.engine.base_effect import BaseEffect, BaseEffectIterator
from terminaltexteffects.engine.terminal import Terminal
from terminaltexteffects.utils import easing, graphics
from terminaltexteffects.utils.argsdataclass import ArgField, ArgsDataClass, argclass
from terminaltexteffects.utils.geometry import Coord


def get_effect_and_args() -> tuple[type[typing.Any], type[ArgsDataClass]]:
    return Pour, PourConfig


@argclass(
    name="pour",
    help="Pours the characters into position from the given direction.",
    description="pour | Pours the characters into position from the given direction.",
    epilog=f"""{argvalidators.EASING_EPILOG}
Example: terminaltexteffects pour --pour-direction down --movement-speed 0.2 --gap 1 --starting-color FFFFFF --final-gradient-stops 8A008A 00D1FF FFFFFF --easing IN_QUAD""",
)
@dataclass
class PourConfig(ArgsDataClass):
    """Configuration for the Pour effect.

    Attributes:
        pour_direction (str): Direction the text will pour. Valid values are "up", "down", "left", and "right".
        pour_speed (int): Number of characters poured in per tick. Increase to speed up the effect. Valid values are n > 0.
        movement_speed (float): Movement speed of the characters. Valid values are n > 0.
        gap (int): Number of frames to wait between each character in the pour effect. Increase to slow down effect and create a more defined back and forth motion. Valid values are n >= 0.
        starting_color (graphics.Color): Color of the characters before the gradient starts.
        final_gradient_stops (tuple[graphics.Color, ...]): Tuple of colors for the character gradient. If only one color is provided, the characters will be displayed in that color.
        final_gradient_steps (tuple[int, ...]): Number of gradient steps to use. More steps will create a smoother and longer gradient animation.
        final_gradient_frames (int): Number of frames to display each gradient step.
        final_gradient_direction (graphics.Gradient.Direction): Direction of the final gradient.
        easing (typing.Callable): Easing function to use for character movement."""

    pour_direction: str = ArgField(
        cmd_name=["--pour-direction"],
        default="down",
        choices=["up", "down", "left", "right"],
        help="Direction the text will pour.",
    )  # type: ignore[assignment]
    "str : Direction the text will pour."

    pour_speed: int = ArgField(
        cmd_name="--pour-speed",
        type_parser=argvalidators.PositiveInt.type_parser,
        default=1,
        metavar=argvalidators.PositiveInt.METAVAR,
        help="Number of characters poured in per tick. Increase to speed up the effect.",
    )  # type: ignore[assignment]
    "int : Number of characters poured in per tick. Increase to speed up the effect."

    movement_speed: float = ArgField(
        cmd_name="--movement-speed",
        type_parser=argvalidators.PositiveFloat.type_parser,
        default=0.2,
        metavar=argvalidators.PositiveFloat.METAVAR,
        help="Movement speed of the characters. ",
    )  # type: ignore[assignment]
    "float : Movement speed of the characters."

    gap: int = ArgField(
        cmd_name="--gap",
        type_parser=argvalidators.NonNegativeInt.type_parser,
        default=1,
        metavar=argvalidators.NonNegativeInt.METAVAR,
        help="Number of frames to wait between each character in the pour effect. Increase to slow down effect and create a more defined back and forth motion.",
    )  # type: ignore[assignment]
    "int : Number of frames to wait between each character in the pour effect."

    starting_color: graphics.Color = ArgField(
        cmd_name=["--starting-color"],
        type_parser=argvalidators.ColorArg.type_parser,
        default="ffffff",
        metavar=argvalidators.ColorArg.METAVAR,
        help="Color of the characters before the gradient starts.",
    )  # type: ignore[assignment]
    "graphics.Color : Color of the characters before the gradient starts."

    final_gradient_stops: tuple[graphics.Color, ...] = ArgField(
        cmd_name=["--final-gradient-stops"],
        type_parser=argvalidators.ColorArg.type_parser,
        nargs="+",
        default=("8A008A", "00D1FF", "FFFFFF"),
        metavar=argvalidators.ColorArg.METAVAR,
        help="Space separated, unquoted, list of colors for the character gradient. If only one color is provided, the characters will be displayed in that color.",
    )  # type: ignore[assignment]
    "tuple[graphics.Color, ...] : Tuple of colors for the character gradient."

    final_gradient_steps: tuple[int, ...] = ArgField(
        cmd_name=["--final-gradient-steps"],
        type_parser=argvalidators.PositiveInt.type_parser,
        default=(12,),
        metavar=argvalidators.PositiveInt.METAVAR,
        help="Number of gradient steps to use. More steps will create a smoother and longer gradient animation.",
    )  # type: ignore[assignment]
    "tuple[int, ...] : Tuple of the number of gradient steps to use."

    final_gradient_frames: int = ArgField(
        cmd_name=["--final-gradient-frames"],
        type_parser=argvalidators.PositiveInt.type_parser,
        default=10,
        metavar=argvalidators.PositiveInt.METAVAR,
        help="Number of frames to display each gradient step.",
    )  # type: ignore[assignment]
    "int : Number of frames to display each gradient step."

    final_gradient_direction: graphics.Gradient.Direction = ArgField(
        cmd_name="--final-gradient-direction",
        type_parser=argvalidators.GradientDirection.type_parser,
        default=graphics.Gradient.Direction.VERTICAL,
        metavar=argvalidators.GradientDirection.METAVAR,
        help="Direction of the final gradient.",
    )  # type: ignore[assignment]
    "graphics.Gradient.Direction : Direction of the final gradient."

    movement_easing: easing.EasingFunction = ArgField(
        cmd_name="--movement-easing",
        default=easing.in_quad,
        type_parser=argvalidators.Ease.type_parser,
        help="Easing function to use for character movement.",
    )  # type: ignore[assignment]
    "easing.EasingFunction : Easing function to use for character movement."

    @classmethod
    def get_effect_class(cls):
        return Pour


class PourIterator(BaseEffectIterator[PourConfig]):
    class PourDirection(Enum):
        UP = auto()
        DOWN = auto()
        LEFT = auto()
        RIGHT = auto()

    def __init__(self, effect: "Pour") -> None:
        super().__init__(effect)
        self._pending_groups: list[list[EffectCharacter]] = []
        self._active_characters: list[EffectCharacter] = []
        self._character_final_color_map: dict[EffectCharacter, graphics.Color] = {}
        self._build()

    def _build(self) -> None:
        self._pour_direction = {
            "down": PourIterator.PourDirection.DOWN,
            "up": PourIterator.PourDirection.UP,
            "left": PourIterator.PourDirection.LEFT,
            "right": PourIterator.PourDirection.RIGHT,
        }.get(self._config.pour_direction, PourIterator.PourDirection.DOWN)
        final_gradient = graphics.Gradient(*self._config.final_gradient_stops, steps=self._config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self._terminal.output_area.top, self._terminal.output_area.right, self._config.final_gradient_direction
        )
        for character in self._terminal.get_characters():
            self._character_final_color_map[character] = final_gradient_mapping[character.input_coord]
        sort_map = {
            PourIterator.PourDirection.DOWN: Terminal.CharacterGroup.ROW_BOTTOM_TO_TOP,
            PourIterator.PourDirection.UP: Terminal.CharacterGroup.ROW_TOP_TO_BOTTOM,
            PourIterator.PourDirection.LEFT: Terminal.CharacterGroup.COLUMN_LEFT_TO_RIGHT,
            PourIterator.PourDirection.RIGHT: Terminal.CharacterGroup.COLUMN_RIGHT_TO_LEFT,
        }
        groups = self._terminal.get_characters_grouped(grouping=sort_map[self._pour_direction])
        for i, group in enumerate(groups):
            for character in group:
                self._terminal.set_character_visibility(character, False)
                if self._pour_direction == PourIterator.PourDirection.DOWN:
                    character.motion.set_coordinate(Coord(character.input_coord.column, self._terminal.output_area.top))
                elif self._pour_direction == PourIterator.PourDirection.UP:
                    character.motion.set_coordinate(
                        Coord(character.input_coord.column, self._terminal.output_area.bottom)
                    )
                elif self._pour_direction == PourIterator.PourDirection.LEFT:
                    character.motion.set_coordinate(Coord(self._terminal.output_area.right, character.input_coord.row))
                elif self._pour_direction == PourIterator.PourDirection.RIGHT:
                    character.motion.set_coordinate(Coord(self._terminal.output_area.left, character.input_coord.row))
                input_coord_path = character.motion.new_path(
                    speed=self._config.movement_speed,
                    ease=self._config.movement_easing,
                )
                input_coord_path.new_waypoint(character.input_coord)
                character.motion.activate_path(input_coord_path)

                pour_gradient = graphics.Gradient(
                    self._config.starting_color,
                    self._character_final_color_map[character],
                    steps=self._config.final_gradient_steps,
                )
                pour_scn = character.animation.new_scene()
                pour_scn.apply_gradient_to_symbols(
                    pour_gradient, character.input_symbol, self._config.final_gradient_frames
                )
                character.animation.activate_scene(pour_scn)
            if i % 2 == 0:
                self._pending_groups.append(group)
            else:
                self._pending_groups.append(group[::-1])
        self.gap = 0
        self.current_group = self._pending_groups.pop(0)

    def __next__(self) -> str:
        if self._pending_groups or self._active_characters or self.current_group:
            if not self.current_group:
                if self._pending_groups:
                    self.current_group = self._pending_groups.pop(0)
            if self.current_group:
                if not self.gap:
                    for _ in range(self._config.pour_speed):
                        if self.current_group:
                            next_character = self.current_group.pop(0)
                            self._terminal.set_character_visibility(next_character, True)
                            self._active_characters.append(next_character)
                    self.gap = self._config.gap
                else:
                    self.gap -= 1
            for character in self._active_characters:
                character.tick()
            next_frame = self._terminal.get_formatted_output_string()
            self._active_characters = [character for character in self._active_characters if character.is_active]
            return next_frame
        else:
            raise StopIteration


class Pour(BaseEffect[PourConfig]):
    """Pours the characters back and forth from the top, bottom, left, or right.

    Attributes:
        effect_config (PourConfig): Configuration for the effect.
        terminal_config (TerminalConfig): Configuration for the terminal.
    """

    _config_cls = PourConfig
    _iterator_cls = PourIterator

    def __init__(self, input_data: str) -> None:
        """Initialize the effect with the provided input data.

        Args:
            input_data (str): The input data to use for the effect."""
        super().__init__(input_data)
