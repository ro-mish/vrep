import os
from pathlib import Path
import ast
import networkx as nx
from typing import Dict, Set, List

class RepoGraphBuilder:
    def __init__(self, repo_path: Path, config: dict):
        """Initialize with repository path and configuration"""
        self.repo_path = Path(repo_path)
        self.config = config
        self.graph = nx.DiGraph()
        self.import_cache: Dict[str, Set[str]] = {}

    def build_graph(self) -> nx.DiGraph:
        """Build dependency graph from Python files"""
        # Find all Python files
        python_files = self._find_python_files()
        
        # Create nodes for each file
        for file_path in python_files:
            relative_path = str(file_path.relative_to(self.repo_path))
            self.graph.add_node(
                relative_path,
                type='file',
                size=os.path.getsize(file_path),
                label=relative_path
            )
            
            # Parse imports
            imports = self._get_file_imports(file_path)
            for imported in imports:
                self.graph.add_edge(relative_path, imported)

        # Calculate metrics
        self._calculate_metrics()
        return self.graph

    def _find_python_files(self) -> List[Path]:
        """Find all Python files in repository"""
        python_files = []
        for root, _, files in os.walk(self.repo_path):
            if 'venv' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        return python_files

    def _get_file_imports(self, file_path: Path) -> Set[str]:
        """Extract imports from a Python file"""
        if file_path in self.import_cache:
            return self.import_cache[file_path]

        imports = set()
        try:
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.add(name.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

        self.import_cache[file_path] = imports
        return imports

    def _calculate_metrics(self):
        """Calculate centrality metrics for the graph"""
        # Calculate various centrality metrics
        degree_centrality = nx.degree_centrality(self.graph)
        betweenness_centrality = nx.betweenness_centrality(self.graph)
        
        # Add metrics to node attributes
        for node in self.graph.nodes():
            self.graph.nodes[node]['degree_centrality'] = degree_centrality[node]
            self.graph.nodes[node]['betweenness_centrality'] = betweenness_centrality[node]
            # Color nodes based on centrality
            self.graph.nodes[node]['color'] = self._get_color_for_centrality(degree_centrality[node])

    def _get_color_for_centrality(self, centrality: float) -> str:
        """Map centrality value to color"""
        # Use a simple blue gradient
        intensity = int(255 * centrality)
        return f'#{intensity:02x}{intensity:02x}ff'
