from typing import Union
from db.models import *
from db.database import engine, create_db_and_tables, create_test_data
from sqlmodel import Session, func, select
from fastapi import FastAPI, HTTPException, Depends
import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = '..\.env'
load_dotenv(dotenv_path)
    
ENVIRONMENT = os.environ.get("ENVIRONMENT")

def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()

# === Startup Function ===
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
    if ENVIRONMENT == "local":
        print("Loading Test Data...")
        create_test_data()
    
    
    
# === API Information ===
@app.get("/")
def root():
    return {
        "Version": "0.0.1",
        "Author":"@naterobertstech",
        "LastUpdated": "2023-02-16"
        }

#region Player

@app.get("/players/")
def read_players(*, session: Session = Depends(get_session)):
    players = session.exec(select(Player).order_by(Player.full_name)).all()
    return players
    
@app.get("/players/{player_id}", response_model=PlayerRead)
def read_player(*, session: Session = Depends(get_session), player_id: UUID):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
    
@app.post('/players/', response_model=PlayerRead)
def create_player(*, session: Session = Depends(get_session), player: PlayerCreate):
    db_player = Player.from_orm(player)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player

@app.patch("/players/{player_id}", response_model=PlayerRead)
def update_player(*, session: Session = Depends(get_session),player_id: UUID, player: PlayerUpdate):
    db_player = session.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    player_data = player.dict(exclude_unset=True)
    for key, value in player_data.items():
        setattr(db_player, key, value)
    db_player.last_modified = datetime.datetime.utcnow()
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player
#endregion Player

#region Team
@app.get("/teams/")
def read_team(*, session: Session = Depends(get_session)):
    teams = session.exec(select(StatLine.opponent).distinct().order_by(StatLine.opponent)).all()
    return teams
#endregion Team

#region Games
@app.get("/games/")
def read_games(*, session: Session = Depends(get_session)):
    games = session.exec(
        select(StatLine.date, StatLine.team, StatLine.opponent)
        .distinct(StatLine.date)
        .order_by(StatLine.date)
        ).all()
    return games
#endregion Games

#region Seasons
@app.get("/seasons/")
def read_seasons(*, session: Session = Depends(get_session)):
    seasons = session.exec(select(StatLine.season).distinct().order_by(StatLine.season)).all()
    return seasons

#endregion Seasons

#region Stats
@app.get("/stats/")
def read_statline(*, session: Session = Depends(get_session)):
    teams = session.exec(select(StatLine)).all()
    return teams

@app.post('/stats/', response_model=StatLineRead)
def create_statline(*, session: Session = Depends(get_session), statline: StatLineCreate):
    db_statline = StatLine.from_orm(statline)
    session.add(db_statline)
    session.commit()
    session.refresh(db_statline)
    return db_statline

@app.patch("/stats/{statline_id}", response_model=StatLineRead)
def update_statline(*, session: Session = Depends(get_session),statline_id: UUID, statline: StatLineUpdate):
    db_statline = session.get(StatLine, statline_id)
    if not db_statline:
        raise HTTPException(status_code=404, detail="statline not found")
    statline_data = statline.dict(exclude_unset=True)
    for key, value in statline_data.items():
        setattr(db_statline, key, value)
    db_statline.last_modified = datetime.datetime.utcnow()
    session.add(db_statline)
    session.commit()
    session.refresh(db_statline)
    return db_statline

#region Stats Player
@app.get("/stats/player")
def get_all_stats_all_players(*, session: Session = Depends(get_session)):
    """
    Endpoint that returns the aggregated stats of each CNU player.
    """
    player_stats = session.exec(
        select(
            Player.full_name,
            StatLine.player_id,
            func.sum(StatLine.ftm).label('ftm'), 
            func.sum(StatLine.fta).label('fta'),
            func.avg(StatLine.ft_pct).label('ft_pct'),
            func.sum(StatLine.fga).label('fga'),
            func.sum(StatLine.fgm).label('fgm'),
            func.avg(StatLine.fg_pct).label('fg_pct'),
            func.sum(StatLine.three_fga).label('three_fga'),
            func.sum(StatLine.three_fgm).label('three_fgm'),
            func.avg(StatLine.three_pt_pct).label('three_pt_pct'),
            func.sum(StatLine.off_reb).label('off_reb'),
            func.sum(StatLine.def_reb).label('def_reb'),
            func.sum(StatLine.tot_reb).label('tot_reb'),
            func.sum(StatLine.pf).label('pf'),
            func.sum(StatLine.ast).label('ast'),
            func.sum(StatLine.to).label('to'),
            func.sum(StatLine.blk).label('blk'),
            func.sum(StatLine.stl).label('stl'),
            func.sum(StatLine.pts).label('pts'),
            )
        .join(Player)
        .group_by(Player.full_name)
        ).all()
    
    return player_stats

@app.get("/stats/players/{player_id}")
def get_all_stats_by_player(*, session: Session = Depends(get_session),player_id: UUID):
    """Endpoint that returns the stats of an individual CNU player as found by the players ID.

    Args:
        player_id (UUID): UUID unique to the player that is being looked for
    """
    player_stats = session.exec(
        select(
            Player.full_name,
            StatLine.player_id,
            func.sum(StatLine.ftm).label('ftm'), 
            func.sum(StatLine.fta).label('fta'),
            func.avg(StatLine.ft_pct).label('ft_pct'),
            func.sum(StatLine.fga).label('fga'),
            func.sum(StatLine.fgm).label('fgm'),
            func.avg(StatLine.fg_pct).label('fg_pct'),
            func.sum(StatLine.three_fga).label('three_fga'),
            func.sum(StatLine.three_fgm).label('three_fgm'),
            func.avg(StatLine.three_pt_pct).label('three_pt_pct'),
            func.sum(StatLine.off_reb).label('off_reb'),
            func.sum(StatLine.def_reb).label('def_reb'),
            func.sum(StatLine.tot_reb).label('tot_reb'),
            func.sum(StatLine.pf).label('pf'),
            func.sum(StatLine.ast).label('ast'),
            func.sum(StatLine.to).label('to'),
            func.sum(StatLine.blk).label('blk'),
            func.sum(StatLine.stl).label('stl'),
            func.sum(StatLine.pts).label('pts'),
            )
        .where(StatLine.player_id == player_id)
        .join(Player)
        .group_by(Player.full_name)
        ).all()
    
    if not player_stats:
        raise HTTPException(status_code=404, detail="Stats for Player requested not found")
    
    return player_stats
#endregion Stats Player

#region Stats Team
@app.get("/stats/teams")
def get_all_stats_all_teams(*, session: Session = Depends(get_session)):
    """
    Endpoint that returns the aggregated stats of CNU Players against each team.
    """
    # season_stats = (session.query(StatLine).group_by(StatLine.season).order_by(StatLine.season))
    team_stats = session.exec(
        select(
            StatLine.opponent,
            func.sum(StatLine.ftm).label('ftm'), 
            func.sum(StatLine.fta).label('fta'),
            func.avg(StatLine.ft_pct).label('ft_pct'),
            func.sum(StatLine.fga).label('fga'),
            func.sum(StatLine.fgm).label('fgm'),
            func.avg(StatLine.fg_pct).label('fg_pct'),
            func.sum(StatLine.three_fga).label('three_fga'),
            func.sum(StatLine.three_fgm).label('three_fgm'),
            func.avg(StatLine.three_pt_pct).label('three_pt_pct'),
            func.sum(StatLine.off_reb).label('off_reb'),
            func.sum(StatLine.def_reb).label('def_reb'),
            func.sum(StatLine.tot_reb).label('tot_reb'),
            func.sum(StatLine.pf).label('pf'),
            func.sum(StatLine.ast).label('ast'),
            func.sum(StatLine.to).label('to'),
            func.sum(StatLine.blk).label('blk'),
            func.sum(StatLine.stl).label('stl'),
            func.sum(StatLine.pts).label('pts'),
            )
        .group_by(StatLine.opponent)
        ).all()
    
    return team_stats

@app.get("/stats/teams/{team_name}")
def get_all_stats_by_team(*, session: Session = Depends(get_session),team_name: str):
    """Endpoint that returns all of the stats of CNU against an individual opponent as found by the team name.

    Args:
        team_name (str): string representation of the team (the opponent) that is being looked for
    """
    team_stats = session.exec(
        select(
            StatLine.opponent,
            func.sum(StatLine.ftm).label('ftm'), 
            func.sum(StatLine.fta).label('fta'),
            func.avg(StatLine.ft_pct).label('ft_pct'),
            func.sum(StatLine.fga).label('fga'),
            func.sum(StatLine.fgm).label('fgm'),
            func.avg(StatLine.fg_pct).label('fg_pct'),
            func.sum(StatLine.three_fga).label('three_fga'),
            func.sum(StatLine.three_fgm).label('three_fgm'),
            func.avg(StatLine.three_pt_pct).label('three_pt_pct'),
            func.sum(StatLine.off_reb).label('off_reb'),
            func.sum(StatLine.def_reb).label('def_reb'),
            func.sum(StatLine.tot_reb).label('tot_reb'),
            func.sum(StatLine.pf).label('pf'),
            func.sum(StatLine.ast).label('ast'),
            func.sum(StatLine.to).label('to'),
            func.sum(StatLine.blk).label('blk'),
            func.sum(StatLine.stl).label('stl'),
            func.sum(StatLine.pts).label('pts'),
            )
        .where(StatLine.opponent == team_name)
        .group_by(StatLine.opponent)
        ).all()
    
    if not team_stats:
        raise HTTPException(status_code=404, detail="Stats for Team requested not found")
    
    return team_stats
#endregion Stats Team

#region Stats Season
@app.get("/stats/season")
def get_all_stats_all_seasons(*, session: Session = Depends(get_session)):
    """
    Endpoint that returns the aggregated stats of CNU for each season.
    """
    # season_stats = (session.query(StatLine).group_by(StatLine.season).order_by(StatLine.season))
    season_stats = session.exec(
        select(
            StatLine.season,
            func.sum(StatLine.ftm).label('ftm'), 
            func.sum(StatLine.fta).label('fta'),
            func.avg(StatLine.ft_pct).label('ft_pct'),
            func.sum(StatLine.fga).label('fga'),
            func.sum(StatLine.fgm).label('fgm'),
            func.avg(StatLine.fg_pct).label('fg_pct'),
            func.sum(StatLine.three_fga).label('three_fga'),
            func.sum(StatLine.three_fgm).label('three_fgm'),
            func.avg(StatLine.three_pt_pct).label('three_pt_pct'),
            func.sum(StatLine.off_reb).label('off_reb'),
            func.sum(StatLine.def_reb).label('def_reb'),
            func.sum(StatLine.tot_reb).label('tot_reb'),
            func.sum(StatLine.pf).label('pf'),
            func.sum(StatLine.ast).label('ast'),
            func.sum(StatLine.to).label('to'),
            func.sum(StatLine.blk).label('blk'),
            func.sum(StatLine.stl).label('stl'),
            func.sum(StatLine.pts).label('pts'),
            )
        .group_by(StatLine.season)
        ).all()
    
    return season_stats

@app.get("/stats/season/{season_year}")
def get_all_stats_by_season(*, session: Session = Depends(get_session),season_year: str):
    """Endpoint that returns the stats of CNU in an individual season as found by the season years.

    Args:
        season_years (str): years of the season (e.g. 2012-2013) that is being looked for.
    """
    season_stats = session.exec(
        select(
            StatLine.season,
            func.sum(StatLine.ftm).label('ftm'), 
            func.sum(StatLine.fta).label('fta'),
            func.avg(StatLine.ft_pct).label('ft_pct'),
            func.sum(StatLine.fga).label('fga'),
            func.sum(StatLine.fgm).label('fgm'),
            func.avg(StatLine.fg_pct).label('fg_pct'),
            func.sum(StatLine.three_fga).label('three_fga'),
            func.sum(StatLine.three_fgm).label('three_fgm'),
            func.avg(StatLine.three_pt_pct).label('three_pt_pct'),
            func.sum(StatLine.off_reb).label('off_reb'),
            func.sum(StatLine.def_reb).label('def_reb'),
            func.sum(StatLine.tot_reb).label('tot_reb'),
            func.sum(StatLine.pf).label('pf'),
            func.sum(StatLine.ast).label('ast'),
            func.sum(StatLine.to).label('to'),
            func.sum(StatLine.blk).label('blk'),
            func.sum(StatLine.stl).label('stl'),
            func.sum(StatLine.pts).label('pts'),
            )
        .where(StatLine.season == season_year)
        .group_by(StatLine.season)
        ).all()
    
    if not season_stats:
        raise HTTPException(status_code=404, detail="Stats for Season requested not found")
    
    return season_stats
#endregion Stats Season

#region Stats Game
@app.get("/stats/games")
def get_all_stats_all_games(*, session: Session = Depends(get_session)):
    """
    Endpoint that returns the aggregated stats of CNU each game.
    """

    game_stats = session.exec(
        select(
            StatLine.date,
            StatLine.team,
            StatLine.opponent,
            func.sum(StatLine.ftm).label('ftm'), 
            func.sum(StatLine.fta).label('fta'),
            func.avg(StatLine.ft_pct).label('ft_pct'),
            func.sum(StatLine.fga).label('fga'),
            func.sum(StatLine.fgm).label('fgm'),
            func.avg(StatLine.fg_pct).label('fg_pct'),
            func.sum(StatLine.three_fga).label('three_fga'),
            func.sum(StatLine.three_fgm).label('three_fgm'),
            func.avg(StatLine.three_pt_pct).label('three_pt_pct'),
            func.sum(StatLine.off_reb).label('off_reb'),
            func.sum(StatLine.def_reb).label('def_reb'),
            func.sum(StatLine.tot_reb).label('tot_reb'),
            func.sum(StatLine.pf).label('pf'),
            func.sum(StatLine.ast).label('ast'),
            func.sum(StatLine.to).label('to'),
            func.sum(StatLine.blk).label('blk'),
            func.sum(StatLine.stl).label('stl'),
            func.sum(StatLine.pts).label('pts'),
            )
        .group_by(StatLine.date)
        ).all()
    
    return game_stats

@app.get("/stats/games/{game_date}")
def get_all_stats_by_game(*, session: Session = Depends(get_session),game_date: datetime.date):
    """Endpoint that returns the stats of CNU in an individual game as found by the game date.

    Args:
        game_date (str): date of the game that was played (e.g. 01-01-2012) that is being looked for.
    """
    game_stats = session.exec(
        select(
            StatLine.date,
            StatLine.team,
            StatLine.opponent,
            func.sum(StatLine.ftm).label('ftm'), 
            func.sum(StatLine.fta).label('fta'),
            func.avg(StatLine.ft_pct).label('ft_pct'),
            func.sum(StatLine.fga).label('fga'),
            func.sum(StatLine.fgm).label('fgm'),
            func.avg(StatLine.fg_pct).label('fg_pct'),
            func.sum(StatLine.three_fga).label('three_fga'),
            func.sum(StatLine.three_fgm).label('three_fgm'),
            func.avg(StatLine.three_pt_pct).label('three_pt_pct'),
            func.sum(StatLine.off_reb).label('off_reb'),
            func.sum(StatLine.def_reb).label('def_reb'),
            func.sum(StatLine.tot_reb).label('tot_reb'),
            func.sum(StatLine.pf).label('pf'),
            func.sum(StatLine.ast).label('ast'),
            func.sum(StatLine.to).label('to'),
            func.sum(StatLine.blk).label('blk'),
            func.sum(StatLine.stl).label('stl'),
            func.sum(StatLine.pts).label('pts'),
            )
        .where(StatLine.date == game_date)
        .group_by(StatLine.date)
        ).all()
    
    if not game_stats:
        raise HTTPException(status_code=404, detail="Stats for Game requested not found")
    
    return game_stats
#endregion Stats Game

#endregion Stats

#region Game Stats
@app.get("/gamestats/")
def read_gamestats(*, session: Session = Depends(get_session)):
    gamestats = session.exec(select(GameStat)).all()
    return gamestats

@app.get("/gamestats/{gamestats_id}", response_model=GameStatRead)
def read_gamestat(*, gamestat_id: int,  session: Session = Depends(get_session)):
    gamestat = session.get(GameStat, gamestat_id)
    if not gamestat:
        raise HTTPException(status_code=404, detail="Game Stat not found")
    return gamestat

@app.post("/gamestats/", response_model=GameStatRead)
def create_gamestat(*, gamestat: GameStatCreate, session: Session = Depends(get_session)):
    db_gamestat = GameStat.from_orm(gamestat)
    
    # If there is a similar record determined by the unique date, raise duplicate record error
    similar_game = session.exec(select(GameStat.date).where(GameStat.date == db_gamestat.date)).all()
    if similar_game:
        raise HTTPException(status_code=409, detail="Duplicate Game Stat Record")
    
    session.add(db_gamestat)
    session.commit()
    session.refresh(db_gamestat)
    return db_gamestat
#endregion Game Stats