import tskit

from lineagekit.core.CoalescentTree import CoalescentTree

ts = tskit.load("D:/test_real_alignment/Alejandro_Andrii/andrii_CYP.trees")
tree1 = ts.at(57684316)

#x_limits = [70879427, 70879429]
node_style1 = ".n49383 .sym {fill: blue}"  # All symbols under node 13
node_style2 = ".n50 > .sym {fill: cyan}"  # Only symbols that are an immediate child of node 15
style3 = "#myUID .background * {fill: #00FF00}"
style4 = ".leaf > .lab {text-anchor: start; transform: rotate(90deg) translate(6px)}" + ".node > .sym {transform: scale(4); fill: yellow; stroke: black; stroke-width: 0.5px}" +  ".tree .node > .lab {transform: translate(0, 0); text-anchor: middle; font-size: 7pt}" + ".n0 .node {stroke: blue; stroke-width: 2px}"
style5 = ".n13 > .sym {fill: cyan}" + ".n29 > .sym {fill: cyan}" + ".n9 > .sym {fill: cyan}"
css_string = node_style1 + node_style2 + style3 + style4 + style5
#ts_small.first().draw_svg(style=css_string)
# Create evenly-spaced y tick positions to avoid overlap
y_tick_pos = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10,20,30,40,50,60,70,80,90,100, 1000, 2000]

tree1.draw_svg(y_axis=True, y_ticks=y_tick_pos, size=(970, 1000), root_svg_attributes={'id': "myUID"})
parsed_tree = CoalescentTree.get_coalescent_tree(tree1)
parsed_tree.save_to_file("parsed_tree")

