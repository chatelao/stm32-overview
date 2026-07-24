from typing import Dict, List, Any
from pydantic import BaseModel
from src.core.registry import RegistryEngine

class Constraints(BaseModel):
    min_flash_kb: int = 0
    min_sram_kb: int = 0
    min_freq_mhz: int = 0
    requires_fpu: bool = False
    peripherals: List[str] = []

class Recommendation(BaseModel):
    board_name: str
    match_score: float                  # Percentage / score of match
    matched_features: List[str]
    missing_features: List[str]

class RecommendationEngine:
    def __init__(self, registry: RegistryEngine):
        self.registry = registry

    def evaluate(self, constraints: Constraints) -> List[Recommendation]:
        """
        Matches constraints against all registered boards.
        Returns a sorted list of recommendations from best match to worst.
        """
        boards = self.registry.list_boards()
        recommendations = []

        for board_name in boards:
            board_details = self.registry.get_board_details(board_name)

            active_constraints = 0
            matched = []
            missing = []

            # 1. Flash memory constraint
            if constraints.min_flash_kb > 0:
                active_constraints += 1
                if board_details.get("memory", {}).get("flash_kb", 0) >= constraints.min_flash_kb:
                    matched.append("flash_kb")
                else:
                    missing.append("flash_kb")

            # 2. SRAM memory constraint
            if constraints.min_sram_kb > 0:
                active_constraints += 1
                if board_details.get("memory", {}).get("sram_kb", 0) >= constraints.min_sram_kb:
                    matched.append("sram_kb")
                else:
                    missing.append("sram_kb")

            # 3. Frequency constraint
            if constraints.min_freq_mhz > 0:
                active_constraints += 1
                if board_details.get("core", {}).get("frequency_mhz", 0) >= constraints.min_freq_mhz:
                    matched.append("frequency_mhz")
                else:
                    missing.append("frequency_mhz")

            # 4. FPU constraint
            if constraints.requires_fpu:
                active_constraints += 1
                if board_details.get("core", {}).get("fpu", False):
                    matched.append("fpu")
                else:
                    missing.append("fpu")

            # 5. Peripherals constraint
            for p in constraints.peripherals:
                active_constraints += 1
                if board_details.get("peripherals", {}).get(p, 0) > 0:
                    matched.append(p)
                else:
                    missing.append(p)

            # Calculate score
            if active_constraints == 0:
                match_score = 100.0
            else:
                match_score = (len(matched) / active_constraints) * 100.0

            recommendations.append(
                Recommendation(
                    board_name=board_name,
                    match_score=round(match_score, 2),
                    matched_features=matched,
                    missing_features=missing
                )
            )

        # Sort recommendations by match_score descending, and board_name alphabetically (ascending) for tie-breaker
        recommendations.sort(key=lambda r: (-r.match_score, r.board_name))
        return recommendations
