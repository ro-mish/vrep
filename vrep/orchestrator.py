#!/usr/bin/env python3
import os
import sys
import argparse
import webbrowser
import tempfile
import atexit
from pathlib import Path
from .interactive_graph import InteractiveRepoGraph
from .utils.gitignore_parser import GitignoreParser

class RepoVisualizer:
    def __init__(self):
        self.temp_file = None
        self.setup_temp_file()
        atexit.register(self.cleanup)

    def setup_temp_file(self):
        """Create a temporary file for the visualization"""
        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.html',
            prefix='repo_viz_',
            dir=tempfile.gettempdir()  # Explicitly use system temp directory
        )
        self.temp_file = temp.name
        temp.close()

    def cleanup(self):
        """Remove temporary files on exit"""
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
                print("\nVisualization file cleaned up successfully.")
            except Exception as e:
                print(f"\nError cleaning up visualization file: {e}")

    def visualize_repo(self, repo_path: str):
        """Generate and display the repository visualization"""
        try:
            # Convert relative path to absolute path
            repo_path = os.path.abspath(repo_path)
            
            # Validate repository path
            if not os.path.exists(repo_path):
                print(f"Error: Repository path does not exist: {repo_path}")
                return 1
            
            if not os.path.isdir(repo_path):
                print(f"Error: Path is not a directory: {repo_path}")
                return 1

            # Check for .gitignore
            gitignore_path = os.path.join(repo_path, '.gitignore')
            if os.path.exists(gitignore_path):
                print(f"Found .gitignore file at {gitignore_path}")
            else:
                print("No .gitignore file found, all files will be included")

            print(f"Analyzing repository: {repo_path}")
            
            # Generate visualization
            interactive_graph = InteractiveRepoGraph(repo_path)
            interactive_graph.build_interactive_graph()
            
            # Save to temporary file
            interactive_graph.save_graph(self.temp_file)
            
            # Open in browser
            print("\nOpening visualization in your default web browser...")
            webbrowser.open(f'file://{self.temp_file}')
            
            # Wait for user
            input("\nPress Enter to close the visualization and cleanup...")
            
            return 0

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return 1
        except Exception as e:
            print(f"\nError: {str(e)}")
            return 1

def parse_args():
    parser = argparse.ArgumentParser(
        description='Visualize Python repository dependencies interactively.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Path to the repository to analyze (defaults to current directory)'
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    visualizer = RepoVisualizer()
    return visualizer.visualize_repo(args.repo_path)

if __name__ == "__main__":
    sys.exit(main()) 