from app import app, db, Game
from datetime import date

with app.app_context():
    # New games by genre
    games = [
# Add these to the games list:
        # More Fighting Games
        Game(
            title="Dragon Ball FighterZ",
            description="Spectacular anime fighting game with stunning visuals and fast-paced combat.",
            genre="Fighting",
            release_date=date(2018, 1, 26),
            developer="Arc System Works",
            publisher="Bandai Namco",
            rating=4.7
        ),
        Game(
            title="The King of Fighters XV",
            description="The legendary fighting game series returns with enhanced graphics and mechanics.",
            genre="Fighting",
            release_date=date(2022, 2, 17),
            developer="SNK",
            publisher="SNK",
            rating=4.6
        ),

        # More Racing Games
        Game(
            title="F1 23",
            description="The official Formula One racing simulation with all current teams and tracks.",
            genre="Racing",
            release_date=date(2023, 6, 16),
            developer="Codemasters",
            publisher="EA Sports",
            rating=4.7
        ),
        Game(
            title="Hot Wheels Unleashed",
            description="Race iconic Hot Wheels cars through creative tracks in this arcade racer.",
            genre="Racing",
            release_date=date(2021, 9, 30),
            developer="Milestone",
            publisher="Milestone",
            rating=4.6
        ),

        # More Strategy Games
        Game(
            title="XCOM 2",
            description="Lead Earth's resistance against alien occupation in this tactical strategy game.",
            genre="Strategy",
            release_date=date(2016, 2, 5),
            developer="Firaxis Games",
            publisher="2K Games",
            rating=4.8
        ),
        Game(
            title="Into the Breach",
            description="Tactical mech combat game from the makers of FTL.",
            genre="Strategy",
            release_date=date(2018, 2, 27),
            developer="Subset Games",
            publisher="Subset Games",
            rating=4.8
        ),

        # More Simulation Games
        Game(
            title="RimWorld",
            description="Manage a colony of survivors in this deep sci-fi simulation.",
            genre="Simulation",
            release_date=date(2018, 10, 17),
            developer="Ludeon Studios",
            publisher="Ludeon Studios",
            rating=4.9
        ),
        Game(
            title="Two Point Hospital",
            description="Build and manage your own hospital in this quirky management sim.",
            genre="Simulation",
            release_date=date(2018, 8, 30),
            developer="Two Point Studios",
            publisher="Sega",
            rating=4.7
        ),

        # More Platform Games
        Game(
            title="Celeste",
            description="Challenging platformer about climbing a mountain and overcoming personal demons.",
            genre="Platform",
            release_date=date(2018, 1, 25),
            developer="Extremely OK Games",
            publisher="Matt Makes Games",
            rating=4.9
        ),
        Game(
            title="A Hat in Time",
            description="Cute and colorful 3D platformer inspired by classic collectathons.",
            genre="Platform",
            release_date=date(2017, 10, 5),
            developer="Gears for Breakfast",
            publisher="Gears for Breakfast",
            rating=4.8
        ),

        # More FPS Games
        Game(
            title="Deep Rock Galactic",
            description="Cooperative FPS where space dwarves mine resources and fight alien threats.",
            genre="FPS",
            release_date=date(2020, 5, 13),
            developer="Ghost Ship Games",
            publisher="Coffee Stain Publishing",
            rating=4.8
        ),
        Game(
            title="Ultrakill",
            description="Lightning-fast retro FPS with stylish combat and scoring system.",
            genre="FPS",
            release_date=date(2020, 9, 3),
            developer="Arsi 'Hakita' Patala",
            publisher="New Blood Interactive",
            rating=4.9
        )

    ]
    
    db.session.add_all(games)
    db.session.commit()
