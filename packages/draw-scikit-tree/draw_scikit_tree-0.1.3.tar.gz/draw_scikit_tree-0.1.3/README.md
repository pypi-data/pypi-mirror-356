<h1>
  <picture>
    <img alt="DrawScikitTreeLogo" src="icons/Logo.png" width="750px">
  </picture>
</h1>

# DrawScikitTree
A simple interface to modify scikit-learn's generated DOT string representation of a trained decision tree. Some basic function include changing the shape and color of each node, and tracing the decision paths taken for a test sample.

## Installation
```
pip install draw-scikit-tree
```

## Basic usage
Using the iris dataset as the classical example.
```python
from sklearn.datasets import load_iris
from sklearn import tree
iris = load_iris()
X, y = iris.data, iris.target
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)
```

Next, use the trained classifier to initialize the `TreeGraph` object.
```python
from DrawScikitTree import TreeGraph
treeGraph = TreeGraph(clf, impurity=False, label="none", fontname="Arial")
```

To trace the decisions paths taken for some test samples, use the `.trace_paths(X_sample)` function.
```python
import numpy as np
import graphviz

# Get some random samples
random_indices = np.random.randint(X.shape[0], size=5)
X_sample = X[random_indices, :]

# Setting verbose=True will print out the decision paths for each sample
treeGraph.trace_paths(X_sample, color="red", verbose=True)

# Displaying the newly modified tree
new_dot_data = treeGraph.export()
graph = graphviz.Source(new_dot_data)
display(graph)
```
<picture>
  <img alt="ExampleTree" src="icons/example_tree.png" width="550px">
</picture>

For more examples check out the [examples](https://github.com/RenZhen95/draw-scikit-tree/tree/master/examples).
