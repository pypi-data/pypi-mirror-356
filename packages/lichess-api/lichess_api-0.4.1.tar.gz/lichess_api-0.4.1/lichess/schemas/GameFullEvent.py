from typing import Literal

from pydantic import BaseModel

from .Variant import Variant
from .Speed import Speed
from .GameEventPlayer import GameEventPlayer
from .GameStateEvent import GameStateEvent


class GameFullEvent(BaseModel):
    """
    GameFullEvent

    See https://github.com/lichess-org/api/blob/master/doc/specs/schemas/GameFullEvent.yaml
    """

    type: Literal["gameFull"]
    id: str
    variant: Variant
    clock: object
    speed: Speed
    perf: object
    rated: bool
    createdAt: int
    white: GameEventPlayer
    black: GameEventPlayer
    initialFen: str
    state: GameStateEvent
    tournamentId: str | None = None
