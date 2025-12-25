from dataclasses import dataclass

@dataclass
class Show:
    title: str
    url: str
    img: str
    
    # stats fields
    score: float
    rank: int
    popularity: int
    watching: int
    completed: int
    on_hold: int
    dropped: int
    plan_to_watch: int
    members: int
    favorites: int
    
    # information fields
    type: str
    episodes: int
    status: str
    aired: str
    premiered: str
    broadcast: str
    producers: str
    licensors: str
    studios: str
    Source: str
    genres: str
    demographic: str
    duration: str
    rating: str
