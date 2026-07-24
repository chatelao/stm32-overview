from typing import Dict, List, Any
from src.core.repository import DataRepository

class RegistryEngine:
    def __init__(self, repository: DataRepository):
        self.repository = repository

    def list_boards(self) -> List[str]:
        """Returns a sorted list of all available board names."""
        specs = self.repository.load_all_specs()
        boards = [spec["board"] for spec in specs]
        return sorted(boards)

    def get_board_details(self, board_name: str) -> Dict[str, Any]:
        """Returns detailed specifications for the specified board name."""
        return self.repository.get_spec(board_name)
