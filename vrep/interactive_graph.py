from pyvis.network import Network
import os
import json
import networkx as nx
from typing import Optional, Dict, Any, Tuple
from .graph_builder import RepoGraphBuilder
from .config.config_manager import ConfigManager

class InteractiveRepoGraph:
    def __init__(self, repo_path: str):
        self.repo_builder = RepoGraphBuilder(repo_path)
        self.config = ConfigManager()
        self.centrality_metrics = {}
        
        # Initialize network with larger dimensions
        self.net = Network(
            height="900px",
            width="100%",
            bgcolor="#ffffff",
            font_color="black",
            directed=True,
            notebook=False
        )
        
        # Configure network physics
        self.net.force_atlas_2based(
            gravity=-50,
            central_gravity=0.01,
            spring_length=100,
            spring_strength=0.08,
            damping=0.4,
            overlap=0.5
        )
        
        # Set other options
        self.net.set_options("""
        const options = {
            "nodes": {
                "shape": "dot",
                "scaling": {
                    "min": 10,
                    "max": 30
                },
                "font": {
                    "size": 12,
                    "face": "Tahoma"
                }
            },
            "edges": {
                "color": {"inherit": true},
                "smooth": {"type": "continuous"},
                "arrows": {"to": {"enabled": true, "scaleFactor": 0.5}}
            },
            "physics": {
                "enabled": true,
                "solver": "forceAtlas2Based",
                "forceAtlas2Based": {
                    "gravitationalConstant": -50,
                    "centralGravity": 0.01,
                    "springLength": 100,
                    "springConstant": 0.08,
                    "damping": 0.4,
                    "avoidOverlap": 0.5
                },
                "stabilization": {
                    "enabled": true,
                    "iterations": 1000,
                    "updateInterval": 25
                }
            },
            "interaction": {
                "hover": true,
                "navigationButtons": true,
                "keyboard": true,
                "dragNodes": true,
                "dragView": true,
                "zoomView": true
            }
        }
        """)

    def build_interactive_graph(self) -> None:
        """Build the graph data structure from repository"""
        self.repo_builder.parse_repository()
        self._calculate_centrality_metrics()
        
        # Print graph statistics and important nodes
        print(f"Found {len(self.repo_builder.graph.nodes())} nodes")
        print(f"Found {len(self.repo_builder.graph.edges())} edges")
        print("\nMost Important Dependencies:")
        self._print_important_nodes()
        
        # Process nodes
        for node, attr in self.repo_builder.graph.nodes(data=True):
            try:
                if attr.get('type') == 'file':
                    file_path = os.path.join(self.repo_builder.repo_path, node)
                    metrics = self._get_node_metrics(node, file_path)
                    color = "#97C2FC"  # Light blue for files
                else:
                    metrics = self._get_external_metrics(node)
                    color = "#FFA07A"  # Light salmon for external imports
                
                # Scale node size based on centrality
                size = 20 + (self.centrality_metrics['betweenness_norm'].get(node, 0) * 30)
                
                # Create tooltip with metrics
                tooltip = self._create_tooltip(metrics)
                
                self.net.add_node(
                    node,
                    label=os.path.basename(node) if os.path.basename(node) else node,
                    title=tooltip,
                    color=color,
                    size=size
                )
            except Exception as e:
                print(f"Error processing node {node}: {str(e)}")
        
        # Add edges
        for source, target in self.repo_builder.graph.edges():
            try:
                self.net.add_edge(source, target)
            except Exception as e:
                print(f"Error adding edge {source}->{target}: {str(e)}")

    def _print_important_nodes(self, top_n: int = 5):
        """Print the most important nodes based on different metrics"""
        metrics = {
            'Most Central (Betweenness)': 'betweenness',
            'Most Influential (Eigenvector)': 'eigenvector',
            'Most Connected (PageRank)': 'pagerank',
            'Most Used (In-Degree)': 'in_degree',
            'Most Dependencies (Out-Degree)': 'out_degree'
        }
        
        for title, metric in metrics.items():
            # Sort nodes by metric value
            sorted_nodes = sorted(
                self.centrality_metrics[metric].items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_n]
            
            # Print section
            print(f"\n{title}:")
            for node, value in sorted_nodes:
                # Get node type (file or external import)
                node_type = "External" if not os.path.exists(os.path.join(self.repo_builder.repo_path, node)) else "File"
                
                # Format value based on metric type
                if metric in ['in_degree', 'out_degree']:
                    formatted_value = f"{value} connections"
                else:
                    formatted_value = f"{value:.3f}"
                
                # Print node info
                print(f"  • {os.path.basename(node)} ({node_type}): {formatted_value}")

    def _create_tooltip(self, metrics: Dict) -> str:
        """Create simple tooltip for node"""
        # Get importance rankings
        rankings = self._get_node_rankings(metrics['name'])
        rankings_text = "\n".join(f"• {title}: #{rank}" for title, rank in rankings.items())
        
        return (
            f"{metrics['name']}\n"
            f"-------------------\n"
            f"Type: {metrics['type']}\n"
            f"Size: {metrics['size']}\n"
            f"Dependencies: {metrics['in_degree']} in, {metrics['out_degree']} out\n"
            f"-------------------\n"
            f"Centrality Metrics:\n"
            f"• Betweenness: {metrics['betweenness']}\n"
            f"• Eigenvector: {metrics['eigenvector']}\n"
            f"• PageRank: {metrics['pagerank']}\n"
            f"-------------------\n"
            f"Rankings:\n"
            f"{rankings_text}"
        )

    def _get_node_rankings(self, node: str) -> Dict[str, int]:
        """Get rankings for a node across different metrics"""
        rankings = {}
        metrics = {
            'Centrality': 'betweenness',
            'Influence': 'eigenvector',
            'Connectivity': 'pagerank',
            'Usage': 'in_degree',
            'Dependencies': 'out_degree'
        }
        
        for title, metric in metrics.items():
            # Sort all nodes by this metric
            sorted_nodes = sorted(
                self.centrality_metrics[metric].items(),
                key=lambda x: x[1],
                reverse=True
            )
            # Find position of current node
            for i, (n, _) in enumerate(sorted_nodes, 1):
                if n == node:
                    rankings[title] = i
                    break
        
        return rankings

    def _calculate_centrality_metrics(self):
        """Calculate various centrality metrics for the graph"""
        G = self.repo_builder.graph
        try:
            self.centrality_metrics['betweenness'] = nx.betweenness_centrality(G)
            self.centrality_metrics['eigenvector'] = nx.eigenvector_centrality(G, max_iter=1000)
            self.centrality_metrics['pagerank'] = nx.pagerank(G)
            self.centrality_metrics['in_degree'] = dict(G.in_degree())
            self.centrality_metrics['out_degree'] = dict(G.out_degree())
            
            # Normalize metrics
            for metric in ['betweenness', 'eigenvector', 'pagerank']:
                max_val = max(self.centrality_metrics[metric].values()) or 1
                self.centrality_metrics[f'{metric}_norm'] = {
                    k: v/max_val for k, v in self.centrality_metrics[metric].items()
                }
        except Exception as e:
            print(f"Warning: Error calculating metrics: {e}")
            for metric in ['betweenness', 'eigenvector', 'pagerank', 'in_degree', 'out_degree']:
                self.centrality_metrics[metric] = {node: 0 for node in G.nodes()}
                self.centrality_metrics[f'{metric}_norm'] = {node: 0 for node in G.nodes()}

    def _get_node_metrics(self, node: str, file_path: str) -> Dict:
        """Get all metrics for a node"""
        stats = os.stat(file_path) if os.path.exists(file_path) else None
        return {
            'name': node,
            'type': 'File',
            'size': f"{stats.st_size/1024:.2f} KB" if stats else "N/A",
            'in_degree': self.centrality_metrics['in_degree'].get(node, 0),
            'out_degree': self.centrality_metrics['out_degree'].get(node, 0),
            'betweenness': f"{self.centrality_metrics['betweenness_norm'].get(node, 0):.3f}",
            'eigenvector': f"{self.centrality_metrics['eigenvector_norm'].get(node, 0):.3f}",
            'pagerank': f"{self.centrality_metrics['pagerank_norm'].get(node, 0):.3f}"
        }

    def _get_external_metrics(self, node: str) -> Dict:
        """Get metrics for external dependencies"""
        return {
            'name': node,
            'type': 'External Import',
            'size': "N/A",
            'in_degree': self.centrality_metrics['in_degree'].get(node, 0),
            'out_degree': self.centrality_metrics['out_degree'].get(node, 0),
            'betweenness': f"{self.centrality_metrics['betweenness_norm'].get(node, 0):.3f}",
            'eigenvector': f"{self.centrality_metrics['eigenvector_norm'].get(node, 0):.3f}",
            'pagerank': f"{self.centrality_metrics['pagerank_norm'].get(node, 0):.3f}"
        }

    def save_graph(self, output_path: str = "repo_graph.html") -> None:
        """Save the interactive graph to an HTML file"""
        try:
            # Save with custom template
            self.net.save_graph(output_path)
            
            # Add custom CSS to the generated file
            with open(output_path, 'r') as f:
                content = f.read()
            
            # Add responsive CSS
            content = content.replace('</head>',
                '''
                <style>
                    html, body { height: 100%; margin: 0; padding: 0; }
                    #mynetwork { width: 100%; height: 100vh; }
                    .vis-network { outline: none; }
                </style>
                </head>
                ''')
            
            with open(output_path, 'w') as f:
                f.write(content)
                
        except Exception as e:
            print(f"Error saving graph: {str(e)}")
            raise e