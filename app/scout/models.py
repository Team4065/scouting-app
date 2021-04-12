from dataclasses import dataclass, field
from typing import Tuple

@dataclass
class Match:
  match_number: int
  red_alliance: Tuple[int, int, int]
  blue_alliance: Tuple[int, int, int]
  
@dataclass
class AllianceContribution:
  match_number: int
  team_number: int
  teleop_points_scored: int
  auto_points_scored: int
  
@dataclass
class PitObservation:
  team_number: int
  has_autonomous: bool
  autonomous_details: str
  