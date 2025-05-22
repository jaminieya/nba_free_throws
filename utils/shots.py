import pandas as pd
from nba_api.stats.endpoints import PlayByPlayV2

# Function to get the running count of shot attempts
def shot_number_up_to_event(game_id: str,
                            person_id: int,
                            action_number: int,
                            count_ft: bool = True) -> int:
    """
    Return the running count of all shot attempts (FG + FT or just FG) that
    `person_id` has taken in `game_id` up to and including `action_number`.
    """
    # Get the play-by-play data for the game
    df = PlayByPlayV2(game_id=game_id).get_data_frames()[0]

    # Filter the DataFrame to include only relevant columns
    df["EVENTNUM"] = df["EVENTNUM"].astype(int)
    df["PLAYER1_ID"] = pd.to_numeric(df["PLAYER1_ID"], errors="coerce").fillna(0).astype(int)

    # Filter the DataFrame to include all shots taken by the player
    shot_types = [1, 2, 3] if count_ft else [1, 2]  # 1 = made shot, 2 = missed shot, 3 = FT
    df["is_player_shot"] = (
        df["EVENTMSGTYPE"].isin(shot_types) & (df["PLAYER1_ID"] == person_id)
    )

    # Filter the DataFrame to calculate the running count of shots
    df = df.sort_values("EVENTNUM")
    df["player_shot_num"] = df.groupby("PLAYER1_ID")["is_player_shot"].cumsum()

    # Filter the DataFrame to show number of shots up to the action number
    try:
        return int(
            df.loc[df["EVENTNUM"] == action_number, "player_shot_num"].iloc[0]
        )
    except IndexError:
        raise ValueError(f"actionNumber {action_number} not found in game {game_id}")
