import pickle
from typing import Union

import numpy as np
import pydantic_models as pm
from app.app import database
from app.chat.models import available_models_dict
from app.chat.workflows.classification import (
    ClassificationWorkflow,
    evaluate_classification,
)
from app.chat.workflows.extraction import ExtractionWorkflow
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.security import check_key
from fastapi import Depends

router = APIRouter(prefix="/{username}/workflows", tags=["workflows"])


@router.get("", response_model=list[pm.Workflow])
def workflows_get(username: str, auth=Depends(check_key)) -> list[pm.Workflow]:
    """Get workflows by username."""
    user_workflows = list(database.workflows.find_by({"username": username}))
    for workflow in user_workflows:
        workflow.calibrators = None

    return user_workflows


@router.put("", response_model=pm.CreateWorkflowResponse)
def workflows_put(
    workflow: pm.Workflow, username: str, auth=Depends(check_key)
) -> pm.CreateWorkflowResponse:
    """Create a workflow with the given name, username."""
    existing_workflow = database.workflows.find_one_by_id(workflow.id)
    if (
        existing_workflow is None or existing_workflow.classes != workflow.classes
    ) and workflow.task.lower() == "classification":
        workflow.class_thresholds = {c: 0 for c in workflow.classes}
    database.workflows.save(workflow)
    return pm.CreateWorkflowResponse(
        message="Workflow created successfully!", workflow_id=str(workflow.id)
    )


@router.get("/{workflow_id}")
def get_workflow(
    workflow_id: str, username: str, auth=Depends(check_key)
) -> Union[pm.Workflow, None]:
    """Get workflow by id."""
    workflow = database.workflows.find_one_by_id(ObjectId(workflow_id))
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    workflow.calibrators = None
    return workflow


@router.delete("/{workflow_id}")
def delete_workflow(
    workflow_id: str, username: str, auth=Depends(check_key)
) -> pm.MessageResponse:
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


@router.put(
    "/{workflow_id}/instructions",
    responses={400: {"description": "Error changing instructions"}},
)
def change_instructions(
    workflow_id: str, workflow_settings: pm.WorkflowSettings, auth=Depends(check_key)
) -> dict:
    """Change the instructions and classes of the workflow."""
    workflow = database.workflows.find_one_by_id(ObjectId(workflow_id))
    print(workflow)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow.instructions = workflow_settings.instructions
    workflow.classes = workflow_settings.classes

    database.workflows.save(workflow)

    return {"message": "Instructions updated successfully!"}


@router.put(
    "/{workflow_id}/model",
    responses={400: {"description": "Error changing model"}},
)
def change_model(workflow_id: str, model: pm.LLM, auth=Depends(check_key)) -> dict:
    """Change the model of the workflow."""
    workflow = database.workflows.find_one_by_id(ObjectId(workflow_id))
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow.model = model

    database.workflows.save(workflow)

    return {"message": "Model updated successfully!"}


@router.post("/{workflow_id}/run")
def run_workflow(
    workflow_id: str,
    username: str,
    message: pm.ClassificationInput,
    auth=Depends(check_key),
) -> tuple[str, float] | list[tuple[str, str, float]]:
    """Run the workflow."""
    workflow: pm.Workflow = get_workflow(workflow_id, username)
    if workflow.model is None:
        raise HTTPException(
            status_code=400, detail="Select a model for the workflow first."
        )
    llm = available_models_dict[workflow.model.name](
        workflow.model.user_variables
    ).as_llm()

    calibrators = pickle.loads(workflow.calibrators) if workflow.calibrators else None

    if workflow.task.lower() == "classification":
        classification_workflow = ClassificationWorkflow(
            classes=workflow.classes,
            instructions=workflow.instructions,
            llm=llm,
            calibrators=calibrators,
        )
        result = classification_workflow.predict(message)
        if result[1] < workflow.class_thresholds[result[0]]:
            return "None", 0.0
    elif workflow.task.lower() == "extraction":
        extraction_workflow = ExtractionWorkflow(
            entities=workflow.entities,
            instructions=workflow.instructions,
            llm=llm,
        )
        result = extraction_workflow.predict(message)
    return result


@router.post("/{workflow_id}/calibrate")
def calibrate_workflow(
    workflow_id: str, username: str, x: list[str], y: list[str], auth=Depends(check_key)
) -> pm.MessageResponse:
    """Calibrate the workflow."""
    workflow: pm.Workflow = get_workflow(workflow_id, username)

    llm = available_models_dict[workflow.model.name](
        workflow.model.user_variables
    ).as_llm()

    if workflow.task.lower() == "classification":
        classification_workflow = ClassificationWorkflow(
            classes=workflow.classes,
            instructions=workflow.instructions,
            llm=llm,
        )
        try:
            y = classification_workflow.encode_labels(y)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        # convert to one hot
        one_hot_y = np.zeros((len(y), len(classification_workflow.classes)))
        for i, class_index in enumerate(y):
            one_hot_y[i, class_index] = 1

        classification_workflow.calibrate(x, one_hot_y)
        workflow.calibrators = pickle.dumps(classification_workflow.calibrators)
        database.workflows.save(workflow)

    else:
        return HTTPException(
            status_code=400, detail="Task not supported for calibration"
        )
    return pm.MessageResponse(message="Workflow calibrated successfully!")


@router.post("/{workflow_id}/evaluate")
def evaluate_workflow(
    workflow_id: str, username: str, x: list[str], y: list[str], auth=Depends(check_key)
) -> dict:
    workflow: pm.Workflow = get_workflow(workflow_id, username)

    llm = available_models_dict[workflow.model.name](
        workflow.model.user_variables
    ).as_llm()
    if workflow.task.lower() != "classification":
        raise HTTPException(
            status_code=400,
            detail="Evaluation is only supported for classification workflows.",
        )
    classification_workflow = ClassificationWorkflow(
        classes=workflow.classes,
        instructions=workflow.instructions,
        llm=llm,
    )
    metrics = evaluate_classification(classification_workflow, x, y)

    return metrics
