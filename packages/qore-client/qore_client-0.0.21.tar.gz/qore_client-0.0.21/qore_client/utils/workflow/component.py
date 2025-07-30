import time
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from qore_client import QoreClient


class Edge(BaseModel):
    id: str
    source: str
    target: str
    type: str = "custom"
    marker_end: dict = Field(
        default_factory=lambda: {"type": "arrowclosed", "width": 24, "height": 24}
    )


class Position(BaseModel):
    x: float
    y: float


class Measured(BaseModel):
    width: float
    height: float


class NodeData(BaseModel):
    label: str
    type: Optional[str] = None


class CodeNodeData(NodeData):
    code: str
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)

    type: str = "code"
    language: str = "python"


class Node(BaseModel):
    id: str
    data: NodeData | CodeNodeData
    position: Position = Field(default_factory=lambda: Position(x=0, y=0))
    measured: Measured = Field(default_factory=lambda: Measured(width=176, height=60))
    type: str = "custom"
    deletable: bool = True
    selected: bool = False
    dragging: bool = False


class Workflow(BaseModel):
    nodes: List[Node] = []
    edges: List[Edge] = []

    @classmethod
    def from_dict(cls, workflow_json: dict):
        return cls.model_validate(workflow_json)

    def to_dict(self):
        return self.model_dump(mode="json")

    @classmethod
    def from_qore(cls, client: "QoreClient", workflow_id: str, diagram: bool = True):
        wf_json = client.get_workflow(workflow_id, diagram=diagram)
        return cls.model_validate(wf_json)

    def to_qore(self, client: "QoreClient", workflow_id: str):
        client.save_workflow(workflow_id, self.to_dict())

    def get_edges(self):
        """
        현재 워크플로우의 edges를 반환한다.
        edges: {source_id: [target_id, ...], ...}
        """
        from collections import defaultdict

        edges = defaultdict(list)
        for edge in self.edges:
            edges[edge.source].append(edge.target)
        return dict(edges)

    def get_nodes(self, summary: bool = True):
        """
        노드 목록을 반환합니다.
        summary=True일 경우, 가독성을 위해 주요 정보만 담은 dict 리스트를 반환합니다.
        """
        if not summary:
            return self.nodes

        node_summaries = []
        for node in self.nodes:
            node_info = {
                "id": node.id,
                "label": node.data.label,
                "type": getattr(node.data, "type", None),
            }
            if isinstance(node.data, CodeNodeData):
                node_info["code"] = node.data.code
            node_summaries.append(node_info)
        return node_summaries

    def add_node(self, data: NodeData | CodeNodeData):
        node_id = str(int(time.time() * 1000))

        node = Node(
            id=node_id,
            data=data,
        )

        self.nodes.append(node)
        return node.id

    def add_code_node(
        self,
        code: str,
        label: str = "Code",
        inputs: Optional[list[str]] = None,
        outputs: Optional[list[str]] = None,
    ):
        node_id = self.add_node(
            CodeNodeData(
                code=code,
                inputs=inputs or [],
                outputs=outputs or [],
                label=label,
            )
        )

        edges = self.get_edges()
        self._arrange_nodes_by_edges(edges)
        return node_id

    def set_edges(self, edges: dict):
        """
        edges: {source_id: [target_id, ...], ...}
        현재 워크플로우의 노드들을 그대로 사용하고,
        edges에 맞게 edges를 새로 생성하며,
        노드 배치는 arrange_nodes_by_edges로 수행한다.
        """
        node_ids = {node.id for node in self.nodes}
        # 1. edges 새로 생성
        new_edges = []
        edge_id = 0
        for src, targets in edges.items():
            for tgt in targets:
                if src in node_ids and tgt in node_ids:
                    new_edges.append(Edge(id=f"edge-{edge_id}", source=src, target=tgt))
                    edge_id += 1
        self.edges = new_edges
        # 2. 노드 배치
        self._arrange_nodes_by_edges(edges)

    def _arrange_nodes_by_edges(self, edges: dict, x_gap=250, y_gap=100, start_x=0, start_y=0):
        """
        edges를 기반으로 위상정렬하여 노드 위치를 배치한다.
        """
        # 위상정렬
        from collections import defaultdict, deque

        indegree: dict[str, int] = defaultdict(int)
        graph = defaultdict(list)
        for src, tgts in edges.items():
            for tgt in tgts:
                graph[src].append(tgt)
                indegree[tgt] += 1
                if src not in indegree:
                    indegree[src] = indegree[src]  # ensure src in indegree
        # 노드 id -> Node 객체 매핑
        node_map = {node.id: node for node in self.nodes}
        # 진입차수 0인 노드부터 시작
        queue = deque([nid for nid in node_map if indegree[nid] == 0])
        visited = set()
        layer = 0
        pos_map = {}
        while queue:
            layer_size = len(queue)
            for i in range(layer_size):
                nid = queue.popleft()
                if nid in visited:
                    continue
                visited.add(nid)
                node = node_map[nid]
                node.position.x = start_x + x_gap * layer
                node.position.y = start_y + y_gap * i
                pos_map[nid] = (node.position.x, node.position.y)
                for next_nid in graph[nid]:
                    indegree[next_nid] -= 1
                    if indegree[next_nid] == 0:
                        queue.append(next_nid)
            layer += 1
        return self
