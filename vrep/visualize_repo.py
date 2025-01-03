#!/usr/bin/env python3
import argparse
import os
from interactive_graph import InteractiveRepoGraph
from graph_builder import RepoGraphBuilder

def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate an interactive visualization of Python dependencies in a repository.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        'repo_path',
        help='Path to the repository to analyze'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='repo_visualization.html',
        help='Output path for the visualization HTML file'
    )
    
    parser.add_argument(
        '--static',
        action='store_true',
        help='Generate a static matplotlib visualization instead of interactive HTML'
    )
    
    parser.add_argument(
        '--no-external',
        action='store_true',
        help='Exclude external dependencies from the visualization'
    )
    
    return parser.parse_args()

def validate_paths(repo_path: str, output_path: str) -> tuple[str, str]:
    """Validate and normalize input/output paths"""
    # Validate repo path
    repo_path = os.path.abspath(repo_path)
    if not os.path.exists(repo_path):
        raise ValueError(f"Repository path does not exist: {repo_path}")
    
    # Validate output path
    output_dir = os.path.dirname(output_path) or '.'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    return repo_path, output_path

def main():
    args = parse_args()
    
    try:
        # Validate paths
        repo_path, output_path = validate_paths(args.repo_path, args.output)
        
        if args.static:
            # Generate static visualization
            print(f"Generating static visualization for {repo_path}")
            graph_builder = RepoGraphBuilder(repo_path)
            graph_builder.parse_repository()
            graph_builder.visualize_static_graph(output_path)
            print(f"Static visualization saved to {output_path}")
        else:
            # Generate interactive visualization
            print(f"Generating interactive visualization for {repo_path}")
            interactive_graph = InteractiveRepoGraph(repo_path)
            interactive_graph.build_interactive_graph()
            interactive_graph.save_graph(output_path)
            print(f"Interactive visualization saved to {output_path}")
            print("Open the HTML file in a web browser to view the visualization")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 