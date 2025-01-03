#!/usr/bin/env python3
import os
import sys
import webbrowser
import tempfile
import atexit
from pathlib import Path

from .config.config_manager import ConfigManager
from .graph_builder import RepoGraphBuilder
from .interactive_graph import InteractiveRepoGraph

class Orchestrator:
    def __init__(self, repo_path: str = ".", config_path: str = None):
        """
        Initialize the visualization orchestrator.
        
        Args:
            repo_path (str): Path to the repository to analyze
            config_path (str, optional): Path to custom configuration file
        """
        self.repo_path = Path(repo_path)
        self.config_manager = ConfigManager(config_path)
        self.temp_file = None
        self.setup_temp_file()
        atexit.register(self.cleanup)

    def setup_temp_file(self):
        """Create a temporary file for the visualization"""
        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.html',
            prefix='repo_viz_',
            dir=tempfile.gettempdir()
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

    def run(self) -> int:
        """
        Execute the visualization process end-to-end.
        
        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        try:
            # Validate repository path
            if not self.repo_path.exists():
                print(f"Error: Repository path does not exist: {self.repo_path}")
                return 1
            
            if not self.repo_path.is_dir():
                print(f"Error: Path is not a directory: {self.repo_path}")
                return 1

            print(f"Analyzing repository: {self.repo_path}")
            
            # Load configuration
            config = self.config_manager.get_config()
            
            # Build dependency graph
            print("Building dependency graph...")
            graph_builder = RepoGraphBuilder(self.repo_path, config)
            graph = graph_builder.build_graph()
            
            # Generate visualization
            print("Generating visualization...")
            interactive_graph = InteractiveRepoGraph(graph)
            interactive_graph.build_interactive_graph()
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

def main():
    """Command-line entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Visualize Python repository dependencies interactively.'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Path to the repository to analyze (defaults to current directory)'
    )
    parser.add_argument(
        '--config',
        help='Path to custom configuration file'
    )
    
    args = parser.parse_args()
    orchestrator = Orchestrator(args.repo_path, args.config)
    return orchestrator.run()

if __name__ == "__main__":
    sys.exit(main()) 