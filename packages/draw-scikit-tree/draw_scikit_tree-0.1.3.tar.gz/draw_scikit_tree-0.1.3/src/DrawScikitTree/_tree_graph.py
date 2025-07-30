import graphviz
import numpy as np
import pandas as pd
from ._node import Node
from ._edge import Edge
from ._leaf import Leaf
from sklearn import tree
from collections import defaultdict

class TreeGraph:
    '''
    Interface to allow for more user-friendly DOT script modifications.

    Parameters
    ----------
    tree_model : sklearn.tree.BaseDecisionTree
     - Trained tree model.

    **kwargs : `sklearn.tree.export_graphivz` properties

    Attributes
    ----------
    tree_model : sklearn.tree.BaseDecisionTree
     - Trained tree model used to initialize this object.

    Nodes : list
     - List of Node objects.

    Edges : list
     - List of Edge objects.

    Leaves : list
     - List of Leaf objects.
    '''
    def __init__(self, tree_model, **kwargs):
        self.tree_model = tree_model
        
        dot_data = tree.export_graphviz(
            self.tree_model, **kwargs
        ).splitlines()

        self.line_dict = defaultdict(str)

        # Indicator of a node
        isNode = lambda x: True if " <= " in x else False
        self.Nodes = []

        # Indicator of an edge
        isEdge = lambda x: True if " -> " in x else False
        self.Edges = []

        # Indicator of a leaf
        isLeaf = lambda x: True if " [label=" in x else False
        self.Leaves = []

        for i, line in enumerate(dot_data):
            # Check if line is a node
            if isNode(line):
                self.Nodes.append(Node(line, self.default_node_shape))
                self.line_dict[i] = self.Nodes[-1]
                continue

            else:
                # Check if line is an edge
                if isEdge(line):
                    self.Edges.append(Edge(line))
                    self.line_dict[i] = self.Edges[-1]
                    continue

                # Check if line is a leaf
                elif isLeaf(line):
                    self.Leaves.append(Leaf(line, self.default_node_shape))
                    self.line_dict[i] = self.Leaves[-1]
                    continue

                # Neither Node, Edge or Leaf
                else:
                    # Get default shape of Nodes and Edges
                    if "node [" in line:
                        self.default_node_shape = line.split(
                            "shape="
                        )[1].split(",")[0]
                        self.line_dict[i] = line
                        continue

                    else:
                        self.line_dict[i] = line
                        continue

    def trace_paths(
            self, X_test, color="red", mark_leaf_count=True, verbose=False
    ):
        '''
        Trace decision paths given test samples.

        Parameters
        ----------
        X_test : pd.Series or pd.DataFrame
         - Test sample(s) to investigate.

        color : str
         - Color to trace decision paths.

        mark_leaf_count : bool, default=True
         - Mark number of samples that reach each leaf.

        verbose : bool, default=False
         - Prints decision paths traversed.
        '''
        # For Numpy matrices
        if isinstance(X_test, np.ndarray):
            X_test = pd.DataFrame(X_test)

        # Map non-integer IDs and features to integers for Pandas DataFrame
        int_sampleID_map = defaultdict()
        for idx, gc in enumerate(X_test.index):
            int_sampleID_map[gc] = idx
        
        int_feature_map = defaultdict()
        for idx, col in enumerate(X_test.columns):
            int_feature_map[idx] = col

        # Get tree features that were traversed (used as splitting criterion)
        tree_features = self.tree_model.tree_.feature
            
        # Conversing the tree for the given samples
        node_indicator = self.tree_model.decision_path(X_test)
        # Matrix [#sp, #tree-nodes] where 1 indicates traversed path
        
        leaf_id = self.tree_model.apply(X_test)
        # leaf_ids for each stride pair
        
        threshold = self.tree_model.tree_.threshold
        # thresholds at each tree node, but if leaf, simply -2
        
        for sample in X_test.index:
            sample_id = int_sampleID_map[sample]

            node_index = node_indicator.indices[
                node_indicator.indptr[sample_id] : node_indicator.indptr[sample_id + 1]
            ]
            self.mark_paths_wColor(node_index, color)

            if mark_leaf_count:
                self.mark_leaf_count(leaf_id[sample_id], color)
        
            if verbose:
                print(f"node_index for {sample_id}: {node_index}")
                print(f"Rules used to predict Sample {sample} ({sample_id}):")
        
                for node_id in node_index:
                    # Continue to the next node if it is a leaf node
                    if leaf_id[sample_id] == node_id:
                        continue
                
                    # Check if value of the split feature for sample is below threshold
                    if X_test.at[sample, int_feature_map[tree_features[node_id]]] <= threshold[node_id]:
                        threshold_sign = "<="
                    else:
                        threshold_sign = ">"
                
                    _value = X_test.at[sample, int_feature_map[tree_features[node_id]]]
                    print(
                        f" - Decision node {node_id} : (X_test[{sample_id}, {tree_features[node_id]}] = {_value}) "
                        f"{threshold_sign} {threshold[node_id]})"
                    )

    def mark_paths_wColor(self, node_indices, color):
        '''
        Sub-routine for `self.trace_paths()`.

        Color arrows to trace path through decision tree.
        '''
        arrows_to_mark = [
            f"{node_indices[i]} -> {node_indices[i+1]}" for i in range(len(node_indices)-1)
        ]
        for arrow in arrows_to_mark:
            for edge in self.Edges:
                if arrow in edge.line:
                    if not f"color=\"{color}\"" in edge.line:
                        if ']' in edge.line:
                            edge.line = edge.line.replace(']', f', color="{color}"]')
                        else:
                            edge.line = edge.line.replace(';', f'[color="{color}"];')
                        break

    def mark_leaf_count(self, leaf_id, color):
        '''
        Sub-routine for `self.trace_paths()`.

        Mark number of times a leaf was reached.
        '''
        get_leaf_count = lambda x: int(
            (x.split('xlabel=')[1]).split('"')[1].replace('#','')
        )
        for leaf in self.Leaves:
            if leaf.ID == str(leaf_id):
                
                # Add count to xlabel
                if 'xlabel' in leaf.line:
                    leafcount = get_leaf_count(leaf.line)
                    leaf.line = leaf.line.replace(
                        f'#{leafcount}', f'#{leafcount + 1}'
                    )
    
                # Initialize xlabel
                else:
                    leaf.line = leaf.line.replace(
                        '] ;', f', xlabel="#1" fontcolor="{color}"] ;'
                    )
                break

    def export(self):
        '''
        Exports DOT script, including changes made by user to every
        Node, Edge, and Leaf object.
        '''
        new_dot_data = ""
        for k in self.line_dict.keys():
            if isinstance(self.line_dict[k], Node):
                new_dot_data += f"{self.line_dict[k].line}\n"
            elif isinstance(self.line_dict[k], Edge):
                new_dot_data += f"{self.line_dict[k].line}\n"
            elif isinstance(self.line_dict[k], Leaf):
                new_dot_data += f"{self.line_dict[k].line}\n"
            else:
                new_dot_data += f"{self.line_dict[k]}\n"

        return new_dot_data

    def render(self, file_name, format="pdf"):
        '''
        Render the DOT script.

        Parameters
        ----------
        file_name : str
         - Desired file name to save tree as.

        format : str, default="pdf"
         - Format of file to save tree as.
        '''
        graphviz.Source(self.export()).render(
            file_name, format=format
        )
