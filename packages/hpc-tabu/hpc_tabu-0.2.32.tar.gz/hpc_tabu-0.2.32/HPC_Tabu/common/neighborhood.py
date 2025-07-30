from abc import ABC, abstractmethod
from typing import List, Optional
from .solution import Solution

class NeighborhoodGenerator(ABC):
    @abstractmethod
    def generate(self, solution: Solution) -> List[Solution]:
        pass

    

class CompositeNeighborhood(NeighborhoodGenerator):
    """Combine plusieurs générateurs de voisinage."""
    def __init__(self, neighborhoods: List[NeighborhoodGenerator]):
        self._neighborhoods = neighborhoods

    def generate(self, solution: Solution) -> List[Solution]:
        neighbors = []
        for neighborhood in self._neighborhoods:
            neighbors.extend(neighborhood.generate(solution))
        return neighbors

    