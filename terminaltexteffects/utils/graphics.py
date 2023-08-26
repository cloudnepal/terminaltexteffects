import typing
from dataclasses import dataclass, field

from terminaltexteffects.utils import ansitools, colorterm, hexttoxterm

if typing.TYPE_CHECKING:
    from terminaltexteffects import base_character


@dataclass
class GraphicalEffect:
    """A class for storing terminal graphical modes and a color.

    Supported graphical modes:
    bold, dim, italic, underline, blink, inverse, hidden, strike

    Args:
        symbol (str): the symbol to show
        bold (bool): bold mode
        dim (bool): dim mode
        italic (bool): italic mode
        underline (bool): underline mode
        blink (bool): blink mode
        reverse (bool): reverse mode
        hidden (bool): hidden mode
        strike (bool): strike mode
        color (int | str): color code
    """

    symbol: str
    bold: bool = False
    dim: bool = False
    italic: bool = False
    underline: bool = False
    blink: bool = False
    reverse: bool = False
    hidden: bool = False
    strike: bool = False
    color: int | str | None = None

    def __post_init__(self):
        self.format_symbol()

    def disable_modes(self) -> None:
        """Disables all graphical modes."""
        self.bold = False
        self.dim = False
        self.italic = False
        self.underline = False
        self.blink = False
        self.reverse = False
        self.hidden = False
        self.strike = False

    def format_symbol(self) -> None:
        """Formats the symbol for printing."""
        formatting_string = ""
        if self.bold:
            formatting_string += ansitools.APPLY_BOLD()
        if self.italic:
            formatting_string += ansitools.APPLY_ITALIC()
        if self.underline:
            formatting_string += ansitools.APPLY_UNDERLINE()
        if self.blink:
            formatting_string += ansitools.APPLY_BLINK()
        if self.reverse:
            formatting_string += ansitools.APPLY_REVERSE()
        if self.hidden:
            formatting_string += ansitools.APPLY_HIDDEN()
        if self.strike:
            formatting_string += ansitools.APPLY_STRIKETHROUGH()
        if self.color is not None:
            formatting_string += colorterm.fg(self.color)

        self.symbol = f"{formatting_string}{self.symbol}{ansitools.RESET_ALL() if formatting_string else ''}"


@dataclass
class Sequence:
    """An Sequence is a graphicaleffect with a duration.
    Args:
        graphical_effect (GraphicalEffect): a GraphicalEffect object containing the graphical modes and color of the character
        duration (int): the number of animation steps to use the Sequence
    """

    graphical_effect: GraphicalEffect
    duration: int

    def __post_init__(self):
        self.frames_played = 0
        self.symbol = self.graphical_effect.symbol


@dataclass
class Scene:
    """A Scene is a list of Sequences.

    Args:
        name (str): the name of the Scene
        sequences (list[Sequence]): a list of Sequence objects
        is_looping (bool): whether the Scene should loop
    """

    name: str
    sequences: list[Sequence] = field(default_factory=list)
    is_looping: bool = False

    def __post_init__(self):
        self.played_sequences = []

    def add_sequence(self, graphicaleffect: GraphicalEffect, duration: int) -> None:
        """Adds a Sequence to the Scene.

        Args:
            graphicaleffect (GraphicalEffect): a GraphicalEffect object containing the graphical modes and color of the character
            duration (int): the number of animation steps to use the Sequence
        """
        self.sequences.append(Sequence(graphicaleffect, duration))

    def get_next_symbol(self) -> str:
        """Returns the next symbol in the Scene.

        Returns:
            str: the next symbol in the Scene
        """
        current_sequence = self.sequences[0]
        next_symbol = current_sequence.symbol
        current_sequence.frames_played += 1
        if current_sequence.frames_played == current_sequence.duration:
            current_sequence.frames_played = 0
            self.played_sequences.append(self.sequences.pop(0))
            if self.is_looping and not self.sequences:
                self.sequences.extend(self.played_sequences)
                self.played_sequences.clear()
        return next_symbol

    def reset_scene(self) -> None:
        """Resets the Scene."""
        for sequence in self.sequences:
            sequence.frames_played = 0
            self.played_sequences.append(sequence)
        self.sequences.clear()
        self.sequences.extend(self.played_sequences)
        self.played_sequences.clear()


class Animator:
    def __init__(self, character: "base_character.EffectCharacter"):
        """Animator handles the animations of a character. It contains a list of Scenes, and the active scene name. GraphicalEffects are
        added to the Scenes, and the Animator returns the next symbol in the active scene.

        Args:
            character (base_character.EffectCharacter): the EffectCharacter object to animate
        """
        self.character = character
        self.scenes: dict[str, Scene] = {}
        self.active_scene_name: str = ""
        self.is_animating: bool = True
        self.use_xterm_colors: bool = False
        self.xterm_color_map: dict[str, int] = {}

    def add_effect_to_scene(
        self, scene_name: str, symbol: str | None = None, color: int | str | None = None, duration: int = 1
    ) -> None:
        """Add a graphical effect to a scene. If the scene doesn't exist, it will be created.

        Args:
            scene_name (str): Name of the scene to which the effect will be added
            symbol (str): Symbol to display, if None, the character's input symbol will be used
            color (int | str): XTerm color code (0-255) or hex color code (e.g. ffffff)
            duration (int): Number of animation steps to display the effect, defaults to 1. Minimum 1.
        """
        if duration < 1:
            raise ValueError("duration must be greater than 0")
        if scene_name not in self.scenes:
            new_scene = Scene(scene_name)
            self.scenes[scene_name] = new_scene
        if not symbol:
            symbol = self.character.input_symbol
        if self.use_xterm_colors and isinstance(color, str):
            if color in self.xterm_color_map:
                color = self.xterm_color_map[color]
            else:
                xterm_color = hexttoxterm.hex_to_xterm(color)
                self.xterm_color_map[color] = xterm_color
                color = xterm_color
        graphicaleffect = GraphicalEffect(symbol, color=color)
        self.scenes[scene_name].add_sequence(graphicaleffect, duration)

    def is_active_scene_complete(self) -> bool:
        """Returns whether the active scene is complete. A scene is complete if all sequences have been played,
        the scene is looping, or the animator is not animating.

        Returns:
            bool: True if complete, False otherwise
        """
        if (
            not self.scenes[self.active_scene_name].sequences
            or self.scenes[self.active_scene_name].is_looping
            or not self.is_animating
        ):
            return True
        else:
            return False

    def step_animation(self) -> None:
        """Apply the next symbol in the scene to the character."""
        if self.active_scene_name and self.scenes[self.active_scene_name].sequences:
            self.character.symbol = self.scenes[self.active_scene_name].get_next_symbol()

    def reset_scene(self, scene_name: str) -> None:
        """Resets the Scene.

        Args:
            scene_name (str): the name of the Scene to reset
        """
        if scene_name in self.scenes:
            self.scenes[scene_name].reset_scene()


def gradient(start_color: str | int, end_color: str | int, steps: int) -> list[str]:
    """Calculate a gradient of colors between two colors using linear interpolation.

    Args:
        start_color (str|int): RGB hex color string or XTerm-256 color code
        end_color (str|int): RGB hex color string or XTerm-256 color code
        steps (int): Number of intermediate colors to calculate

    Returns:
        list[str]: List (length=steps + 2) of RGB hex color strings
    """
    if isinstance(start_color, int):
        start_color = hexttoxterm.xterm_to_hex(start_color)
    if isinstance(end_color, int):
        end_color = hexttoxterm.xterm_to_hex(end_color)
    start_color_ints = colorterm._hex_to_int(start_color)
    end_color_ints = colorterm._hex_to_int(end_color)
    gradient_colors = []
    gradient_colors.append(start_color)
    red_delta = (end_color_ints[0] - start_color_ints[0]) // steps
    green_delta = (end_color_ints[1] - start_color_ints[1]) // steps
    blue_delta = (end_color_ints[2] - start_color_ints[2]) // steps
    for i in range(steps):
        red = start_color_ints[0] + (red_delta * i)
        green = start_color_ints[1] + (green_delta * i)
        blue = start_color_ints[2] + (blue_delta * i)
        gradient_colors.append(f"{red:02x}{green:02x}{blue:02x}")
    gradient_colors.append(end_color)
    return gradient_colors