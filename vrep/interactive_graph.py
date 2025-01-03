import networkx as nx
from pyvis.network import Network
import json

class InteractiveRepoGraph:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.net = Network(
            height="750px",
            width="100%",
            bgcolor="#ffffff",
            font_color="black"
        )
        self.net.toggle_physics(True)
        self._calculate_statistics()

    def _calculate_statistics(self):
        """Calculate repository statistics"""
        self.stats = {
            "Repository Statistics": {
                "Total Files": len(self.graph.nodes()),
                "Total Dependencies": len(self.graph.edges()),
                "Max Depth": self._calculate_max_depth()
            },
            "Most Central Files": self._get_most_central_files(),
            "Most Used Files": self._get_most_used_files(),
            "Most Dependencies": self._get_files_with_most_deps()
        }

    def _calculate_max_depth(self) -> int:
        """Calculate maximum dependency depth"""
        try:
            return nx.dag_longest_path_length(self.graph)
        except:
            return 0

    def _get_most_central_files(self, n=5):
        """Get files with highest centrality"""
        centrality = nx.degree_centrality(self.graph)
        return {k: f"{v:.3f}" for k, v in sorted(
            centrality.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n]}

    def _get_most_used_files(self, n=5):
        """Get most imported files"""
        return {node: f"{self.graph.in_degree(node):.3f}" for node in sorted(
            self.graph.nodes(), 
            key=lambda x: self.graph.in_degree(x),
            reverse=True
        )[:n]}

    def _get_files_with_most_deps(self, n=5):
        """Get files with most dependencies"""
        return {node: f"{self.graph.out_degree(node):.3f}" for node in sorted(
            self.graph.nodes(), 
            key=lambda x: self.graph.out_degree(x),
            reverse=True
        )[:n]}

    def build_interactive_graph(self):
        """Build the interactive visualization"""
        # Add nodes with their attributes
        for node in self.graph.nodes(data=True):
            self.net.add_node(
                node[0],
                label=node[0],
                title=self._build_node_tooltip(node[0]),
                color=node[1].get('color', '#97c2fc')
            )

        # Add edges
        for edge in self.graph.edges():
            self.net.add_edge(edge[0], edge[1])

    def _build_node_tooltip(self, node: str) -> str:
        """Build HTML tooltip for node"""
        metrics = {
            'Centrality': f"{self.graph.nodes[node].get('degree_centrality', 0):.3f}",
            'Dependencies': self.graph.out_degree(node),
            'Used by': self.graph.in_degree(node)
        }
        return '<br>'.join(f'{k}: {v}' for k, v in metrics.items())

    def save_graph(self, output_path: str):
        """Save the visualization with statistics panel"""
        # Generate HTML for statistics panel
        stats_html = self._generate_stats_html()
        
        # Save graph with custom HTML
        self.net.save_graph(output_path)
        
        # Insert statistics panel into saved HTML
        with open(output_path, 'r') as f:
            html = f.read()
        
        html = html.replace('<body>', f'<body>{stats_html}')
        
        with open(output_path, 'w') as f:
            f.write(html)

    def _generate_stats_html(self) -> str:
        """Generate HTML for statistics panel"""
        html = '''
        <style>
            #stats-panel {
                position: fixed;
                left: 10px;
                top: 10px;
                background: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                max-width: 300px;
                z-index: 1000;
            }
            .stat-section {
                margin-bottom: 15px;
            }
            .stat-section h3 {
                margin: 5px 0;
                color: #333;
            }
            .stat-item {
                margin: 3px 0;
                color: #666;
            }
        </style>
        <div id="stats-panel">
        '''
        
        for section, items in self.stats.items():
            html += f'<div class="stat-section"><h3>{section}</h3>'
            for key, value in items.items():
                html += f'<div class="stat-item">• {key}: {value}</div>'
            html += '</div>'
        
        html += '</div>'
        return html