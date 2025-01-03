import os
import networkx as nx
import ast
from typing import Dict, Set, List
import matplotlib.pyplot as plt
from .utils.gitignore_parser import GitignoreParser

class RepoGraphBuilder:
    def __init__(self, repo_path: str):
        self.repo_path = os.path.abspath(repo_path)
        self.graph = nx.DiGraph()
        self.dependencies: Dict[str, Set[str]] = {}
        self.gitignore = GitignoreParser(self.repo_path)
        
    def parse_repository(self) -> None:
        """Walks through the repository and analyzes Python files for dependencies"""
        for root, dirs, files in os.walk(self.repo_path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if not self.gitignore.should_ignore(os.path.join(root, d))]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    # Skip ignored files
                    if self.gitignore.should_ignore(file_path):
                        continue
                    
                    relative_path = os.path.relpath(file_path, self.repo_path)
                    self.analyze_file(file_path, relative_path)

    def analyze_file(self, file_path: str, relative_path: str) -> None:
        """Analyzes a single Python file for imports and dependencies"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            imports = self._extract_imports(tree)
            
            # Add node for current file
            self.graph.add_node(relative_path, type='file')
            
            # Add dependencies to graph
            for import_path in imports:
                # Skip ignored imports
                import_file = f"{import_path.replace('.', '/')}.py"
                if self.gitignore.should_ignore(import_file):
                    continue
                
                # Add the import as a node if it doesn't exist
                if import_path not in self.graph:
                    self.graph.add_node(import_path, type='import')
                self.graph.add_edge(relative_path, import_path)
                
        except Exception as e:
            print(f"Error analyzing {file_path}: {str(e)}")

    def _extract_imports(self, tree: ast.AST) -> Set[str]:
        """Extracts import statements from AST"""
        imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name.split('.')[0])  # Get base module name
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])  # Get base module name
                
        return imports

    def visualize_static_graph(self, output_path: str = None) -> None:
        """Creates a static visualization of the dependency graph"""
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph, k=1, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph,
            pos,
            node_color='lightblue',
            node_size=2000,
        )
        
        # Draw edges
        nx.draw_networkx_edges(
            self.graph,
            pos,
            edge_color='gray',
            arrows=True,
            arrowsize=20
        )
        
        # Draw labels
        nx.draw_networkx_labels(
            self.graph,
            pos,
            font_size=8,
            font_weight='bold'
        )
        
        plt.title("Repository Dependencies")
        if output_path:
            plt.savefig(output_path, bbox_inches='tight')
        plt.close()
