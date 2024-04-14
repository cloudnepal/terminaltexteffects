import random
import typing
from collections.abc import Iterator
from dataclasses import dataclass

import terminaltexteffects.utils.arg_validators as arg_validators
from terminaltexteffects.base_character import EffectCharacter
from terminaltexteffects.base_effect import BaseEffect
from terminaltexteffects.utils import graphics
from terminaltexteffects.utils.argsdataclass import ArgField, ArgsDataClass, argclass
from terminaltexteffects.utils.terminal import Terminal, TerminalConfig


def get_effect_and_args() -> tuple[type[typing.Any], type[ArgsDataClass]]:
    return BeamsEffect, EffectConfig


@argclass(
    name="beams",
    help="Create beams which travel over the output area illuminating the characters behind them.",
    description="beams | Create beams which travel over the output area illuminating the characters behind them.",
    epilog="""Example: terminaltexteffects beams --beam-row-symbols ▂ ▁ _ --beam-column-symbols ▌ ▍ ▎ ▏ --beam-delay 10 --beam-row-speed-range 10-40 --beam-column-speed-range 6-10 --beam-gradient-stops ffffff 00D1FF 8A008A --beam-gradient-steps 2 8 --beam-gradient-frames 2 --final-gradient-stops 8A008A 00D1FF ffffff --final-gradient-steps 12 --final-gradient-frames 5 --final-gradient-direction vertical --final-wipe-speed 1""",
)
@dataclass
class EffectConfig(ArgsDataClass):
    """Configuration for the Beams effect.

    Attributes:
        beam_row_symbols (tuple[str, ...]): Symbols to use for the beam effect when moving along a row. Strings will be used in sequence to create an animation.
        beam_column_symbols (tuple[str, ...]): Symbols to use for the beam effect when moving along a column. Strings will be used in sequence to create an animation.
        beam_delay (int): Number of frames to wait before adding the next group of beams. Beams are added in groups of size random(1, 5).
        beam_row_speed_range (tuple[int, int]): Speed range of the beam when moving along a row.
        beam_column_speed_range (tuple[int, int]): Speed range of the beam when moving along a column.
        beam_gradient_stops (tuple[graphics.Color, ...]): Tuple of colors for the beam, a gradient will be created between the colors.
        beam_gradient_steps (tuple[int, ...]): Tuple of the number of gradient steps to use. More steps will create a smoother and longer gradient animation. Steps are paired with the colors in final-gradient-stops.
        beam_gradient_frames (int): Number of frames to display each gradient step.
        final_gradient_stops (tuple[graphics.Color, ...]): Tuple of colors for the wipe gradient.
        final_gradient_steps (tuple[int,]): Tuple of the number of gradient steps to use. More steps will create a smoother and longer gradient animation. Steps are paired with the colors in final-gradient-stops.
        final_gradient_frames (int): Number of frames to display each gradient step.
        final_gradient_direction (graphics.Gradient.Direction): Direction of the gradient for the final color.
        final_wipe_speed (int): Speed of the final wipe as measured in diagonal groups activated per frame.
    """

    beam_row_symbols: tuple[str, ...] = ArgField(
        cmd_name="--beam-row-symbols",
        type_parser=arg_validators.Symbol.type_parser,
        nargs="+",
        default=("▂", "▁", "_"),
        metavar=arg_validators.Symbol.METAVAR,
        help="Symbols to use for the beam effect when moving along a row. Strings will be used in sequence to create an animation.",
    )  # type: ignore[assignment]
    "tuple[str, ...] : Symbols to use for the beam effect when moving along a row. Strings will be used in sequence to create an animation."

    beam_column_symbols: tuple[str, ...] = ArgField(
        cmd_name="--beam-column-symbols",
        type_parser=arg_validators.Symbol.type_parser,
        nargs="+",
        default=("▌", "▍", "▎", "▏"),
        metavar=arg_validators.Symbol.METAVAR,
        help="Symbols to use for the beam effect when moving along a column. Strings will be used in sequence to create an animation.",
    )  # type: ignore[assignment]
    "tuple[str, ...] : Symbols to use for the beam effect when moving along a column. Strings will be used in sequence to create an animation."

    beam_delay: int = ArgField(
        cmd_name="--beam-delay",
        type_parser=arg_validators.PositiveInt.type_parser,
        default=10,
        metavar=arg_validators.PositiveInt.METAVAR,
        help="Number of frames to wait before adding the next group of beams. Beams are added in groups of size random(1, 5).",
    )  # type: ignore[assignment]
    "int : Number of frames to wait before adding the next group of beams. Beams are added in groups of size random(1, 5)."

    beam_row_speed_range: tuple[int, int] = ArgField(
        cmd_name="--beam-row-speed-range",
        type_parser=arg_validators.IntRange.type_parser,
        default=(10, 40),
        metavar=arg_validators.IntRange.METAVAR,
        help="Speed range of the beam when moving along a row.",
    )  # type: ignore[assignment]
    "tuple[int, int] : Speed range of the beam when moving along a row."

    beam_column_speed_range: tuple[int, int] = ArgField(
        cmd_name="--beam-column-speed-range",
        type_parser=arg_validators.IntRange.type_parser,
        default=(6, 10),
        metavar=arg_validators.IntRange.METAVAR,
        help="Speed range of the beam when moving along a column.",
    )  # type: ignore[assignment]
    "tuple[int, int] : Speed range of the beam when moving along a column."

    beam_gradient_stops: tuple[graphics.Color, ...] = ArgField(
        cmd_name="--beam-gradient-stops",
        type_parser=arg_validators.Color.type_parser,
        nargs="+",
        default=("ffffff", "00D1FF", "8A008A"),
        metavar="(XTerm [0-255] OR RGB Hex [000000-ffffff])",
        help="Space separated, unquoted, list of colors for the beam, a gradient will be created between the colors.",
    )  # type: ignore[assignment]
    "tuple[graphics.Color, ...] : Tuple of colors for the beam, a gradient will be created between the colors."

    beam_gradient_steps: tuple[int, ...] = ArgField(
        cmd_name="--beam-gradient-steps",
        type_parser=arg_validators.PositiveInt.type_parser,
        nargs="+",
        default=(2, 8),
        metavar=arg_validators.PositiveInt.METAVAR,
        help="Space separated, unquoted, numbers for the of gradient steps to use. More steps will create a smoother and longer gradient animation. Steps are paired with the colors in final-gradient-stops.",
    )  # type: ignore[assignment]
    "tuple[int, ...] : Tuple of the number of gradient steps to use. More steps will create a smoother and longer gradient animation. Steps are paired with the colors in final-gradient-stops."

    beam_gradient_frames: int = ArgField(
        cmd_name="--beam-gradient-frames",
        type_parser=arg_validators.PositiveInt.type_parser,
        default=2,
        metavar=arg_validators.PositiveInt.METAVAR,
        help="Number of frames to display each gradient step.",
    )  # type: ignore[assignment]
    "int : Number of frames to display each gradient step."

    final_gradient_stops: tuple[graphics.Color, ...] = ArgField(
        cmd_name="--final-gradient-stops",
        type_parser=arg_validators.Color.type_parser,
        nargs="+",
        default=("8A008A", "00D1FF", "ffffff"),
        metavar=arg_validators.Color.METAVAR,
        help="Space separated, unquoted, list of colors for the wipe gradient.",
    )  # type: ignore[assignment]
    "tuple[graphics.Color, ...] : Tuple of colors for the wipe gradient."

    final_gradient_steps: tuple[int,] = ArgField(
        cmd_name="--final-gradient-steps",
        type_parser=arg_validators.PositiveInt.type_parser,
        nargs="+",
        default=(12,),
        metavar=arg_validators.PositiveInt.METAVAR,
        help="Space separated, unquoted, numbers for the of gradient steps to use. More steps will create a smoother and longer gradient animation. Steps are paired with the colors in final-gradient-stops.",
    )  # type: ignore[assignment]
    "tuple[int, ...] : Tuple of the number of gradient steps to use. More steps will create a smoother and longer gradient animation. Steps are paired with the colors in final-gradient-stops."

    final_gradient_frames: int = ArgField(
        cmd_name="--final-gradient-frames",
        type_parser=arg_validators.PositiveInt.type_parser,
        default=5,
        metavar=arg_validators.PositiveInt.METAVAR,
        help="Number of frames to display each gradient step.",
    )  # type: ignore[assignment]
    "int : Number of frames to display each gradient step."

    final_gradient_direction: graphics.Gradient.Direction = ArgField(
        cmd_name="--final-gradient-direction",
        type_parser=arg_validators.GradientDirection.type_parser,
        default=graphics.Gradient.Direction.VERTICAL,
        metavar=arg_validators.GradientDirection.METAVAR,
        help="Direction of the gradient for the final color.",
    )  # type: ignore[assignment]
    "graphics.Gradient.Direction : Direction of the gradient for the final color."

    final_wipe_speed: int = ArgField(
        cmd_name="--final-wipe-speed",
        type_parser=arg_validators.PositiveInt.type_parser,
        default=1,
        metavar=arg_validators.PositiveInt.METAVAR,
        help="Speed of the final wipe as measured in diagonal groups activated per frame.",
    )  # type: ignore[assignment]
    "int : Speed of the final wipe as measured in diagonal groups activated per frame."

    @classmethod
    def get_effect_class(cls):
        return BeamsEffect


class _Group:
    def __init__(self, characters: list[EffectCharacter], direction: str, terminal: Terminal, args: EffectConfig):
        self.characters = characters
        self.direction: str = direction
        self.terminal = terminal
        direction_speed_range = {
            "row": (args.beam_row_speed_range[0], args.beam_row_speed_range[1]),
            "column": (args.beam_column_speed_range[0], args.beam_column_speed_range[1]),
        }
        self.speed = random.randint(direction_speed_range[direction][0], direction_speed_range[direction][1]) * 0.1
        self.next_character_counter: float = 0
        if self.direction == "row":
            self.characters.sort(key=lambda character: character.input_coord.column)
        elif self.direction == "column":
            self.characters.sort(key=lambda character: character.input_coord.row)
        if random.choice([True, False]):
            self.characters.reverse()

    def increment_next_character_counter(self) -> None:
        self.next_character_counter += self.speed

    def get_next_character(self) -> EffectCharacter | None:
        self.next_character_counter -= 1
        next_character = self.characters.pop(0)
        if next_character.animation.active_scene:
            next_character.animation.active_scene.reset_scene()
            return_value = None
        else:
            self.terminal.set_character_visibility(next_character, True)
            return_value = next_character
        next_character.animation.activate_scene(next_character.animation.query_scene("beam_" + self.direction))
        return return_value

    def complete(self) -> bool:
        return not self.characters


class BeamsEffect(BaseEffect):
    """Effect that creates beams which travel over the output area illuminated the characters behind them."""

    def __init__(
        self,
        input_data: str,
        effect_config: EffectConfig = EffectConfig(),
        terminal_config: TerminalConfig = TerminalConfig(),
    ):
        """Initializes the effect.

        Args:
            input_data (str): The input data to apply the effect to.
            effect_config (EffectConfig, optional): The configuration of the effect. Defaults to EffectConfig().
            terminal_config (TerminalConfig, optional): The configuration of the terminal. Defaults to TerminalConfig().
        """
        self.terminal = Terminal(input_data, terminal_config)
        self.config = effect_config
        self._built = False
        self._pending_groups: list[_Group] = []
        self._active_chars: list[EffectCharacter] = []
        self._character_final_color_map: dict[EffectCharacter, graphics.Color] = {}

    def build(self) -> None:
        self._pending_groups.clear()
        self._active_chars.clear()
        self._character_final_color_map.clear()
        final_gradient = graphics.Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.output_area.top, self.terminal.output_area.right, self.config.final_gradient_direction
        )
        for character in self.terminal.get_characters(fill_chars=True):
            self._character_final_color_map[character] = final_gradient_mapping[character.input_coord]

        beam_gradient = graphics.Gradient(*self.config.beam_gradient_stops, steps=self.config.beam_gradient_steps)
        groups: list[_Group] = []
        for row in self.terminal.get_characters_grouped(Terminal.CharacterGroup.ROW_TOP_TO_BOTTOM, fill_chars=True):
            groups.append(_Group(row, "row", self.terminal, self.config))
        for column in self.terminal.get_characters_grouped(
            Terminal.CharacterGroup.COLUMN_LEFT_TO_RIGHT, fill_chars=True
        ):
            groups.append(_Group(column, "column", self.terminal, self.config))
        for group in groups:
            for character in group.characters:
                beam_row_scn = character.animation.new_scene(id="beam_row")
                beam_column_scn = character.animation.new_scene(id="beam_column")
                beam_row_scn.apply_gradient_to_symbols(
                    beam_gradient, self.config.beam_row_symbols, self.config.beam_gradient_frames
                )
                beam_column_scn.apply_gradient_to_symbols(
                    beam_gradient, self.config.beam_column_symbols, self.config.beam_gradient_frames
                )
                faded_color = character.animation.adjust_color_brightness(
                    self._character_final_color_map[character], 0.3
                )
                fade_gradient = graphics.Gradient(self._character_final_color_map[character], faded_color, steps=10)
                beam_row_scn.apply_gradient_to_symbols(fade_gradient, character.input_symbol, 5)
                beam_column_scn.apply_gradient_to_symbols(fade_gradient, character.input_symbol, 5)
                brighten_gradient = graphics.Gradient(faded_color, self._character_final_color_map[character], steps=10)
                brigthen_scn = character.animation.new_scene(id="brighten")
                brigthen_scn.apply_gradient_to_symbols(
                    brighten_gradient, character.input_symbol, self.config.final_gradient_frames
                )
        self._pending_groups = groups
        random.shuffle(self._pending_groups)
        self._built = True

    @property
    def built(self) -> bool:
        """Returns True if the effect has been built."""
        return self._built

    def __iter__(self) -> Iterator[str]:
        self.build()
        active_groups: list[_Group] = []
        delay = 0
        phase = "beams"
        final_wipe_groups = self.terminal.get_characters_grouped(
            Terminal.CharacterGroup.DIAGONAL_TOP_LEFT_TO_BOTTOM_RIGHT
        )
        while phase != "complete" or self._active_chars:
            if phase == "beams":
                if not delay:
                    if self._pending_groups:
                        for _ in range(random.randint(1, 5)):
                            if self._pending_groups:
                                active_groups.append(self._pending_groups.pop(0))
                    delay = self.config.beam_delay
                else:
                    delay -= 1
                for group in active_groups:
                    group.increment_next_character_counter()
                    if int(group.next_character_counter) > 1:
                        for _ in range(int(group.next_character_counter)):
                            if not group.complete():
                                next_char = group.get_next_character()
                                if next_char:
                                    self._active_chars.append(next_char)
                active_groups = [group for group in active_groups if not group.complete()]
                if not self._pending_groups and not active_groups and not self._active_chars:
                    phase = "final_wipe"
            elif phase == "final_wipe":
                if final_wipe_groups:
                    for _ in range(self.config.final_wipe_speed):
                        if not final_wipe_groups:
                            break
                        next_group = final_wipe_groups.pop(0)
                        for character in next_group:
                            character.animation.activate_scene(character.animation.query_scene("brighten"))
                            self.terminal.set_character_visibility(character, True)
                            self._active_chars.append(character)
                else:
                    phase = "complete"
            yield self.terminal.get_formatted_output_string()
            self.animate_chars()

            self._active_chars = [character for character in self._active_chars if character.is_active]
        yield self.terminal.get_formatted_output_string()
        self._built = False

    def animate_chars(self) -> None:
        """Animates the characters by calling the tick method on all active characters."""
        for character in self._active_chars:
            character.tick()
