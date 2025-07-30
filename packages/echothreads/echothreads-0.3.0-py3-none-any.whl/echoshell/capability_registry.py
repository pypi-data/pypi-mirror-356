"""In-memory registry for universal capabilities."""

from typing import Dict, Any, List

class CapabilityRegistry:
    def __init__(self):
        self._caps: Dict[str, Dict[str, Any]] = {}

    def register(self, cap: Dict[str, Any]):
        cap_id = cap.get("id")
        if cap_id:
            self._caps[cap_id] = cap

    def list(self) -> List[Dict[str, Any]]:
        return list(self._caps.values())
