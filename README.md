# vrep

vrep is a tool for visualizing the commit history of a Git repository. It provides a graphical representation of the repository's structure, making it easier to understand the relationships between different parts of the project.

## Installation

To install vrep, you can use pip:
```
pip install vrep
```
This will install vrep and its dependencies.

## Usage

To use vrep, navigate to the root directory of the Git repository you want to visualize and run the following command:
```
vrep
```
This will launch a web browser with an interactive visualization of the repository's commit history. You can explore the graph by clicking on nodes and edges to see more information about each commit.

### Customizing the Visualization

You can customize the visualization by creating a configuration file. The configuration file should be in YAML format and can be placed anywhere in the repository. To use a custom configuration file, specify its path when running vrep:
```
vrep --config path/to/config.yaml
```
