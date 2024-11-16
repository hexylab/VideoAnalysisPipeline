# pipeline/pipeline.py

import networkx as nx
import matplotlib.pyplot as plt

class Pipeline:
    def __init__(self, frame):
        self.graph = nx.DiGraph()  # DAGのためのグラフ
        self.frame = frame  # フレームオブジェクト

    def add_step(self, step, dependencies=[]):
        """パイプラインにステップを追加"""
        step_name = self._get_step_name(step)  # ノードラベルを生成
        self.graph.add_node(step_name, func=step)  # ノードとしてラベルと関数を登録
        for dep in dependencies:
            dep_name = self._get_step_name(dep)
            self.graph.add_edge(dep_name, step_name)  # エッジを追加
        return self

    def execute(self):
        """パイプラインを実行"""
        for step_name in nx.topological_sort(self.graph):
            step = self.graph.nodes[step_name]['func']
            self.frame = step(self.frame)  # ステップごとにフレームを処理
        return self.frame
    
    def save_dag_image(self, output_path="pipeline_dag.png"):
        ag = nx.nx_agraph.to_agraph(self.graph)
        ag.node_attr.update(shape='ellipse', style='filled', color='lightblue', fontsize=12)
        ag.edge_attr.update(color='black', arrowsize=1)
        ag.graph_attr.update(rankdir='TD', fontsize=14)
        ag.draw(output_path, format='png', prog='dot')
        print(f"DAG image saved to {output_path}")

    def _get_step_name(self, step):
        """関数またはメソッドのフルネームを生成"""
        if hasattr(step, '__self__') and step.__self__ is not None:
            return f"{step.__self__.__class__.__name__}.{step.__name__}"
        elif hasattr(step, '__name__'):  # 関数
            return step.__name__
        else:
            raise ValueError("Step must be a callable object with a __name__ attribute.")
