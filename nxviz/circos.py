from .base import BasePlot
from .geometry import node_theta, get_cartesian
import matplotlib.patches as patches

from matplotlib.path import Path


class CircosPlot(BasePlot):
    """docstring for CircosPlot"""
    def __init__(self, nodes, edges, radius,
                 nodecolor=None, edgecolor=None,
                 nodeprops=None, edgeprops=None,
                 figsize=None):
        BasePlot.__init__()
        self.radius = radius

    def draw_nodes(self):
        """
        Renders nodes to the figure.
        """
        r = self.radius
        node_r = self.node_radius
        # if 'color' in self.nodeprops:
        #    self.nodeprops.pop('color')
        if 'facecolor' in self.nodeprops:
            self.nodeprops.pop('facecolor')
        # Check if self.nodecolor is a string. If so, this color gets applied
        # to all nodes.
        if isinstance(self.nodecolor, str):
            nodes_and_colors = zip(self.nodes,
                                   [self.nodecolor] * len(self.nodes))
        # Check if nodecolor is an iterable. If so and same length as nodes.
        # This applies each matched color to that node.
        elif hasattr(self.nodecolor, '__iter__') and \
                (len(self.nodes) == len(self.nodecolor)):
            nodes_and_colors = zip(self.nodes, self.nodecolor)
        # Throw error if above two conditions are not met.
        else:
            raise TypeError("""nodecolor must be a string or iterable of the
                same length as nodes.""")
        # Draw the nodes to screen.
        for node, color in nodes_and_colors:
            theta = node_theta(self.nodelist, node)
            x, y = get_cartesian(r, theta)
            self.nodeprops['facecolor'] = color
            node_patch = patches.Ellipse((x, y), node_r, node_r,
                                         lw=0, **self.nodeprops)
            self.ax.add_patch(node_patch)

    def draw_edges(self):
        """
        Draws edges to screen.
        """
        for start, end in self.edges:
            start_theta = node_theta(self.nodelist, start)
            end_theta = node_theta(self.nodelist, end)
            verts = [get_cartesian(self.radius, start_theta),
                     (0, 0),
                     get_cartesian(self.radius, end_theta)]
            codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]

            path = Path(verts, codes)
            self.edgeprops['facecolor'] = 'none'
            self.edgeprops['edgecolor'] = self.edgecolor
            patch = patches.PathPatch(path, lw=1, **self.edgeprops)
            self.ax.add_patch(patch)
