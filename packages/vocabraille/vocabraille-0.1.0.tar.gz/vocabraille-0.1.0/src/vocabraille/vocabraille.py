import ctypes as _ctypes
import struct
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import Any, Iterator, NamedTuple, Union
from warnings import warn


class _SpeechParam(IntEnum):
    """Parameters used for functions speechSetValue, speechGetValue, speechSetString and speechGetString.
    The following few values are in groupes of 4 parameters.
    + First one is used to get or set the current value for this parameter
    + Second and third one are used to retriev the minimum and the maximum values allowed for the parameter
    + Last one is used to query if the currently active engine, subengine, language and voice supports the parameter. If 0 is returned, then the parameter isn't supported. Any other value different than 0 means that the parameter is supported and thus can be get or set. A supported parameter may be read only and thus refuse any attend to change the value.
    """

    VOLUME = 0
    VOLUME_MAX = 1
    VOLUME_MIN = 2
    VOLUME_SUPPORTED = 3
    RATE = 4
    RATE_MAX = 5
    RATE_MIN = 6
    RATE_SUPPORTED = 7
    PITCH = 8
    PITCH_MAX = 9
    PITCH_MIN = 10
    PITCH_SUPPORTED = 11
    INFLEXION = 12
    INFLEXION_MAX = 13
    INFLEXION_MIN = 14
    INFLEXION_SUPPORTED = 15
    PAUSED = 16
    PAUSE_SUPPORTED = 17
    BUSY = 18
    BUSY_SUPPORTED = 19
    WAIT = 20
    WAIT_SUPPORTED = 21

    ENABLE_NATIVE_SPEECH = 0xFFFF
    VOICE = 0x10000
    LANGUAGE = 0x20000
    SUBENGINE = 0x30000
    ENGINE = 0x40000
    ENGINE_AVAILABLE = 0x50000
    AUTO_ENGINE = 0xFFFE
    USER_PARAM = 0x1000000


class _Engine(NamedTuple):
    """Represents a speech engine."""

    index: int
    name: str
    available: bool

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return (
            f'_Engine(id={self.index}, name="{self.name}", available={self.available})'
        )


class _Voice(NamedTuple):
    """Represents a voice in a speech engine."""

    index: int
    name: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f'_Voice(id={self.index}, name="{self.name}")'


class _Language(NamedTuple):
    """Represents a language in a speech engine."""

    index: int
    name: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f'_Language(id={self.index}, name="{self.name}")'


class _SubEngine(NamedTuple):
    """Represents a sub-engine in a speech engine."""

    index: int
    name: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f'_SubEngine(id={self.index}, name="{self.name}")'


class ErrorsMode(StrEnum):
    """Enum for error handling modes."""

    IGNORE = "ignore"
    WARN = "warn"
    RAISE = "raise"

    def __str__(self):
        return self.value


class VocaBrailleWarning(Warning):
    """Custom warning category for VocaBraille library."""

    pass


class VocaBraille:
    """A Python wrapper for the UniversalSpeech library that provides text-to-speech functionality.

    VocaBraille provides a high-level interface to various text-to-speech (TTS) engines
    through the UniversalSpeech library. It supports multiple engines, voices, languages,
    and speech parameters like volume, rate, pitch, and inflection.

    The class automatically loads the appropriate UniversalSpeech DLL based on the
    system architecture and provides methods to control speech synthesis and
    braille display output.

    Features:
    - Multiple TTS engine support with automatic or manual selection
    - Voice, language, and sub-engine selection
    - Control of speech parameters (volume, rate, pitch, inflection)
    - Speech interruption and queue management
    - Braille display output
    - Error handling with configurable behavior (ignore, warn, raise)

    Basic usage:
    ```
    from vocabraille import VocaBraille, ErrorsMode

    # Create a VocaBraille instance
    vb = VocaBraille(errors=ErrorsMode.WARN)

    # Get available engines and select one
    print(vb.available_engines)
    vb.engine = "SAPI5"

    # Speak text
    vb.say("Hello, world!")

    # Speak and display on braille device
    vb.say_and_braille("Hello, braille world!")
    ```

    Error handling modes:
    - ErrorsMode.RAISE: Raises exceptions when operations fail (default)
    - ErrorsMode.WARN: Issues warnings when operations fail
    - ErrorsMode.IGNORE: Silently ignores operation failures
    """

    MAX_ENTITIES = 100  # Maximum number of entities (engines, voices, languages, subengines) to query

    def __init__(self, errors=ErrorsMode.RAISE) -> None:
        """Initialize the VocaBraille class and load the UniversalSpeech DLL."""
        self._errors = errors
        architecture_bits = struct.calcsize("P") * 8
        dll_path = (
            Path(__file__).parent
            / "bin"
            / str(architecture_bits)
            / "UniversalSpeech.dll"
        )
        try:
            self._uspeech = _ctypes.CDLL(str(dll_path))
        except FileNotFoundError:
            raise RuntimeError(f"UniversalSpeech.dll не знайдено за шляхом {dll_path}")
        except OSError as e:
            raise RuntimeError(f"Помилка завантаження UniversalSpeech.dll: {e}")
        self._setup_ctypes()

    def _setup_ctypes(self) -> None:
        """Set up ctypes argument and return types for UniversalSpeech DLL functions."""
        self._uspeech.speechGetString.restype = _ctypes.c_wchar_p
        self._uspeech.speechSetString.argtypes = [_ctypes.c_int, _ctypes.c_wchar_p]
        self._uspeech.speechGetStringA.restype = _ctypes.c_char_p
        self._uspeech.speechSetStringA.argtypes = [_ctypes.c_int, _ctypes.c_char_p]
        self._uspeech.speechSay.argtypes = [_ctypes.c_wchar_p, _ctypes.c_int]
        self._uspeech.speechSayA.argtypes = [_ctypes.c_char_p, _ctypes.c_int]
        self._uspeech.brailleDisplay.argtypes = [_ctypes.c_wchar_p]
        self._uspeech.brailleDisplayA.argtypes = [_ctypes.c_char_p]

    def _get_value(self, what: int) -> int:
        """Get integer parameter value from UniversalSpeech DLL."""
        return self._uspeech.speechGetValue(what)

    def _set_value(self, what: int, value: int) -> int:
        """Set integer parameter value in UniversalSpeech DLL."""
        return self._uspeech.speechSetValue(what, value)

    def _get_string(self, what: int) -> str:
        """Get string parameter value from UniversalSpeech DLL."""
        return self._uspeech.speechGetString(what) or ""

    def _set_string(self, what: int, value: str) -> int:
        """Set string parameter value in UniversalSpeech DLL."""
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")
        return self._uspeech.speechSetString(what, value)

    """ANSI version of the functions above, for those who don't support unicode.
    export const char* speechGetStringA (int what) ;
    export int speechSetStringA (int what, const char* value) ;
    """

    def _get_string_ansi(self, what: int) -> bytes:
        """Get ANSI string parameter value from UniversalSpeech DLL."""
        return self._uspeech.speechGetStringA(what) or b""

    def _set_string_ansi(self, what: int, value: bytes) -> int:
        """Set ANSI string parameter value in UniversalSpeech DLL."""
        if not isinstance(value, bytes):
            raise ValueError("Value must be a bytes object.")
        return self._uspeech.speechSetStringA(what, value)

    def _validate_value(
        self, value: int, name: str, min_val: int, max_val: int
    ) -> bool:
        """Validate that a value is an integer within a given range."""
        if not isinstance(value, int):
            raise ValueError(f"Value of {name!r} must be an integer.")
        if min_val <= value <= max_val:
            return True

        msg = f"{name} must be between {min_val} and {max_val}."
        if self._errors == ErrorsMode.RAISE:
            raise ValueError(msg)
        if self._errors == ErrorsMode.WARN:
            warn(msg, VocaBrailleWarning)
        return False

    ##### Engine
    """
    Being present on the list does not necessarily mean that the engine is available and working. 
    Generally, you will let the user select one of the supported ones. 
    By default, the system automatically select the first available and working engine, 
    and switch automatically to another engine when the current one become unavailable.
    When querying, it returns the actual current engine used as 0-based index. 
    A return value of -1 means that the system didn't find any suitable engine to work with.
    By setting the engine to a positive value, you force the system to use this engine, 
    even if it is in fact inoperant.
    You can restore the default behavior by setting the engine to -1.

    Query for example the parameter SP_ENGINE_AVAILABLE+3 to determine 
    if 4th engine is currently available and working if you select it.
    0 means unavailable, any other value mean available. 
    Normally, if you loop for names with SP_ENGINE+n, 
    you will get all engines names supported by universal speech, 
    not necessarily those which are really ready to be used. 
    Querying for actual availability allow you to filter the list presented to the user.
    """

    def _is_engine_available(self, engine_index: int) -> bool:
        """Check if the specified engine is available."""
        return bool(self._get_value(_SpeechParam.ENGINE_AVAILABLE + engine_index))

    def _get_current_entity_name(self, base_param: int) -> str | None:
        """Get the name of the current entity (engine, voice, language, subengine) by index."""
        current_index = self._get_value(base_param)
        if current_index < 0:
            return None
        return self._get_string(base_param + current_index) or None

    def _get_entity_name(self, base_param: int, index: int) -> str:
        """Get the name of the entity (engine, voice, language, subengine) at the specified index."""
        return self._get_string(base_param + index)

    def _iter_entities(
        self, base_param: int, entity_cls: type, available_check: Any = None
    ) -> Iterator[Any]:
        """Generic generator for iterating over entities (engine, voice, language, subengine)."""
        for index in range(self.MAX_ENTITIES):
            name = self._get_entity_name(base_param, index)
            if not name:
                return
            if available_check:
                available = available_check(index)
                yield entity_cls(index, name, available)
            else:
                yield entity_cls(index=index, name=name)

    def _iter_engines(self) -> Iterator[_Engine]:
        return self._iter_entities(
            _SpeechParam.ENGINE, _Engine, self._is_engine_available
        )

    def _iter_voices(self) -> Iterator[_Voice]:
        return self._iter_entities(_SpeechParam.VOICE, _Voice)

    def _iter_languages(self) -> Iterator[_Language]:
        return self._iter_entities(_SpeechParam.LANGUAGE, _Language)

    def _iter_subengines(self) -> Iterator[_SubEngine]:
        return self._iter_entities(_SpeechParam.SUBENGINE, _SubEngine)

    def _set_entity_by_name(
        self, value: str, entity_name: str, iter_func: Any, param: int
    ) -> None:
        """Set the current entity (engine, voice, language, subengine) by name."""
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")
        for entity in iter_func():
            if entity.name == value:
                self._set_value(param, entity.index)
                return
        match self._errors:
            case ErrorsMode.IGNORE:
                return
            case ErrorsMode.WARN:
                warn(
                    f"{entity_name} '{value}' not found or not available.",
                    VocaBrailleWarning,
                )
            case ErrorsMode.RAISE:
                raise ValueError(f"{entity_name} '{value}' not found or not available.")

    @property
    def supported_engines(self) -> list[str]:
        """List of all supported speech engines."""
        return [engine.name for engine in self._iter_engines()]

    @property
    def available_engines(self) -> list[str]:
        """List of available speech engines."""
        return [engine.name for engine in self._iter_engines() if engine.available]

    @property
    def engine(self) -> str | None:
        """Get the currently used speech engine."""
        return self._get_current_entity_name(_SpeechParam.ENGINE)

    @engine.setter
    def engine(self, value: str) -> None:
        """Set the current speech engine by name."""
        self._set_entity_by_name(
            value, "Engine", self._iter_engines, _SpeechParam.ENGINE
        )

    def reset_engine(self) -> None:
        """Reset the current speech engine to the default automatic detection."""
        self._set_value(_SpeechParam.ENGINE, -1)

    def is_auto_engine(self) -> bool:
        """Check if the automatic engine selection is enabled.

        Query if default automatic detection is used or not
        SP_AUTO_ENGINE = 0xFFFE,
        """
        return bool(self._get_value(_SpeechParam.AUTO_ENGINE))

    """
    Enable or disable specific OS speech engines that can in principle never fail, 
    such as SAPI5 on windows. 
    0 means disabled, any other value means enabled. 
    This parameter is disabled by default.
    """

    @property
    def native_speech(self) -> bool:
        """Check if native speech is enabled."""
        return bool(self._get_value(_SpeechParam.ENABLE_NATIVE_SPEECH))

    @native_speech.setter
    def native_speech(self, value: bool) -> None:
        """Enable or disable native speech."""
        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean.")
        self._set_value(_SpeechParam.ENABLE_NATIVE_SPEECH, int(value))

    """
    Some engines or subengines may give access to additionnal specific parameters
    Engine wrapper devloppers shouldn't use a parameter identifier below this value,
    to ensure that there wont be any conflict with a standard parameter (one of the above)
    SP_USER_PARAM = 0x1000000
    """

    def get_user_param(self, param_id: int) -> int:
        """Get a user-defined parameter value."""
        raise NotImplementedError("User-defined parameters are not implemented yet.")

    ##### Voice
    """Voice specific to the current engine.
    Some engines supports different voices. 
    Screen readers usually do not provite that in their API, 
    but multiple voices can be installed into OS specific engines such as SAPI5. 
    This parameter is used to get or set the current voice (0-based index), 
    or to query for voices names.
    + use speechGetValue with this parameter to query the currently selected voice, as a 0-based index
    + Use speechSetValue with this parameter to set the current voice, as a 0-based index
    + use speechGetString with this parameter + n to retriev the voice name of the nth 0-based index voice, i.e. speechGetString(SP_VOICE+5) to retriev the name of the 6th voice. You can iterate starting at 0 until you get NULL to discover how many voices the current engine has.
    """

    @property
    def available_voices(self) -> list[str]:
        """List of available voices for the current engine."""
        return [voice.name for voice in self._iter_voices()]

    @property
    def voice(self) -> str | None:
        """Get the currently selected voice."""
        return self._get_current_entity_name(_SpeechParam.VOICE)

    @voice.setter
    def voice(self, value: str) -> None:
        """Set the current voice by name."""
        self._set_entity_by_name(value, "Voice", self._iter_voices, _SpeechParam.VOICE)

    ##### Language
    """Same principle as voices but for languages. 
    Some engines allow to change dynamically the speech language. 
    Note that the list of available voices may change following a language change, 
    depending on how the engine works.
    """

    @property
    def available_languages(self) -> list[str]:
        """List of available languages for the current engine."""
        return [lang.name for lang in self._iter_languages()]

    @property
    def language(self) -> str | None:
        """Get the currently selected language."""
        return self._get_current_entity_name(_SpeechParam.LANGUAGE)

    @language.setter
    def language(self, value: str) -> None:
        """Set the current language by name."""
        self._set_entity_by_name(
            value, "Language", self._iter_languages, _SpeechParam.LANGUAGE
        )

    ##### Subengine
    """Same principle as voices and languages but for sub-engines. 
    Some engines are in fact wrappers that can handle a collection of engines, 
    such as speech dispatcher on linux. 
    This parameter allow to select an engine out of an engine wrapper. 
    In general, languages and voices available changes following a sub-engine change.
    """

    @property
    def available_subengines(self) -> list[str]:
        """List of available sub-engines for the current engine."""
        return [subengine.name for subengine in self._iter_subengines()]

    @property
    def subengine(self) -> str | None:
        """Get the currently selected sub-engine."""
        return self._get_current_entity_name(_SpeechParam.SUBENGINE)

    @subengine.setter
    def subengine(self, value: str) -> None:
        """Set the current sub-engine by name."""
        self._set_entity_by_name(
            value, "Subengine", self._iter_subengines, _SpeechParam.SUBENGINE
        )

    ##### Volume

    def supports_volume(self) -> bool:
        """Check if volume control is supported."""
        return bool(self._get_value(_SpeechParam.VOLUME_SUPPORTED))

    @property
    def volume(self) -> int:
        """Get the current volume level."""
        res = self._handle_unsupported(self.supports_volume(), "Volume control", 0)
        if res is not None:
            return res
        return self._get_value(_SpeechParam.VOLUME)

    @volume.setter
    def volume(self, value: int) -> None:
        res = self._handle_unsupported(self.supports_volume(), "Volume control", None)
        if res is not None:
            return
        if self._validate_value(value, "Volume", self.min_volume, self.max_volume):
            self._set_value(_SpeechParam.VOLUME, value)

    @property
    def min_volume(self) -> int:
        res = self._handle_unsupported(self.supports_volume(), "Volume control", 0)
        if res is not None:
            return res
        return self._get_value(_SpeechParam.VOLUME_MIN)

    @property
    def max_volume(self) -> int:
        res = self._handle_unsupported(self.supports_volume(), "Volume control", 100)
        if res is not None:
            return res
        return self._get_value(_SpeechParam.VOLUME_MAX)

    ##### Speech Rate

    def supports_rate(self) -> bool:
        """Check if speech rate control is supported."""
        return bool(self._get_value(_SpeechParam.RATE_SUPPORTED))

    @property
    def rate(self) -> int:
        res = self._handle_unsupported(self.supports_rate(), "Speech rate control", 0)
        if res is not None:
            return res
        return self._get_value(_SpeechParam.RATE)

    @rate.setter
    def rate(self, value: int) -> None:
        res = self._handle_unsupported(
            self.supports_rate(), "Speech rate control", None
        )
        if res is not None:
            return
        if self._validate_value(value, "Rate", self.min_rate, self.max_rate):
            self._set_value(_SpeechParam.RATE, value)

    @property
    def min_rate(self) -> int:
        res = self._handle_unsupported(self.supports_rate(), "Speech rate control", 0)
        if res is not None:
            return res
        return self._get_value(_SpeechParam.RATE_MIN)

    @property
    def max_rate(self) -> int:
        res = self._handle_unsupported(self.supports_rate(), "Speech rate control", 100)
        if res is not None:
            return res
        return self._get_value(_SpeechParam.RATE_MAX)

    ###### Pitch

    def supports_pitch(self) -> bool:
        """Check if pitch control is supported."""
        return bool(self._get_value(_SpeechParam.PITCH_SUPPORTED))

    @property
    def pitch(self) -> int:
        res = self._handle_unsupported(self.supports_pitch(), "Pitch control", 0)
        if res is not None:
            return res
        return self._get_value(_SpeechParam.PITCH)

    @pitch.setter
    def pitch(self, value: int) -> None:
        res = self._handle_unsupported(self.supports_pitch(), "Pitch control", None)
        if res is not None:
            return
        if self._validate_value(value, "Pitch", self.min_pitch, self.max_pitch):
            self._set_value(_SpeechParam.PITCH, value)

    @property
    def min_pitch(self) -> int:
        res = self._handle_unsupported(self.supports_pitch(), "Pitch control", 0)
        if res is not None:
            return res
        return self._get_value(_SpeechParam.PITCH_MIN)

    @property
    def max_pitch(self) -> int:
        res = self._handle_unsupported(self.supports_pitch(), "Pitch control", 100)
        if res is not None:
            return res
        return self._get_value(_SpeechParam.PITCH_MAX)

    ##### Inflexion

    def supports_inflexion(self) -> bool:
        """Check if inflexion control is supported."""
        return bool(self._get_value(_SpeechParam.INFLEXION_SUPPORTED))

    @property
    def inflexion(self) -> int:
        res = self._handle_unsupported(
            self.supports_inflexion(), "Inflexion control", 0
        )
        if res is not None:
            return res
        return self._get_value(_SpeechParam.INFLEXION)

    @inflexion.setter
    def inflexion(self, value: int) -> None:
        res = self._handle_unsupported(
            self.supports_inflexion(), "Inflexion control", None
        )
        if res is not None:
            return
        if self._validate_value(
            value, "Inflexion", self.min_inflexion, self.max_inflexion
        ):
            self._set_value(_SpeechParam.INFLEXION, value)

    @property
    def min_inflexion(self) -> int:
        res = self._handle_unsupported(
            self.supports_inflexion(), "Inflexion control", 0
        )
        if res is not None:
            return res
        return self._get_value(_SpeechParam.INFLEXION_MIN)

    @property
    def max_inflexion(self) -> int:
        res = self._handle_unsupported(
            self.supports_inflexion(), "Inflexion control", 100
        )
        if res is not None:
            return res
        return self._get_value(_SpeechParam.INFLEXION_MAX)

    ##### Pause

    def supports_pause(self) -> bool:
        """Check if pause control is supported."""
        return bool(self._get_value(_SpeechParam.PAUSE_SUPPORTED))

    @property
    def pause(self) -> bool:
        res = self._handle_unsupported(self.supports_pause(), "Pause control", False)
        if res is not None:
            return res
        return bool(self._get_value(_SpeechParam.PAUSED))

    @pause.setter
    def pause(self, value: bool) -> None:
        res = self._handle_unsupported(self.supports_pause(), "Pause control", None)
        if res is not None:
            return
        self._set_value(_SpeechParam.PAUSED, int(value))

    def toggle_pause(self) -> None:
        """Toggle the pause state of the speech engine."""
        current_state = self.pause
        self.pause = not current_state

    ###### Busy

    def supports_busy(self) -> bool:
        """Check if busy status is supported."""
        return bool(self._get_value(_SpeechParam.BUSY_SUPPORTED))

    def is_busy(self) -> bool:
        res = self._handle_unsupported(
            self.supports_busy(), "Busy status control", False
        )
        if res is not None:
            return res
        return bool(self._get_value(_SpeechParam.BUSY))

    ##### Wait
    """Wait for the speech to finish. 
    Use speechGetValue with this parameter to wait indefinitely for the current speech to finish. 
    Use speechSetValue with a number of milliseconds to wait at most the specified time for the current speech to finish.
    """

    def supports_wait(self) -> bool:
        """Check if wait control is supported."""
        return bool(self._get_value(_SpeechParam.WAIT_SUPPORTED))

    def wait(self, milliseconds: int = 0) -> None:
        res = self._handle_unsupported(self.supports_wait(), "Wait control", None)
        if res is not None:
            return
        if not isinstance(milliseconds, int) or milliseconds < 0:
            raise ValueError("Milliseconds must be a non-negative integer.")
        if milliseconds == 0:  # Wait indefinitely
            self._get_value(_SpeechParam.WAIT)
        else:
            self._set_value(_SpeechParam.WAIT, milliseconds)

    ###### Speak
    def say(self, msg: Union[str, bytes], interrupt: bool = True) -> int:
        """Send a message to be spoken, automatically handling Unicode or ANSI."""
        if isinstance(msg, (bytes, bytearray)):
            return self._uspeech.speechSayA(msg, int(interrupt))
        return self._uspeech.speechSay(msg, int(interrupt))

    def braille(self, msg: Union[str, bytes]) -> int:
        """Send a message to be displayed on braille, automatically handling Unicode or ANSI."""
        if isinstance(msg, (bytes, bytearray)):
            return self._uspeech.brailleDisplayA(msg)
        return self._uspeech.brailleDisplay(msg)

    def say_and_braille(self, msg: Union[str, bytes], interrupt: bool = True) -> None:
        """Send a message to be spoken and displayed on braille, automatically handling Unicode or ANSI."""
        self.say(msg, interrupt)
        self.braille(msg)

    def stop(self) -> int:
        """Immediately stop speaking and clear the queue of pending messages
        export int speechStop (void) ;
        """
        return self._uspeech.speechStop()

    def _handle_unsupported(self, supported: bool, feature: str, default: Any) -> Any:
        """Handle unsupported feature according to error mode."""
        if supported:
            return None
        match self._errors:
            case ErrorsMode.IGNORE:
                return default
            case ErrorsMode.WARN:
                warn(f"{feature} is not supported.", VocaBrailleWarning)
                return default
            case ErrorsMode.RAISE:
                raise ValueError(f"{feature} is not supported.")
