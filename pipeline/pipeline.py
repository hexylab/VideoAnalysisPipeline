# pipeline/pipeline.py
import networkx as nx

class Pipeline:
    def __init__(self, frame):
        self.graph = nx.DiGraph()  # DAGのためのグラフ
        self.frame = frame  # フレームオブジェクト

    def add_step(self, step, dependencies=[]):
        self.graph.add_node(step)
        for dep in dependencies:
            self.graph.add_edge(dep, step)
        return self

    def execute(self):
        for step in nx.topological_sort(self.graph):
            self.frame = step(self.frame)  # ステップごとにフレームを処理
        return self.frame