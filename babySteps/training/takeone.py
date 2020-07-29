from pathlib import Path
from rlbot.matchconfig.match_config import Team, PlayerConfig
from rlbottraining.common_exercises.bronze_goalie import BallRollingToGoalie

def make_default_playlist():
    exercises =  [
        BallRollingToGoalie("first training exercise")
    ]
    for e in exercises:
        e.match_config.player_configs = [
        PlayerConfig.bot_config(Path(__file__).absolute().parent.parent / 'babySteps.cfg',
            Team.BLUE)
        ]
    return exercises