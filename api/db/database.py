from sqlmodel import SQLModel, Session, create_engine
from .models import *
import random
from datetime import date
# UIsing SQLite here but can easily use PostgreSQL by changing the url
sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

# The engine is the interface to our database so we can execute SQL commands
engine = create_engine(sqlite_url, echo=True,  connect_args=connect_args)


# using the engine we create the tables we need if they aren't already done
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def create_test_data():
    session = Session(engine)
    
    opponents = [
        'Mary Washington',
        'Marymount University',
        'Virginia Wesleyan University',
        'University of Mount Union',
        'Swathmore',
        'Salisbury University',
        'York College (PA)',
        'Lynchburg University'
        ]
    
    for i in range(50):
        game_date = date.today()
        rand_team = "Christopher Newport University"
        rand_opponent = opponents[random.randint(0, 7)]
        season = "2021-2022"
        fgm = random.randint(0, 20)
        fga = random.randint(1, 20)
        fg_pct = fgm/fga
        three_fgm = random.randint(0, 10)
        three_fga = random.randint(1, 10)
        three_pt_pct = three_fgm/three_fga
        ftm = random.randint(0, 10)
        fta = random.randint(1, 10)
        ft_pct = ftm/fta
        off_reb = random.randint(0, 7)
        def_reb = random.randint(0, 7)
        tot_reb = random.randint(0, 7)
        pf = random.randint(0, 5)
        ast = random.randint(0, 7)
        to = random.randint(0, 7)
        blk = random.randint(0, 7)
        stl = random.randint(0, 7)
        pts = random.randint(0, 45)
        
        stat = StatLine(
            date = game_date,
            team = rand_team,
            opponent = rand_opponent,
            season = season,
            fgm = fgm,
            fga = fga,
            fg_pct = fg_pct,
            three_fgm = three_fgm,
            three_fga = three_fga,
            three_pt_pct = three_pt_pct,
            ftm = ftm,
            fta = fta,
            ft_pct = ft_pct,
            off_reb = off_reb,
            def_reb = def_reb,
            tot_reb = tot_reb,
            pf = pf,
            ast = ast,
            to = to,
            blk = blk,
            stl = stl,
            pts = pts
        )
        
        session.add(stat)
    session.commit()
    
    
if __name__ == '__main__':
    # creates the table if this file is run independently, as a script
    create_db_and_tables()