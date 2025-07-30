
---

### 🔬 `hpc_ts/README.md`

```markdown
# hpc_ts

`hpc_ts` est un framework modulaire pour la conception et l’exécution de stratégies de recherche tabou (Tabu Search) en environnement parallèle. Construit en Python, il est conçu pour être générique et réutilisable dans des contextes de haute performance (HPC).

## ⚙️ Fonctionnalités principales

- Architecture orientée objet :
  - `TabuMemory` : gestion des mouvements tabous
  - `NeighborGenerator` : modules pour différents types de voisins
  - `TabuSearch` : cœur de l’algorithme
- Prise en charge de plusieurs stratégies de voisinage :
  - Suppression
  - Insertion
  - Remplacement
  - Injection de motifs denses
- Modèle de parallélisme flexible :
  - **1-contrôle rigide**
  - Génération parallèle des voisins par `ThreadPoolExecutor`
  - Calcul distribué des métriques via `Ray`
- Installation simple et utilisation portable

## 🛠️ Installation

```bash
pip install hpc_ts
```

## 🚀 Exemple d'utilisation
from hpc_ts.tabu_search import TabuSearch
from hpc_ts.neighbors import generate_neighbors

search = TabuSearch(...)
best_solution = search.optimize()

## 📁 Structure du projet
hpc_ts/
├── tabu_search/
├── tabu_memory/
├── neighbors/
├── diversification/
├── metrics/
└── parallel/


## 🔬 Applications

Optimisation combinatoire

Bioinformatique (clustering de réseaux PPI)

Planification, affectation, etc.

