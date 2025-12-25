from dataclasses import dataclass

@dataclass
class Ranking:
    rank: int
    title: str
    score: float
    url: str
    thumbnail: str
