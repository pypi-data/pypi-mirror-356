from dataclasses import dataclass
from datetime import datetime
from typing import Any, MutableMapping, Sequence, Union

from maimai_py.enums import *
from maimai_py.exceptions import *
from maimai_py.utils import UNSET, _UnsetSentinel


@dataclass()
class Song:
    id: int
    title: str
    artist: str
    genre: Genre
    bpm: int
    map: Union[str, None]
    version: int
    rights: Union[str, None]
    aliases: Union[list[str], None]
    disabled: bool
    difficulties: "SongDifficulties"

    def get_difficulty(self, type: SongType, level_index: Union[LevelIndex, None]) -> Union["SongDifficulty", None]:
        if type == SongType.DX:
            return next((diff for diff in self.difficulties.dx if diff.level_index == level_index), None)
        if type == SongType.STANDARD:
            return next((diff for diff in self.difficulties.standard if diff.level_index == level_index), None)
        if type == SongType.UTAGE:
            return next(iter(self.difficulties.utage), None)


@dataclass()
class SongDifficulties:
    standard: list["SongDifficulty"]
    dx: list["SongDifficulty"]
    utage: list["SongDifficultyUtage"]

    def _get_children(self, song_type: Union[SongType, _UnsetSentinel] = UNSET) -> Sequence["SongDifficulty"]:
        if song_type == UNSET:
            return self.standard + self.dx + self.utage
        return self.dx if song_type == SongType.DX else self.standard if song_type == SongType.STANDARD else self.utage

    def _get_divingfish_ids(self, id: int) -> set[int]:
        ids = set()
        for difficulty in self._get_children():
            ids.add(difficulty._get_divingfish_id(id))
        return ids


@dataclass()
class CurveObject:
    sample_size: int
    fit_level_value: float
    avg_achievements: float
    stdev_achievements: float
    avg_dx_score: float
    rate_sample_size: dict[RateType, int]
    fc_sample_size: dict[FCType, int]


@dataclass()
class SongDifficulty:
    type: SongType
    level: str
    level_value: float
    level_index: LevelIndex
    note_designer: str
    version: int
    tap_num: int
    hold_num: int
    slide_num: int
    touch_num: int
    break_num: int
    curve: Union[CurveObject, None]

    def _get_divingfish_id(self, id: int) -> int:
        if id < 0 or id > 9999:
            raise ValueError("Invalid song ID")
        if self.type == SongType.DX:
            return id + 10000
        elif self.type == SongType.UTAGE:
            return id + 100000
        return id


@dataclass()
class SongDifficultyUtage(SongDifficulty):
    kanji: str
    description: str
    is_buddy: bool


@dataclass()
class SongAlias:
    """@private"""

    song_id: int
    aliases: list[str]


@dataclass()
class PlayerIdentifier:
    qq: Union[int, None] = None
    username: Union[str, None] = None
    friend_code: Union[int, None] = None
    credentials: Union[str, MutableMapping[str, str], None] = None

    def __post_init__(self):
        if self.qq is None and self.username is None and self.friend_code is None and self.credentials is None:
            raise InvalidPlayerIdentifierError("At least one of the following must be provided: qq, username, friend_code, credentials")

    def _as_diving_fish(self) -> dict[str, Any]:
        if self.qq:
            return {"qq": str(self.qq)}
        elif self.username:
            return {"username": self.username}
        elif self.friend_code:
            raise InvalidPlayerIdentifierError("Friend code is not applicable for Diving Fish")
        else:
            raise InvalidPlayerIdentifierError("No valid identifier provided")

    def _as_lxns(self) -> str:
        if self.friend_code:
            return str(self.friend_code)
        elif self.qq:
            return f"qq/{str(self.qq)}"
        elif self.username:
            raise InvalidPlayerIdentifierError("Username is not applicable for LXNS")
        else:
            raise InvalidPlayerIdentifierError("No valid identifier provided")


@dataclass()
class PlayerItem:
    @staticmethod
    def _namespace() -> str:
        raise NotImplementedError


@dataclass()
class PlayerTrophy(PlayerItem):
    id: int
    name: str
    color: str

    @staticmethod
    def _namespace():
        return "trophies"


@dataclass()
class PlayerIcon(PlayerItem):
    id: int
    name: str
    description: Union[str, None] = None
    genre: Union[str, None] = None

    @staticmethod
    def _namespace():
        return "icons"


@dataclass()
class PlayerNamePlate(PlayerItem):
    id: int
    name: str
    description: Union[str, None] = None
    genre: Union[str, None] = None

    @staticmethod
    def _namespace():
        return "nameplates"


@dataclass()
class PlayerFrame(PlayerItem):
    id: int
    name: str
    description: Union[str, None] = None
    genre: Union[str, None] = None

    @staticmethod
    def _namespace():
        return "frames"


@dataclass()
class PlayerPartner(PlayerItem):
    id: int
    name: str

    @staticmethod
    def _namespace():
        return "partners"


@dataclass()
class PlayerChara(PlayerItem):
    id: int
    name: str

    @staticmethod
    def _namespace():
        return "charas"


@dataclass()
class PlayerRegion:
    region_id: int
    region_name: str
    play_count: int
    created_at: datetime


@dataclass()
class Player:
    name: str
    rating: int


@dataclass()
class DivingFishPlayer(Player):
    nickname: str
    plate: str
    additional_rating: int


@dataclass()
class LXNSPlayer(Player):
    friend_code: int
    course_rank: int
    class_rank: int
    star: int
    frame: Union[PlayerFrame, None]
    icon: Union[PlayerIcon, None]
    trophy: Union[PlayerTrophy, None]
    name_plate: Union[PlayerNamePlate, None]
    upload_time: str


@dataclass()
class ArcadePlayer(Player):
    is_login: bool
    icon: Union[PlayerIcon, None]
    trophy: Union[PlayerTrophy, None]
    name_plate: Union[PlayerNamePlate, None]


@dataclass()
class AreaCharacter:
    name: str
    illustrator: str
    description1: str
    description2: str
    team: str
    props: dict[str, str]


@dataclass()
class AreaSong:
    id: Union[int, None]
    title: str
    artist: str
    description: str
    illustrator: Union[str, None]
    movie: Union[str, None]


@dataclass()
class Area:
    id: str
    name: str
    comment: str
    description: str
    video_id: str
    characters: list[AreaCharacter]
    songs: list[AreaSong]


@dataclass()
class Score:
    id: int
    level: str
    level_index: LevelIndex
    achievements: Union[float, None]
    fc: Union[FCType, None]
    fs: Union[FSType, None]
    dx_score: Union[int, None]
    dx_rating: Union[float, None]
    play_count: Union[int, None]
    rate: RateType
    type: SongType

    def _compare(self, other: Union["Score", None]) -> "Score":
        if other is None:
            return self
        if self.dx_score != other.dx_score:  # larger value is better
            return self if (self.dx_score or 0) > (other.dx_score or 0) else other
        if self.achievements != other.achievements:  # larger value is better
            return self if (self.achievements or 0) > (other.achievements or 0) else other
        if self.rate != other.rate:  # smaller value is better
            self_rate = self.rate.value if self.rate is not None else 100
            other_rate = other.rate.value if other.rate is not None else 100
            return self if self_rate < other_rate else other
        if self.fc != other.fc:  # smaller value is better
            self_fc = self.fc.value if self.fc is not None else 100
            other_fc = other.fc.value if other.fc is not None else 100
            return self if self_fc < other_fc else other
        if self.fs != other.fs:  # bigger value is better
            self_fs = self.fs.value if self.fs is not None else -1
            other_fs = other.fs.value if other.fs is not None else -1
            return self if self_fs > other_fs else other
        return self  # we consider they are equal

    def _join(self, other: Union["Score", None]) -> "Score":
        if other is not None:
            if self.level_index != other.level_index or self.type != other.type:
                raise ValueError("Cannot join scores with different level indexes or types")
            self.achievements = max(self.achievements or 0, other.achievements or 0)
            if self.fc != other.fc:
                self_fc = self.fc.value if self.fc is not None else 100
                other_fc = other.fc.value if other.fc is not None else 100
                selected_value = min(self_fc, other_fc)
                self.fc = FCType(selected_value) if selected_value != 100 else None
            if self.fs != other.fs:
                self_fs = self.fs.value if self.fs is not None else -1
                other_fs = other.fs.value if other.fs is not None else -1
                selected_value = max(self_fs, other_fs)
                self.fs = FSType(selected_value) if selected_value != -1 else None
            if self.rate != other.rate:
                selected_value = min(self.rate.value, other.rate.value)
                self.rate = RateType(selected_value)
        return self


@dataclass()
class PlateObject:
    song: Song
    levels: set[LevelIndex]
    scores: list[Score]
