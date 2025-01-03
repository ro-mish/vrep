# vrep

<img width="1318" alt="Screenshot 2025-01-03 at 5 36 54 PM" src="https://github.com/user-attachments/assets/b85443ec-aee4-45a5-abd6-55d67c6afd6a" />

vrep is a tool for visualizing codebase repositories. It provides a graphical representation of the repository's structure, making it easier to understand the relationships between different project parts.

## Getting started
First clone the repo.

```
git clone https://github.com/ro-mish/vrep.git
```

Next, change into the vrep repo.
```
cd vrep
```

To install vrep, you can use make install:
```
make install
```
This will install vrep and its dependencies.

## Usage

To use vrep, navigate to the root directory of the Git repository you want to visualize and run the following command:
```
vrep .
```
This will launch a web browser with an interactive visualization of the repository's commit history.

### Customizing the Visualization

You can customize the visualization by creating a configuration file. The configuration file should be in YAML format and can be placed anywhere in the repository. To use a custom configuration file, specify its path when running vrep:
```
vrep --config path/to/config.yaml
```
