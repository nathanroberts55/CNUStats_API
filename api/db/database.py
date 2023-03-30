from sqlmodel import SQLModel, Session, select, create_engine
from .models import *
import random
from datetime import date, timedelta

# UIsing SQLite here but can easily use PostgreSQL by changing the url
sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

# The engine is the interface to our database so we can execute SQL commands
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


# using the engine we create the tables we need if they aren't already done
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_test_data():
    session = Session(engine)

    opponents = [
        "Mary Washington",
        "Marymount University",
        "Virginia Wesleyan University",
        "University of Mount Union",
        "Swathmore",
        "Salisbury University",
        "York College (PA)",
        "Lynchburg University",
    ]

    # Create Players
    player_ids = session.execute(select(Player.id)).all()

    if not player_ids:
        player_1 = Player(
            full_name="Nathan Roberts",
            class_name="Sr.",
            position="C",
            height="6'8",
            weight="230",
            hometown_hs="Fairfax, VA | Fairfax HS",
            jersey_num=0,
        )
        session.add(player_1)
        player_2 = Player(
            full_name="Tyler Femi",
            class_name="Sr.",
            position="PG",
            height="6'1",
            weight="215",
            hometown_hs="Chantilly, VA | Chantilly HS",
            jersey_num=10,
        )
        session.add(player_2)
        player_3 = Player(
            full_name="Spencer Marin",
            class_name="Sr.",
            position="C",
            height="6'9",
            weight="230",
            hometown_hs="Springfield, VA | West Springfield HS",
            jersey_num=14,
        )
        session.add(player_3)
        player_4 = Player(
            full_name="Tim Daly",
            class_name="Sr.",
            position="C",
            height="6'6",
            weight="230",
            hometown_hs="Midlothian, VA | James River HS",
            jersey_num=44,
        )
        session.add(player_4)
        player_5 = Player(
            full_name="Ben Watkins",
            class_name="Sr.",
            position="C",
            height="6'7",
            weight="230",
            hometown_hs="Richmond, VA | Colonial Forge HS",
            jersey_num=52,
        )
        session.add(player_5)

        session.commit()

        # Get the Players ID's
        player_ids = session.execute(select(Player.id)).all()

    # Create Stats for the Players
    if not session.execute(select(StatLine.id)).all():
        for i in range(100):
            year = random.randint(2012, 2022)
            game_date = date.today() - timedelta(days=i)
            rand_team = "Christopher Newport University"
            rand_opponent = opponents[random.randint(0, 7)]
            season = f"{year}-{year+1}"
            fgm = random.randint(0, 15)
            fga = random.randint(15, 30)
            fg_pct = fgm / fga
            three_fgm = random.randint(0, 8)
            three_fga = random.randint(8, 20)
            three_pt_pct = three_fgm / three_fga
            ftm = random.randint(0, 8)
            fta = random.randint(8, 20)
            ft_pct = ftm / fta
            off_reb = random.randint(0, 7)
            def_reb = random.randint(0, 7)
            tot_reb = random.randint(0, 7)
            pf = random.randint(0, 5)
            ast = random.randint(0, 7)
            to = random.randint(0, 7)
            blk = random.randint(0, 7)
            stl = random.randint(0, 7)
            pts = random.randint(0, 45)
            player_num = random.randint(0, 4)
            player_id = player_ids[player_num][0]

            stat = StatLine(
                date=game_date,
                team=rand_team,
                opponent=rand_opponent,
                season=season,
                fgm=fgm,
                fga=fga,
                fg_pct=fg_pct,
                three_fgm=three_fgm,
                three_fga=three_fga,
                three_pt_pct=three_pt_pct,
                ftm=ftm,
                fta=fta,
                ft_pct=ft_pct,
                off_reb=off_reb,
                def_reb=def_reb,
                tot_reb=tot_reb,
                pf=pf,
                ast=ast,
                to=to,
                blk=blk,
                stl=stl,
                pts=pts,
                player_id=player_id,
            )

            session.add(stat)
        session.commit()


if __name__ == "__main__":
    # creates the table if this file is run independently, as a script
    create_db_and_tables()
