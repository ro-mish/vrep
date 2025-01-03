#!/usr/bin/env python3
import argparse
import os
import networkx as nx
from pathlib import Path
from .interactive_graph import InteractiveRepoGraph
from .graph_builder import RepoGraphBuilder

def main():
    """Legacy entry point - redirects to orchestrator"""
    from .orchestrator import main as orchestrator_main
    return orchestrator_main()

if __name__ == "__main__":
    exit(main()) 