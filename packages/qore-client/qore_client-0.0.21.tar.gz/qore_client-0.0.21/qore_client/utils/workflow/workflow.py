from typing import Any, Dict, List, Literal

from qore_client.utils.workflow.component import Workflow


class WorkflowOperations:
    """Workflow operation utilities for QoreClient"""

    def __init__(self, request_method):
        """
        Initialize with the request method from the parent client

        :param request_method: The _request method from QoreClient
        """
        self._request = request_method

    def get_published_workflow_detail(self, workflow_id: str) -> dict:
        """Published 워크플로우 상세 정보를 가져옵니다."""
        response = self._request("GET", f"/api/workflow/{workflow_id}")
        return response

    def get_draft_workflow_detail(self, workflow_id: str) -> dict:
        """Draft 워크플로우 상세 정보를 가져옵니다."""
        response = self._request("GET", f"/api/workflow/{workflow_id}/draft")
        return response

    def get_version_workflow_detail(self, workflow_id: str, version: str) -> dict:
        """Version 워크플로우 상세 정보를 가져옵니다."""
        response = self._request("GET", f"/api/workflow/{workflow_id}/{version}")
        return response

    def create_workflow(self, workspace_id: str, workflow_name: str, description: str = "") -> dict:
        """워크플로우를 생성합니다."""
        response = self._request(
            "POST",
            "/api/workflow/create",
            data={"workspace_id": workspace_id, "name": workflow_name, "description": description},
        )
        return response

    def execute_workflow(self, workflow_id: str, workflow: Workflow) -> dict:
        """워크플로우를 실행합니다."""
        response = self._request(
            "POST", f"/api/workflow/{workflow_id}/draft/execute", json=workflow.to_dict()
        )
        return response

    def save_workflow(self, workflow_id: str, workflow: Workflow) -> dict:
        """워크플로우를 저장합니다."""
        return self._request(
            "PUT", f"/api/workflow/{workflow_id}/draft/save", json=workflow.to_dict()
        )

    def get_workflow_versions(self, workflow_id: str) -> List[dict]:
        """워크플로우의 버전 목록을 가져옵니다."""
        return self._request("GET", f"/api/workflow/{workflow_id}/versions")

    def execute_published_workflow(
        self,
        workflow_id: str,
        format: Literal["raw", "logs"] = "logs",
        version: Literal["latest"] | int = "latest",
        **kwargs,
    ) -> List[str] | Dict[str, Any]:
        """Published 워크플로우를 실행합니다."""
        response_data = self._request(
            "POST", f"/api/workflow/{workflow_id}/{version}/execute", json=kwargs
        )

        if response_data is None:
            raise ValueError("Failed to execute workflow, received None response.")

        if format == "logs":
            return extract_logs(response_data)
        elif format == "raw":
            return response_data
        else:
            raise ValueError(f"Invalid format: {format}")


def extract_logs(workflow_result: Dict[str, Any]) -> List[str]:
    """
    워크플로우 실행 결과에서 logs만 추출하여 리스트로 반환

    :param workflow_result: execute_workflow의 원본 결과
    :return: 각 노드의 logs를 담은 리스트 (None이 아닌 것만)
    """
    logs = []
    for _, node_data in workflow_result.items():
        execute_result = node_data.get("execute_result", {})
        log_content = execute_result.get("logs")
        if log_content:
            logs.append(log_content)
    return logs
