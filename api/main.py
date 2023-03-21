from typing import Union
from db.models import *
from db.database import engine, create_db_and_tables
from sqlmodel import Session, select
from fastapi import FastAPI, HTTPException, Depends

def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()

# === Startup Function ===
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
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
    players = session.exec(select(Player)).all()
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
    teams = session.exec(select(StatLine.opponent).distinct()).all()
    return teams
#endregion Team

#region Games
@app.get("/games/")
def read_games(*, session: Session = Depends(get_session)):
    games = session.exec(select(StatLine.date, StatLine.team, StatLine.opponent).distinct(StatLine.date)).all()
    return games
#endregion Games

#region Seasons
@app.get("/seasons/")
def read_seasons(*, session: Session = Depends(get_session)):
    seasons = session.exec(select(StatLine.season).distinct()).all()
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

#region Entity Stat Endpoints
""" 
Want to follow the syntax of /stats/{entity}/{entity.id}
That way we can get the data of an individual player, team, game, season but for the entity
For example /stats/players/2 will return all the statlines for the player with the matching ID
Can let the front end handle the aggregation and math. That should hopefully reduce the need for any 
preprocessing or query strings in the URL.
"""

# @app.get("/stats/players/{player_id}", response_model=PlayerWithStatLines)
# def get_players_stats(*, session: Session = Depends(get_session), player_id: UUID):
#     pass

# @app.get("/stats/teams/{team_id}", response_model=TeamWithStatLines)
# def get_teams_stats(*, session: Session = Depends(get_session), team_id: UUID):
#     pass

# @app.get("/stats/seasons/{season_id}", response_model=SeasonWithStatLines)
# def get_seasons_stats(*, session: Session = Depends(get_session), season_id: UUID):
#     pass

# @app.get("/stats/games/{game_id}", response_model=GameWithStatLines)
# def get_games_stats(*, session: Session = Depends(get_session), game_id: UUID):
#     pass

#endregion Entity Stat Endpoints