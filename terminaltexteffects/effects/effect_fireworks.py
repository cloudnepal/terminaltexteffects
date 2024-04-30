"""Launches characters up the screen where they explode like fireworks and fall into place.

Classes:
    Fireworks: Characters explode like fireworks and fall into place.
    FireworksConfig: Configuration for the Fireworks effect.
    FireworksIterator: Iterates over the effect. Does not normally need to be called directly.
"""

import random
import typing
from dataclasses import dataclass

from terminaltexteffects.engine.base_character import EffectCharacter, EventHandler
from terminaltexteffects.engine.base_effect import BaseEffect, BaseEffectIterator
from terminaltexteffects.utils import argvalidators, easing, geometry, graphics
from terminaltexteffects.utils.argsdataclass import ArgField, ArgsDataClass, argclass
from terminaltexteffects.utils.geometry import Coord


def get_effect_and_args() -> tuple[type[typing.Any], type[ArgsDataClass]]:
    return Fireworks, FireworksConfig


@argclass(
    name="fireworks",
    help="Characters launch and explode like fireworks and fall into place.",
    description="fireworks | Characters explode like fireworks and fall into place.",
    epilog="""Example: terminaltexteffects fireworks --firework-colors 88F7E2 44D492 F5EB67 FFA15C FA233E --firework-symbol o --firework-volume 0.02 --final-gradient-stops 8A008A 00D1FF FFFFFF --final-gradient-steps 12 --launch-delay 60 --explode-distance 0.1 --explode-anywhere""",
)
@dataclass
class FireworksConfig(ArgsDataClass):
    """Configuration for the Fireworks effect.

    Attributes:
        explode_anywhere (bool): If set, fireworks explode anywhere in the output area. Otherwise, fireworks explode above highest settled row of text.
        firework_colors (tuple[graphics.Color, ...]): Tuple of colors from which firework colors will be randomly selected.
        firework_symbol (str): Symbol to use for the firework shell.
        firework_volume (float): Percent of total characters in each firework shell. Valid values are 0 < n <= 1.
        final_gradient_stops (tuple[graphics.Color, ...]): Tuple of colors for the final color gradient. If only one color is provided, the characters will be displayed in that color.
        final_gradient_steps (tuple[int, ...]): Tuple of the number of gradient steps to use. More steps will create a smoother and longer gradient animation. Valid values are n > 0.
        final_gradient_direction (graphics.Gradient.Direction): Direction of the final gradient.
        launch_delay (int): Number of frames to wait between launching each firework shell. +/- 0-50 percent randomness is applied to this value. Valid values are n >= 0.
        explode_distance (float): Maximum distance from the firework shell origin to the explode waypoint as a percentage of the total output area width. Valid values are 0 < n <= 1."""

    explode_anywhere: bool = ArgField(
        cmd_name="--explode-anywhere",
        action="store_true",
        default=False,
        help="If set, fireworks explode anywhere in the output area. Otherwise, fireworks explode above highest settled row of text.",
    )  # type: ignore[assignment]
    "bool : If set, fireworks explode anywhere in the output area. Otherwise, fireworks explode above highest settled row of text."

    firework_colors: tuple[graphics.Color, ...] = ArgField(
        cmd_name="--firework-colors",
        type_parser=argvalidators.ColorArg.type_parser,
        nargs="+",
        default=("88F7E2", "44D492", "F5EB67", "FFA15C", "FA233E"),
        metavar=argvalidators.ColorArg.METAVAR,
        help="Space separated list of colors from which firework colors will be randomly selected.",
    )  # type: ignore[assignment]
    "tuple[graphics.Color, ...] : Tuple of colors from which firework colors will be randomly selected."

    firework_symbol: str = ArgField(
        cmd_name="--firework-symbol",
        type_parser=argvalidators.Symbol.type_parser,
        default="o",
        metavar=argvalidators.Symbol.METAVAR,
        help="Symbol to use for the firework shell.",
    )  # type: ignore[assignment]
    "str : Symbol to use for the firework shell."

    firework_volume: float = ArgField(
        cmd_name="--firework-volume",
        type_parser=argvalidators.Ratio.type_parser,
        default=0.02,
        metavar=argvalidators.Ratio.METAVAR,
        help="Percent of total characters in each firework shell.",
    )  # type: ignore[assignment]
    "float : Percent of total characters in each firework shell."

    final_gradient_stops: tuple[graphics.Color, ...] = ArgField(
        cmd_name="--final-gradient-stops",
        type_parser=argvalidators.ColorArg.type_parser,
        nargs="+",
        default=("8A008A", "00D1FF", "FFFFFF"),
        metavar=argvalidators.ColorArg.METAVAR,
        help="Space separated, unquoted, list of colors for the character gradient (applied from bottom to top). If only one color is provided, the characters will be displayed in that color.",
    )  # type: ignore[assignment]
    "tuple[graphics.Color, ...] : Tuple of colors for the final color gradient. If only one color is provided, the characters will be displayed in that color."

    final_gradient_steps: tuple[int, ...] = ArgField(
        cmd_name="--final-gradient-steps",
        type_parser=argvalidators.PositiveInt.type_parser,
        nargs="+",
        default=(12,),
        metavar=argvalidators.PositiveInt.METAVAR,
        help="Space separated, unquoted, list of the number of gradient steps to use. More steps will create a smoother and longer gradient animation.",
    )  # type: ignore[assignment]
    "tuple[int, ...] : Tuple of the number of gradient steps to use. More steps will create a smoother and longer gradient animation."

    final_gradient_direction: graphics.Gradient.Direction = ArgField(
        cmd_name="--final-gradient-direction",
        type_parser=argvalidators.GradientDirection.type_parser,
        default=graphics.Gradient.Direction.HORIZONTAL,
        metavar=argvalidators.GradientDirection.METAVAR,
        help="Direction of the final gradient.",
    )  # type: ignore[assignment]
    "graphics.Gradient.Direction : Direction of the final gradient."

    launch_delay: int = ArgField(
        cmd_name="--launch-delay",
        type_parser=argvalidators.NonNegativeInt.type_parser,
        default=60,
        metavar=argvalidators.NonNegativeInt.METAVAR,
        help="Number of frames to wait between launching each firework shell. +/- 0-50 percent randomness is applied to this value.",
    )  # type: ignore[assignment]
    "int : Number of frames to wait between launching each firework shell. +/- 0-50 percent randomness is applied to this value."

    explode_distance: float = ArgField(
        cmd_name="--explode-distance",
        default=0.1,
        type_parser=argvalidators.Ratio.type_parser,
        metavar=argvalidators.Ratio.METAVAR,
        help="Maximum distance from the firework shell origin to the explode waypoint as a percentage of the total output area width.",
    )  # type: ignore[assignment]
    "float : Maximum distance from the firework shell origin to the explode waypoint as a percentage of the total output area width."

    @classmethod
    def get_effect_class(cls):
        return Fireworks


class FireworksIterator(BaseEffectIterator[FireworksConfig]):
    def __init__(self, effect: "Fireworks"):
        super().__init__(effect)
        self._pending_chars: list[EffectCharacter] = []
        self._active_chars: list[EffectCharacter] = []
        self._shells: list[list[EffectCharacter]] = []
        self._firework_volume = max(1, round(self._config.firework_volume * len(self._terminal._input_characters)))
        self._explode_distance = max(1, round(self._terminal.output_area.right * self._config.explode_distance))
        self._character_final_color_map: dict[EffectCharacter, graphics.Color] = {}
        self._launch_delay: int = 0
        self._build()

    def prepare_waypoints(self) -> None:
        firework_shell: list[EffectCharacter] = []
        for character in self._terminal.get_characters():
            if len(firework_shell) == self._firework_volume or not firework_shell:
                self._shells.append(firework_shell)
                firework_shell = []
                origin_x = random.randrange(0, self._terminal.output_area.right)
                if not self._config.explode_anywhere:
                    min_row = character.input_coord.row
                else:
                    min_row = self._terminal.output_area.bottom
                origin_y = random.randrange(min_row, self._terminal.output_area.top + 1)
                origin_coord = Coord(origin_x, origin_y)
                explode_waypoint_coords = geometry.find_coords_in_circle(origin_coord, self._explode_distance)
            character.motion.set_coordinate(Coord(origin_x, self._terminal.output_area.bottom))
            apex_path = character.motion.new_path(id="apex_pth", speed=0.2, ease=easing.out_expo)
            apex_wpt = apex_path.new_waypoint(origin_coord)
            explode_path = character.motion.new_path(speed=0.15, ease=easing.out_circ)
            explode_wpt = explode_path.new_waypoint(random.choice(explode_waypoint_coords))

            bloom_control_point = geometry.find_coord_at_distance(
                apex_wpt.coord, explode_wpt.coord, self._explode_distance // 2
            )
            bloom_wpt = explode_path.new_waypoint(
                Coord(bloom_control_point.column, max(1, bloom_control_point.row - 7)),
                bezier_control=bloom_control_point,
            )
            input_path = character.motion.new_path(id="input_pth", speed=0.3, ease=easing.in_out_quart)
            input_control_point = Coord(bloom_wpt.coord.column, 1)
            input_path.new_waypoint(character.input_coord, bezier_control=input_control_point)
            character.event_handler.register_event(
                EventHandler.Event.PATH_ACTIVATED, apex_path, EventHandler.Action.SET_LAYER, 2
            )
            character.event_handler.register_event(
                EventHandler.Event.PATH_COMPLETE, explode_path, EventHandler.Action.SET_LAYER, 0
            )
            character.event_handler.register_event(
                EventHandler.Event.PATH_COMPLETE,
                apex_path,
                EventHandler.Action.ACTIVATE_PATH,
                explode_path,
            )
            character.event_handler.register_event(
                EventHandler.Event.PATH_COMPLETE, explode_path, EventHandler.Action.ACTIVATE_PATH, input_path
            )

            character.motion.activate_path(apex_path)

            firework_shell.append(character)
        if firework_shell:
            self._shells.append(firework_shell)

    def prepare_scenes(self) -> None:
        final_gradient = graphics.Gradient(*self._config.final_gradient_stops, steps=self._config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self._terminal.output_area.top, self._terminal.output_area.right, self._config.final_gradient_direction
        )
        for character in self._terminal.get_characters():
            self._character_final_color_map[character] = final_gradient_mapping[character.input_coord]
        for firework_shell in self._shells:
            shell_color = random.choice(self._config.firework_colors)
            for character in firework_shell:
                # launch scene
                launch_scn = character.animation.new_scene()
                launch_scn.add_frame(self._config.firework_symbol, 2, color=shell_color)
                launch_scn.add_frame(self._config.firework_symbol, 1, color="FFFFFF")
                launch_scn.is_looping = True
                # bloom scene
                bloom_scn = character.animation.new_scene()
                bloom_scn.add_frame(character.input_symbol, 1, color=shell_color)
                # fall scene
                fall_scn = character.animation.new_scene()
                fall_gradient = graphics.Gradient(shell_color, self._character_final_color_map[character], steps=15)
                fall_scn.apply_gradient_to_symbols(fall_gradient, character.input_symbol, 15)
                character.animation.activate_scene(launch_scn)
                character.event_handler.register_event(
                    EventHandler.Event.PATH_COMPLETE,
                    character.motion.query_path("apex_pth"),
                    EventHandler.Action.ACTIVATE_SCENE,
                    bloom_scn,
                )
                character.event_handler.register_event(
                    EventHandler.Event.PATH_ACTIVATED,
                    character.motion.query_path("input_pth"),
                    EventHandler.Action.ACTIVATE_SCENE,
                    fall_scn,
                )

    def _build(self) -> None:
        self.prepare_waypoints()
        self.prepare_scenes()

    def __next__(self) -> str:
        if self._shells or self._active_chars:
            if self._shells and self._launch_delay == 0:
                next_group = self._shells.pop()
                for character in next_group:
                    self._terminal.set_character_visibility(character, True)
                    self._active_chars.append(character)
                self._launch_delay = int(self._config.launch_delay * random.uniform(0.5, 1.5))
            for character in self._active_chars:
                character.tick()
            self._launch_delay -= 1
            next_frame = self._terminal.get_formatted_output_string()
            self._active_chars = [character for character in self._active_chars if character.is_active]
            return next_frame

        else:
            raise StopIteration


class Fireworks(BaseEffect[FireworksConfig]):
    """Launches characters up the screen where they explode like fireworks and fall into place.

    Attributes:
        effect_config (FireworksConfig): Configuration for the effect.
        terminal_config (TerminalConfig): Configuration for the terminal.

    """

    _config_cls = FireworksConfig
    _iterator_cls = FireworksIterator

    def __init__(self, input_data: str):
        """Initialize the effect with the provided input data.

        Args:
            input_data (str): The input data to use for the effect."""
        super().__init__(input_data)
