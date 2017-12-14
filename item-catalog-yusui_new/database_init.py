from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import Category, Base, GameItem, User

engine = create_engine('sqlite:///categorygamewithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="kevin durant", email="kd@udacity.com")
session.add(User1)
session.commit()

# Create dummy categories
Category1 = Category(
    name="Role Playing",
    user_id=1
    )
session.add(Category1)
session.commit()

Category2 = Category(
    name="Sports",
    user_id=1
    )
session.add(Category2)
session.commit

Category3 = Category(
    name="Strategy",
    user_id=1
    )
session.add(Category3)
session.commit()

Category4 = Category(
    name="Action",
    user_id=1
    )
session.add(Category4)
session.commit()

Category5 = Category(
    name="Cell Phone",
    user_id=1
    )
session.add(Category5)
session.commit()

# Populate categories with games for testing purpose
game1 = GameItem(
    name="Diablo III",
    date=datetime.datetime.now(),
    description="Diablo III is a dungeon crawler action role-playing video \
    game developed and published by Blizzard Entertainment.",
    official_website="https://us.battle.net/d3/en/",
    category_id=1,
    user_id=1
    )
session.add(game1)
session.commit()

game2 = GameItem(
    name="World of Warcraft",
    date=datetime.datetime.now(),
    description="World of Warcraft is a massively multiplayer \
    online role-playing game released in 2004 by Blizzard Entertainment. \
    It is the fourth released game set in the fantasy Warcraft universe.",
    official_website="https://worldofwarcraft.com/",
    category_id=1,
    user_id=1
    )
session.add(game2)
session.commit()

game3 = GameItem(
    name="Final Fantacy VII",
    date=datetime.datetime.now(),
    description="Final Fantasy VII is a role-playing video \
    game developed by Square for the PlayStation console. \
    Released in 1997, it is the seventh main installment in \
    the Final Fantasy series.",
    official_website="finalfantasyviipc.com/",
    category_id=1,
    user_id=1)
session.add(game3)
session.commit()

game4 = GameItem(
    name="The Witcher III",
    date=datetime.datetime.now(),
    description="The Witcher 3: Wild Hunt is a 2015 action\
    role-playing video game developed and published by CD Projekt.",
    official_website="www.thewitcher.com/",
    category_id=1,
    user_id=1
    )
session.add(game4)
session.commit()

game5 = GameItem(
    name="The Elder Scrolls III",
    date=datetime.datetime.now(),
    description="The Elder Scrolls III: Tribunal is the first \
    expansion for Bethesda Game Studios' The Elder Scrolls III: Morrowind. \
    It takes place in the temple-city of Mournhold, the capital of Morrowind, \
    located in the larger city of Almalexia.",
    official_website="https://elderscrolls.bethesda.net/",
    category_id=1,
    user_id=1
    )
session.add(game5)
session.commit()

game6 = GameItem(
    name="NBA 2K17",
    date=datetime.datetime.now(),
    description="NBA 2K17 is a basketball simulation video \
    game developed by Visual Concepts and published by 2K Sports. \
    It is the 18th installment in the NBA 2K franchise and \
    the successor to NBA 2K16.",
    official_website="https://www.2k.com/games/nba-2k17",
    category_id=2,
    user_id=1)
session.add(game6)
session.commit()

game7 = GameItem(
    name="FIFA 17",
    date=datetime.datetime.now(),
    description="FIFA 17 is a sports video game in the FIFA \
    series developed and published by Electronic Arts, which \
    released in September 2016. This is the first FIFA game in \
    the series to use the Frostbite game engine.",
    official_website="www.futhead.com/17/",
    category_id=2,
    user_id=1)
session.add(game7)
session.commit()

game8 = GameItem(
    name="Candy Crush Saga",
    date=datetime.datetime.now(),
    description="Candy Crush Saga is a free-to-play match-three \
    puzzle video game released by King on April 12, 2012, for \
    Facebook; other versions for iOS, Android, Windows Phone, \
    and Windows 10 followed. It is a variation on their browser \
    game Candy Crush.",
    official_website="https://king.com/game/candycrush",
    category_id=5,
    user_id=1)
session.add(game8)
session.commit()

game9 = GameItem(
    name="Pokemon Go",
    date=datetime.datetime.now(),
    description="Pokemon Go is a free-to-play, location-based \
    augmented reality game developed by Niantic for iOS and \
    Android devices.",
    official_website="www.pokemongo.com/",
    category_id=5,
    user_id=1
    )
session.add(game9)
session.commit()

game10 = GameItem(
    name="Clash of Clans",
    date=datetime.datetime.now(),
    description="Clash of Clans is a freemium mobile strategy \
    video game developed and published by Finnish game developer \
    Supercell. The game was released for iOS platforms on \
    August 2, 2012, and on Google Play for Android on October 7, 2013.",
    official_website="https://clashofclans.com/",
    category_id=5,
    user_id=1
    )
session.add(game10)
session.commit()

game11 = GameItem(
    name="StarCraft II: Wings of Liberty is a military",
    date=datetime.datetime.now(),
    description="StarCraft II: Wings of Liberty is a military \
    science fiction real-time strategy video game developed and \
    published by Blizzard Entertainment. It was released worldwide\
    in July 2010 for Microsoft Windows and Mac OS X.",
    official_website="https://www.starcraft2.com/",
    category_id=3,
    user_id=1
    )
session.add(game11)
session.commit()

game12 = GameItem(
    name="Civilization V",
    date=datetime.datetime.now(),
    description="Sid Meier's Civilization V is a \
    4X video game in the Civilization series developed \
    by Firaxis Games. The game was released on Microsoft \
    Windows in September 2010, on OS X on November 23, 2010, \
    and on Linux on June 10, 2014.",
    official_website="www.civilization5.com/",
    category_id=3,
    user_id=1
    )
session.add(game12)
session.commit()

game13 = GameItem(
    name="Total War: Rome II",
    date=datetime.datetime.now(),
    description="Total War: Rome II is a strategy game \
    developed by The Creative Assembly and published by \
    Sega. It was released on 3 September 2013 for Microsoft \
    Windows and is the eighth standalone game in the Total \
    War series of video games.",
    official_website="https://www.totalwar.com/",
    category_id=3,
    user_id=1
    )
session.add(game13)
session.commit()

game14 = GameItem(
    name="Call of Duty: WWII",
    date=datetime.datetime.now(),
    description="Call of Duty: WWII is a first-person shooter \
    video game developed by Sledgehammer Games and published \
    by Activision.",
    official_website="https://www.callofduty.com/wwii",
    category_id=4,
    user_id=1
    )
session.add(game14)
session.commit()

game15 = GameItem(
    name="League of Legends",
    date=datetime.datetime.now(),
    description="League of Legends is a multiplayer online \
    battle arena video game developed and published by Riot \
    Games for Microsoft Windows and macOS.",
    official_website="https://na.leagueoflegends.com/",
    category_id=4,
    user_id=1)
session.add(game15)
session.commit()

print "added game items!"
