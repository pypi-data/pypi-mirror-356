import pandas as pd
import numpy as np
import networkx as nx
import copy
from swmm_api.input_file import SwmmInput, section_labels as sections
import os
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

class graph_create_from_inp:
    def __init__(self, inp_file: str):
        self.inp_file = inp_file
        self.inp_to_graph()
    
    def hortons_hierarchy(self):
        """应对非完全树状图情况"""
        graph = self.G.copy()
        outlet_node = [node for node in graph.nodes() if graph.out_degree(node) == 0]
        nodes_hierarchy = {item: 1 for item in list(graph.nodes())}
        in_degree = graph.in_degree()
        # print(graph.number_of_nodes())
        delete_nodes = []
        while graph.number_of_nodes() > len(outlet_node):
            # print(graph.nodes())
            degree_0_nodes = [node for node, degree in in_degree if degree==0]
            confluence_nodes = [node for node, degree in in_degree if degree>0]

            for node in confluence_nodes:
                pre_nodes = list(graph.predecessors(node))
                if set(pre_nodes).issubset(set(degree_0_nodes)): # 邻接上游点是否均为源头点
                    pre_nodes_hierarchy = [nodes_hierarchy[node] for node in pre_nodes]
                    if len(pre_nodes_hierarchy) == 1:
                        nodes_hierarchy[node] = pre_nodes_hierarchy[0]
                        self.G.nodes[node]['weight'] = nodes_hierarchy[node]
                    else:
                        if len(set(pre_nodes_hierarchy)) == 1:
                            nodes_hierarchy[node] = pre_nodes_hierarchy[0] + 1
                            self.G.nodes[node]['weight'] = nodes_hierarchy[node]
                        else:
                            nodes_hierarchy[node] = max(pre_nodes_hierarchy)
                            self.G.nodes[node]['weight'] = nodes_hierarchy[node]
                    # print(node, nodes_hierarchy[node])
                    delete_nodes += pre_nodes
            
            graph.remove_nodes_from(delete_nodes)
            # print(graph.number_of_nodes())
            # print(graph.nodes.data())
            in_degree = graph.in_degree()

        # 更新排放口等级
        for index, node in enumerate(outlet_node):
            adj_nodes = list(self.G.reverse().successors(outlet_node[index]))
            nodes_hierarchy[node] = nodes_hierarchy[adj_nodes[0]]    
            self.G.nodes[node]['weight'] = nodes_hierarchy[node]
        # print(self.G.nodes.data())
        # print(nodes_hierarchy)
        return nodes_hierarchy

    def inp_to_graph(self):
        inp = SwmmInput.read_file(self.inp_file)
        # ------------------------ conduits ----------------------------
        conduits_df = inp[sections.CONDUITS].frame.reset_index()
        edges_df = conduits_df.drop_duplicates()
        # ------------------------- nodes --------------------------------
        nodes_df = inp[sections.COORDINATES].frame.reset_index()
        nodes_df = nodes_df.drop_duplicates()
        n_x_min = float(nodes_df['x'].min())
        n_y_min = float(nodes_df['y'].min())
        nodes_df['x_shift'] = nodes_df['x'].astype('float') - n_x_min
        nodes_df['y_shift'] = nodes_df['y'].astype('float') - n_y_min
        self.nodes_pos = dict(zip(nodes_df['node'], zip(nodes_df['x_shift'], nodes_df['y_shift'])))
        nodes_df = nodes_df.copy().set_index('node')
        # ---------------------- create digraph----------------------------
        # sewer_network = graph_tools.sewer_network_graph_toolkit(nodes_df, edges_df)
        self.G = nx.DiGraph()
        # set nodes attr (coords)
        nodes_coords = nodes_df.apply(lambda row: (row['x_shift'], row['y_shift']), axis=1).to_dict()
        # create nodes
        self.nodes_attr = [(key, {"pos": nodes_coords[key], 'weight': 1}) for key in nodes_coords]
        self.G.add_nodes_from(self.nodes_attr)
        # create edges
        edges_attr = edges_df.apply(lambda row: (row['from_node'], row['to_node'], {'label': row['name']}), axis=1)
        # create digraph
        self.G.add_edges_from(edges_attr)
        # -------------------- calculate edge length ------------------------
        adjacency_matrix = nx.to_pandas_adjacency(self.G).T
        length_matrix = adjacency_matrix.copy()
        nodes = adjacency_matrix.columns
        for i, node_i in enumerate(nodes): # source
            for j, node_j in enumerate(nodes): # target
                if adjacency_matrix[node_i][node_j] == 1:
                    length = round(np.sqrt((self.nodes_attr[i][1]['pos'][0] - self.nodes_attr[j][1]['pos'][0])**2 + (self.nodes_attr[i][1]['pos'][1] - self.nodes_attr[j][1]['pos'][1])**2), 3)
                    length_matrix[node_i][node_j] = length
                    self.G[node_i][node_j]['length'] = length
        # ---------------- cal horton hierachy ------------------------
        # print(self.G.nodes())
        self.hortons_hierarchy()
        # ------------------------- draw graph ----------------------------
        # nx.draw_networkx(graph, nodes_pos, with_labels=False, node_color='lightblue', node_size=50, font_size=13, arrowsize=20)
        # plt.show()

    def cal_tailored_betweenness_centrality(self, subgraph: nx.DiGraph):
        # calculate betweenness centrality and tailored betweenness centrality
        nodes = list(subgraph.nodes)
        betweenness_centrality = nx.betweenness_centrality(subgraph, weight='length')
        relevance_betweenness_centrality = {key: subgraph.nodes[key]['weight'] * betweenness_centrality[key] for key in nodes}
        # max_tailored_betweenness_node = max(relevance_betweenness_centrality, key=relevance_betweenness_centrality.get)
        # print(max_tailored_betweenness_node)
        return relevance_betweenness_centrality

    def add_nodes_elevation_attr(self, graph: nx.DiGraph):
        inp = SwmmInput.read_file(self.inp_file)
        inp_junctions = inp[sections.JUNCTIONS].frame.reset_index()
        inp_outfalls = inp[sections.OUTFALLS].frame.reset_index()
        inp_conduits = inp[sections.CONDUITS].frame.reset_index()
        inp_xsections = inp[sections.XSECTIONS].frame.reset_index()
        # ------------------------ 井底标高 ----------------------------
        print(inp_xsections.columns)
        # inp_junctions['bottom_elevation'] = np.round(inp_junctions['elevation'] - inp_junctions['depth_max'], 3) # elevation为管底标高
        inp_junctions['bottom_elevation'] = np.round(inp_junctions['elevation'], 3) # elevation为管底标高
        junctions_bottom_elevation = dict(zip(inp_junctions['name'], inp_junctions['bottom_elevation']))
        outfalls_bottom_elevation = dict(zip(inp_outfalls['name'], inp_outfalls['elevation']))
        nodes_bottom_elevation = {**junctions_bottom_elevation, **outfalls_bottom_elevation}
        print(len(junctions_bottom_elevation), len(outfalls_bottom_elevation), len(nodes_bottom_elevation))
        # print(nodes_bottom_elevation)
        # # ------------------------ 节点上游管段末端管底标高 ----------------------------
        # nodes_h_in = dict(zip(inp_conduits['to_node'], inp_conduits['offset_downstream']))
        # # ------------------------ 节点下游管段始端管底标高 ----------------------------
        # nodes_h_out = dict(zip(inp_conduits['from_node'], inp_conduits['offset_upstream']))
        # # ------------------------ 节点上下游管段管径 -----------------------------------
        # # print(len(inp_conduits), len(inp_xsections))
        # inp_conduits_xsections = pd.merge(inp_conduits, inp_xsections, how='left', left_on='name', right_on='link')
        # nodes_d_in = dict(zip(inp_conduits_xsections['to_node'], inp_conduits_xsections['height']))
        # nodes_d_out = dict(zip(inp_conduits_xsections['from_node'], inp_conduits_xsections['height']))
        # ------------------------ 更新节点属性 ----------------------------
        attrs = {}
        # for node in nodes_bottom_elevation.keys():
        #     if node in nodes_h_in.keys():
        #         if node in nodes_h_out.keys():
        #             attrs[node] = {"h_bottom": nodes_bottom_elevation[node], "h_in": nodes_h_in[node], "h_out": nodes_h_out[node], 'd_in': nodes_d_in[node], 'd_out': nodes_d_out[node]}
        #         else:
        #             attrs[node] = {"h_bottom": nodes_bottom_elevation[node], "h_in": nodes_h_in[node], "h_out": np.nan, 'd_in': nodes_d_in[node], 'd_out': np.nan}
        #     else:
        #         if node in nodes_h_out.keys():
        #             attrs[node] = {"h_bottom": nodes_bottom_elevation[node], "h_in": np.nan, "h_out": nodes_h_out[node], 'd_in': np.nan, 'd_out': nodes_d_out[node]}
        #         else:
        #             attrs[node] = {"h_bottom": nodes_bottom_elevation[node], "h_in": np.nan, "h_out": nodes_h_out[node], 'd_in': np.nan, 'd_out': np.nan}
        for node in nodes_bottom_elevation.keys():
            attrs[node] = {"h_bottom": nodes_bottom_elevation[node]}
        nx.set_node_attributes(graph, attrs)
        # print(graph.nodes.data())
        return graph

    def add_edges_elevation_attr(self, graph: nx.DiGraph):
        inp = SwmmInput.read_file(self.inp_file)
        inp_conduits = inp[sections.CONDUITS].frame.reset_index()
        inp_xsections = inp[sections.XSECTIONS].frame.reset_index()
        offset_upstream = dict(zip(inp_conduits['name'], inp_conduits['offset_upstream']))
        offset_downstream = dict(zip(inp_conduits['name'], inp_conduits['offset_downstream']))
        edges_d = dict(zip(inp_xsections['link'], inp_xsections['height']))
        attrs = {}
        for edge, source_node, target_node in zip(inp_conduits['name'], inp_conduits['from_node'], inp_conduits['to_node']):
            attrs[(source_node, target_node)] = {"h_upstream": offset_upstream[edge], "h_downstream": offset_downstream[edge], 'd': edges_d[edge]}
        # print(attrs)
        nx.set_edge_attributes(graph, attrs)
        # print(graph.edges.data())
        return graph

    def reverse_slope_conduits_detection(self, graph: nx.DiGraph):
        reverse_slope_conduits = []
        for edge in graph.edges():
            if graph.edges[edge]['h_upstream'] < graph.edges[edge]['h_downstream']:
                reverse_slope_conduits.append(edge)
                graph.edges[edge]['h_downstream'] = graph.edges[edge]['h_upstream'] - 0.5
        print(f'开始时存在{len(reverse_slope_conduits)}段逆坡管段')
        # 检测是否还存在逆坡
        for edge in graph.edges():
            if graph.edges[edge]['h_upstream'] < graph.edges[edge]['h_downstream']:
                print('存在管段逆坡')
                break
        
        return graph
    
    def reverse_slope_nodes_detection(self, graph: nx.DiGraph):
        while True:
            # 1. 找出所有逆坡节点
            reverse_slope_nodes = []
            for node in graph.nodes():
                if graph.in_degree(node) != 0: # 非源节点
                    in_edges = list(graph.in_edges(node)) # target_node = node
                    out_edges = list(graph.out_edges(node)) # source_node = node
                    if graph.out_degree(node) != 0:
                        h_out = graph.edges[out_edges[0]]['h_upstream'] + graph.edges[out_edges[0]]['d'] # 节点下游管顶标高
                        h_in = min(graph.edges[edge]['h_downstream'] + graph.edges[edge]['d'] for edge in in_edges) # 节点上游最低的管顶标高
                        if h_in < h_out:
                            reverse_slope_nodes.append(node)
            print(f'存在{len(reverse_slope_nodes)}个逆坡节点,{reverse_slope_nodes}')
            if not reverse_slope_nodes:
                break
            # 2. 修正所有逆坡节点及其后代
            print('节点逆坡修正后')
            for node in reverse_slope_nodes:
                in_edges = list(graph.in_edges(node)) # target_node = node
                out_edges = list(graph.out_edges(node)) # source_node = node
                if graph.out_degree(node) != 0:
                    h_in = min(graph.edges[edge]['h_downstream'] + graph.edges[edge]['d'] for edge in in_edges) # 节点上游最低的管顶标高
                    h_out = graph.edges[out_edges[0]]['h_upstream'] + graph.edges[out_edges[0]]['d'] # 节点下游管顶标高
                    if h_in < h_out:
                        delta_h = h_out - h_in
                        graph.edges[out_edges[0]]['h_upstream'] -= delta_h
                        graph.edges[out_edges[0]]['h_downstream'] -= delta_h
                        # print()
        
        # 3. 最终检测
        for node in graph.nodes():
            if graph.in_degree(node) != 0: # 非源节点
                in_edges = list(graph.in_edges(node)) # target_node = node
                out_edges = list(graph.out_edges(node)) # source_node = node
                if graph.out_degree(node) != 0:
                    h_out = graph.edges[out_edges[0]]['h_upstream'] + graph.edges[out_edges[0]]['d'] # 节点下游管顶标高
                    h_in = min(graph.edges[in_edges[i]]['h_downstream'] + graph.edges[in_edges[i]]['d'] for i in range(len(in_edges))) # 节点上游最低的管顶标高 
                    # print(h_in, h_out)
                    if h_in < h_out:
                        print('存在节点逆坡')
        # 检测是否还存在逆坡
        for edge in graph.edges():
            if graph.edges[edge]['h_upstream'] < graph.edges[edge]['h_downstream']:
                print('存在管段逆坡')
                break
        return graph

    def nodes_bottom_elevation_detection(self, graph: nx.DiGraph):
        wrong_bottom_elevation_nodes = []
        for node in graph.nodes():
            if graph.in_degree(node) == 0:
                out_edges = list(graph.out_edges(node)) # source_node = node
                h_out = min(graph.edges[edge]['h_upstream'] for edge in out_edges)
                if h_out - graph.nodes[node]['h_bottom'] < 0 or h_out - graph.nodes[node]['h_bottom'] > 0.1:
                    graph.nodes[node]['h_bottom'] = h_out
                    wrong_bottom_elevation_nodes.append(node)
            elif graph.out_degree(node) == 0:
                in_edges = list(graph.in_edges(node))
                h_in = min(graph.edges[edge]['h_downstream'] for edge in in_edges)
                if h_in - graph.nodes[node]['h_bottom'] < 0 or h_in - graph.nodes[node]['h_bottom'] > 0.1:
                    graph.nodes[node]['h_bottom'] = h_in
                    wrong_bottom_elevation_nodes.append(node)
            else:
                out_edges = list(graph.out_edges(node)) # source_node = node
                in_edges = list(graph.in_edges(node))
                h_out = min(graph.edges[edge]['h_upstream'] for edge in out_edges)
                h_in = min(graph.edges[edge]['h_downstream'] for edge in in_edges)
                h_min = min(h_out, h_in)
                if h_min - graph.nodes[node]['h_bottom'] < 0 or h_min - graph.nodes[node]['h_bottom'] > 0.1:
                    graph.nodes[node]['h_bottom'] = h_min
                    wrong_bottom_elevation_nodes.append(node)
            # print(graph.nodes[node]['h_bottom'])
        print(f'存在{len(wrong_bottom_elevation_nodes)}个井底标高错误的节点')

        return graph

    def ideal_gravity_flow(self, inflow_nodes: list):
        """
        1. 删除无入流的源节点;
        2. 逆坡检测与修正(管段逆坡、节点逆坡);
        3. 井底标高检测与修正
        """
        graph = copy.deepcopy(self.G)
        # ------------------------ 删除无入流的源节点 ----------------------------
        # all_nodes = list(graph.nodes())
        # record_descendants = []
        # for node in inflow_nodes:
        #     descendants = nx.descendants(graph, node)
        #     record_descendants+=list(descendants)
        # record_descendants+=inflow_nodes
        # no_flow_nodes = [item for item in all_nodes if item not in record_descendants]
        # print('len(no_flow_nodes): ', len(no_flow_nodes))
        # graph.remove_nodes_from(no_flow_nodes)
        # print(graph)
        # nx.draw_networkx(graph, self.nodes_pos, with_labels=False, node_color='blue', node_size=30, arrowsize=5, alpha=0.5)
        # plt.show()
        # ------------------ 逆坡检测与修正(管段逆坡和点逆坡) -----------------------------
        graph = self.add_edges_elevation_attr(graph)
        graph = self.add_nodes_elevation_attr(graph)
        # ---------------------------[管段逆坡]------------------------------------------
        graph = self.reverse_slope_conduits_detection(graph)
        # ---------------------------[节点逆坡]-------------------------------------------
        graph = self.reverse_slope_nodes_detection(graph)
        # ------------------------ 井底标高检测与修正 ----------------------------
        graph = self.nodes_bottom_elevation_detection(graph)
        return graph
    
    def graph_to_inp(self, graph: nx.DiGraph, save_path: str):
        # 1. 读取原有 INP 文件
        inp = copy.deepcopy(SwmmInput.read_file(self.inp_file))
        # 2. 基于 DiGraph 属性进行更新
        # [JUNCTIONS][OUTFALLS]节点属性更新
        inp_junctions = inp[sections.JUNCTIONS].frame.reset_index()
        inp_junctions_depth = dict(zip(inp_junctions['name'], inp_junctions['depth_max']))
        for node, attr in graph.nodes(data=True):
            if node in inp[sections.JUNCTIONS]:
                # 更新管底高程（elevation）
                inp[sections.JUNCTIONS][node]['elevation'] = attr['h_bottom']
            elif node in inp[sections.OUTFALLS]:
                # 如果是出水口，也可以类似处理
                inp[sections.OUTFALLS][node]['elevation'] = attr['h_bottom']
        # [CONDUITS]管道属性更新
        for u, v, attr in graph.edges(data=True):
            # conduit_name = attr.get('name', f'{u}_{v}')
            conduit_name = attr['label']
            if conduit_name in inp[sections.CONDUITS]:
                # 更新'offset_upstream'和'offset_downstream', 直接用conduit_name可能会有问题, 通过u和v来获取
                inp[sections.CONDUITS][conduit_name]['offset_upstream'] = attr['h_upstream']
                inp[sections.CONDUITS][conduit_name]['offset_downstream'] = attr['h_downstream']

        # 3. 保存为新文件
        inp.write_file(save_path)

        print('已完成 INP 文件属性更新')

if __name__ == '__main__':
    inp_file = './temp/fhq_dwf_nooffset.inp'
    graph_obj = graph_create_from_inp(inp_file)
    graph = graph_obj.G
    print(graph)

    inp = SwmmInput.read_file(inp_file)
    inflow_nodes = list(set(inp[sections.DWF].frame.reset_index()['node'].tolist()))
    # print(inflow_nodes)
    # graph_obj.add_nodes_elevation_attr(graph)
    # graph_obj.add_edges_elevation_attr(graph)
    graph_ideal = graph_obj.ideal_gravity_flow(inflow_nodes)
    graph_obj.graph_to_inp(graph_ideal, './temp/fhq_dwf_nooffset_ideal.inp')