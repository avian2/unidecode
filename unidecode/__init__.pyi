from typing import Any, Dict, Optional, Sequence

Cache: Dict[int, Optional[Sequence[Optional[str]]]]

class UnidecodeError(ValueError):
    index: Optional[int] = ...
