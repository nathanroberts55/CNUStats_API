from typing import List, Set, Optional
from uuid import UUID, uuid4
import datetime
from enum import Enum, IntEnum
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint


# === Choices as Enums ===
class ClassEnum(str, Enum):
    freshman = "Fr."
    sophomore = "So."
    junior = "Jr."
    senior = "Sr."
    graduate = "Gr."


class PositionEnum(str, Enum):
    point_guard = "PG"
    shooting_guard = "SG"
    small_forward = "SF"
    power_forward = "PF"
    center = "C"


# === Models ===


# === Stat Line Models ===
class StatLineBase(SQLModel):
    date: datetime.date
    team: str
    opponent: str
    season: str
    fgm: int = Field(default=0)
    fga: int = Field(default=0)
    fg_pct: float = Field(default=0.0)
    three_fgm: int = Field(default=0)
    three_fga: int = Field(default=0)
    three_pt_pct: float = Field(default=0.0)
    ftm: int = Field(default=0)
    fta: int = Field(default=0)
    ft_pct: float = Field(default=0.0)
    off_reb: int = Field(default=0)
    def_reb: int = Field(default=0)
    tot_reb: int = Field(default=0)
    pf: int = Field(default=0)
    ast: int = Field(default=0)
    to: int = Field(default=0)
    blk: int = Field(default=0)
    stl: int = Field(default=0)
    pts: int = Field(default=0)


class StatLine(StatLineBase, table=True):
    __tablename__ = "statLines"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())

    # Relationships
    player_id: Optional[UUID] = Field(default=None, foreign_key="players.id")


class StatLineCreate(StatLineBase):
    pass


class StatLineRead(StatLineBase):
    id: UUID


class StatLineUpdate(SQLModel):
    date: Optional[datetime.date] = None
    fgm: Optional[int] = None
    fga: Optional[int] = None
    fg_pct: Optional[float] = None
    three_fgm: Optional[int] = None
    three_fga: Optional[int] = None
    three_pt_pct: Optional[float] = None
    ftm: Optional[int] = None
    fta: Optional[int] = None
    ft_pct: Optional[float] = None
    off_reb: Optional[int] = None
    def_reb: Optional[int] = None
    tot_reb: Optional[int] = None
    pf: Optional[int] = None
    ast: Optional[int] = None
    to: Optional[int] = None
    blk: Optional[int] = None
    stl: Optional[int] = None
    pts: Optional[int] = None


# === Player Models ===
class PlayerBase(SQLModel):
    full_name: str
    class_name: ClassEnum
    position: PositionEnum
    height: str
    weight: str
    hometown_hs: str
    jersey_num: int


class Player(PlayerBase, table=True):
    __tablename__ = "players"
    __table_args__ = (UniqueConstraint("full_name", "hometown_hs"),)

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())

    # Relationships
    stats: Optional[List["StatLine"]] = Relationship()


class PlayerCreate(PlayerBase):
    pass


class PlayerRead(PlayerBase):
    id: UUID


class PlayerUpdate(SQLModel):
    full_name: Optional[str] = None
    class_name: Optional[ClassEnum] = None
    position: Optional[PositionEnum] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    hometown_hs: Optional[str] = None
    jersey_num: Optional[int] = None


# === Game Stats Model ===
class GameStatBase(SQLModel):
    three_fga: int
    three_fga_diff: int
    three_fgm: int
    three_fgm_diff: float
    three_pt_percent: float
    three_pt_percent_diff: float
    ast: int
    ast_diff: int
    blk: int
    blk_diff: int
    cnu_score: int
    date: datetime.date = Field(unique=True)
    day: int
    def_reb: int
    def_diff: int
    fg_percent: float
    fg_percent_diff: float
    fga: int
    fga_diff: int
    fgm: int
    fgm_diff: int
    ft_percent: float
    ft_percent_diff: float
    fta: int
    fta_diff: int
    ftm: int
    ftm_diff: int
    home: int
    month: int
    off_reb: int
    off_diff: int
    opp_three_fga: int
    opp_three_fgm: int
    opp_three_pt_percent: float
    opp_ast: int
    opp_blk: int
    opp_def: int
    opp_fg_percent: float
    opp_fga: int
    opp_fgm: int
    opp_ft_percent: float
    opp_fta: int
    opp_ftm: int
    opp_off_reb: int
    opp_pf: int
    opp_ppg_avg: float
    opp_pts: int
    opp_rb_avg: float
    opp_score: int
    opp_stl: int
    opp_turnover: int
    opp_tot_reb: int
    opponent: str
    overtime: int
    pf: int
    pf_diff: int
    ppg_avg: float
    pts: int
    ranked: int
    rb_avg: float
    season: str
    stl: int
    stl_diff: int
    turnover: int
    turnover_diff: int
    tot_reb: int
    tot_diff: int
    weekday: int
    win: int
    year: int


class GameStat(GameStatBase, table=True):
    __tablename__ = "gamestats"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())


class GameStatCreate(GameStatBase):
    pass


class GameStatRead(GameStatBase):
    id: UUID


# === Relational Model Views ===
class StatLineReadWithPlayer(StatLineRead):
    player_id: Optional[PlayerRead] = None


class PlayerWithStatLines(PlayerRead):
    stats: Optional[List[StatLineRead]] = []
