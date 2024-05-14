from typing import Union

import pydantic_models as pm
from app.app import database
from bson import ObjectId
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{username}/workflows", tags=["workflows"])


@router.get("", response_model=list[pm.Workflow])
def workflows_get(username: str) -> list[pm.Workflow]:
    """Get workflows by username."""
    user_workflows = list(database.workflows.find_by({"username": username}))

    return user_workflows


@router.put("", response_model=pm.CreateWorkflowResponse)
def workflows_put(workflow: pm.Workflow, username: str) -> pm.CreateWorkflowResponse:
    """Create a workflow with the given name, username."""
    database.workflows.save(workflow)
    return pm.CreateWorkflowResponse(message="Workflow created successfully!", workflow_id=str(workflow.id))


@router.get("/{workflow_id}")
def get_workflow(workflow_id: str, username: str) -> Union[pm.Workflow, None]:
    """Get workflow by id."""
    workflow = database.workflows.find_one_by_id(ObjectId(workflow_id))
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.delete("/{workflow_id}")
def delete_workflow(workflow_id: str, username: str) -> pm.MessageResponse:
    """Delete workflow by id."""
    workflow = get_workflow(workflow_id, username)
    database.workflows.delete(workflow)
    # Delete all tasks involving the workflow
    tasks = list(database.tasks.find_by({"workflow_id": ObjectId(workflow_id)}))
    for task in tasks:
        database.tasks.delete(task)
    # Delete all sources of the workflow
    sources = list(database.sources.find_by({"workflow_id": ObjectId(workflow_id)}))
    for source in sources:
        database.sources.delete(source)

    return pm.MessageResponse(message="Workflow deleted successfully!")


@router.put("/{workflow_id}/instructions", responses={400: {"description": "Error changing instructions"}})
def change_instructions(workflow_id: str, workflow_settings: pm.WorkflowSettings):
    """Change the instructions and classes of the workflow."""
    workflow = database.workflows.find_one_by_id(ObjectId(workflow_id))
    print(workflow)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow.instructions = workflow_settings.instructions
    workflow.classes = workflow_settings.classes

    database.workflows.save(workflow)

    return {"message": "Instructions updated successfully!"}
