import ray
from typing import Callable, List, Dict, Optional, Tuple, Any

from ..common.neighborhood import NeighborhoodGenerator
from ..common.solution import Solution
from ..sequential.tabu_search import TabuSearch

class ParallelTabuSearch:
    def __init__(
        self,
        initial_solutions: List[Solution],
        neighborhood_generator: NeighborhoodGenerator,  # Doit être une instance de NeighborhoodGenerator
        get_move_hash: Callable[[Solution], int],
        tabu_tenure: int = 10,
        aspiration_criteria: Optional[List[Callable[[Solution], bool]]] = None,
        update_history: Optional[Callable[[Solution, Dict], Dict]] = None,
        apply_intensification: Optional[Callable[[Solution, List], Solution]] = None,
        update_intensification_memory: Optional[Callable[[Solution, List], List]] = None,
        apply_diversification: Optional[Callable[[Solution, List], Solution]] = None,
        update_diversification_memory: Optional[Callable[[Solution, List], List]] = None,
        max_iterations: int = 100,
        diversification_necessity: int = 5,
        diversification_frequency: int = 20,
        intensification_threshold: int = 20,
        patience: int = 15,
        control_cardinality: str = "p-control",
        communication_type: str = "collegial",
        search_strategy: str = "MPDS",
        platform_config: Optional[Dict[str, Any]] = None
    ):
        # Vérification du type de neighborhood_generator
        if not isinstance(neighborhood_generator, NeighborhoodGenerator):
            raise TypeError("neighborhood_generator doit être une instance de NeighborhoodGenerator")
            
        self.initial_solutions = initial_solutions
        self.neighborhood = neighborhood_generator
        self.get_move_hash = get_move_hash
        self.tabu_tenure = tabu_tenure
        self.aspiration_criteria = aspiration_criteria or []
        self.update_history = update_history
        self.apply_intensification = apply_intensification
        self.update_intensification_memory = update_intensification_memory
        self.apply_diversification = apply_diversification
        self.update_diversification_memory = update_diversification_memory
        self.max_iterations = max_iterations
        self.diversification_necessity = diversification_necessity
        self.diversification_frequency = diversification_frequency
        self.intensification_threshold = intensification_threshold
        self.patience = patience
        self.control_cardinality = control_cardinality
        self.communication_type = communication_type
        self.search_strategy = search_strategy
        self.platform_config = platform_config or {}

        self.worker_configs = self._configure_workers()

    def _configure_workers(self) -> List[Dict[str, Any]]:
        """Configure les paramètres de chaque worker."""
        base_config = {
            "neighborhood_generator": self.neighborhood,  # Passe directement l'objet NeighborhoodGenerator
            "get_move_hash": self.get_move_hash,
            "tabu_tenure": self.tabu_tenure,
            "aspiration_criteria": self.aspiration_criteria,
            "update_history": self.update_history,
            "apply_intensification": self.apply_intensification,
            "update_intensification_memory": self.update_intensification_memory,
            "apply_diversification": self.apply_diversification,
            "update_diversification_memory": self.update_diversification_memory,
            "max_iterations": self.max_iterations,
            "diversification_necessity": self.diversification_necessity,
            "diversification_frequency": self.diversification_frequency,
            "intensification_threshold": self.intensification_threshold,
            "patience": self.patience
        }

        if self.search_strategy == "SPSS":
            return [base_config.copy() for _ in self.initial_solutions]
        elif self.search_strategy == "SPDS":
            return [
                {**base_config, "tabu_tenure": self.tabu_tenure + i}
                for i in range(len(self.initial_solutions))
            ]
        elif self.search_strategy == "MPSS":
            return [base_config.copy() for _ in self.initial_solutions]
        elif self.search_strategy == "MPDS":
            return [
                {
                    **base_config,
                    "tabu_tenure": self.tabu_tenure + i,
                    "max_iterations": self.max_iterations + i * 10,
                    "diversification_frequency": self.diversification_frequency + i * 2
                }
                for i in range(len(self.initial_solutions))
            ]
        else:
            raise ValueError(f"Stratégie de recherche inconnue : {self.search_strategy}")

    @ray.remote
    class TabuSearchWorker:
        """Worker Ray pour exécuter une instance de TabuSearch."""
        def __init__(self, initial_solution: Solution, config: Dict[str, Any]):
            # Vérification que neighborhood_generator est bien un NeighborhoodGenerator
            if not isinstance(config["neighborhood_generator"], NeighborhoodGenerator):
                raise TypeError("neighborhood_generator doit être une instance de NeighborhoodGenerator")
                
            self.ts = TabuSearch(
                initial_solution=initial_solution,
                neighborhood_generator=config["neighborhood_generator"],
                get_move_hash=config["get_move_hash"],
                tabu_tenure=config["tabu_tenure"],
                aspiration_criteria=config["aspiration_criteria"],
                update_history=config["update_history"],
                apply_intensification=config["apply_intensification"],
                update_intensification_memory=config["update_intensification_memory"],
                apply_diversification=config["apply_diversification"],
                update_diversification_memory=config["update_diversification_memory"],
                max_iterations=config["max_iterations"],
                diversification_necessity=config["diversification_necessity"],
                diversification_frequency=config["diversification_frequency"],
                intensification_threshold=config["intensification_threshold"],
                patience=config["patience"]
            )

        def run(self) -> Solution:
            return self.ts.run()

        def get_current_state(self) -> Dict[str, Any]:
            """Retourne l'état actuel pour les communications."""
            return {
                "best_solution": self.ts.best_solution,
                "diversification_memory": self.ts.diversification_memory,
                "intensification_memory": self.ts.intensification_memory,
                "history": self.ts.history
            }

        def update_state(self, new_state: Dict[str, Any]):
            """Met à jour l'état du worker."""
            if new_state["best_solution"].evaluate() > self.ts.best_solution.evaluate():
                self.ts.best_solution = new_state["best_solution"].copy()
            self.ts.diversification_memory = new_state["diversification_memory"]
            self.ts.intensification_memory = new_state["intensification_memory"]
            self.ts.history = new_state["history"]

    def run(self) -> Solution:
        """Exécute la recherche Tabu parallèle selon la taxonomie définie."""
        workers = [
            self.TabuSearchWorker.remote(sol, config)
            for sol, config in zip(self.initial_solutions, self.worker_configs)
        ]

        if self.control_cardinality == "1-control":
            return self._run_1_control(workers)
        else:
            return self._run_p_control(workers)

    def _run_1_control(self, workers: List[Any]) -> Solution:
        """Implémentation 1-control (master-slave)."""
        results = ray.get([worker.run.remote() for worker in workers])
        return max(results, key=lambda x: x.evaluate())

    def _run_p_control(self, workers: List[Any]) -> Solution:
        """Implémentation p-control avec différents types de communication."""
        if self.communication_type == "rigid":
            results = ray.get([worker.run.remote() for worker in workers])
            return max(results, key=lambda x: x.evaluate())

        elif self.communication_type == "knowledge_sync":
            for _ in range(self.max_iterations // 10):
                ray.get([worker.run.remote() for worker in workers])
                states = ray.get([worker.get_current_state.remote() for worker in workers])
                best_state = max(states, key=lambda x: x["best_solution"].evaluate())
                ray.get([worker.update_state.remote(best_state) for worker in workers])
            results = ray.get([worker.run.remote() for worker in workers])
            return max(results, key=lambda x: x.evaluate())

        elif self.communication_type in ["collegial", "knowledge_collegial"]:
            for worker in workers:
                worker.run.remote()

            while True:
                states = ray.get([worker.get_current_state.remote() for worker in workers])
                best_state = max(states, key=lambda x: x["best_solution"].evaluate())

                if self.communication_type == "knowledge_collegial":
                    best_state["diversification_memory"] = self._combine_memories(
                        [s["diversification_memory"] for s in states]
                    )

                ray.get([worker.update_state.remote(best_state) for worker in workers])

                if all(s["best_solution"].evaluate() == best_state["best_solution"].evaluate() for s in states):
                    break

            return best_state["best_solution"]

    def _combine_memories(self, memories: List[List]) -> List:
        """Combine les mémoires pour la communication knowledge_collegial."""
        combined = []
        for mem in memories:
            combined.extend(mem)
        return list(set(combined))  # Élimine les doublons

    def shutdown(self):
        """Arrête proprement Ray."""
        ray.shutdown()
