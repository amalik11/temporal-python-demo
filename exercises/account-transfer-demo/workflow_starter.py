import logging
import asyncio
import shared 
from temporalio import workflow

from temporal.activity import Activity
from temporal.workerfactory import WorkerFactory
from temporal.workflow import workflow_method, WorkflowClient
import money_transfer_project_template_go.app as app

async def start_workflow():
    logging.basicConfig(level=logging.INFO)

    async with WorkflowClient() as client:
        input_data = {
            "SourceAccount": "85-150",
            "TargetAccount": "43-812",
            "Amount": 250,
            "ReferenceID": "12345",
        }
        options = app.MoneyTransferWorkflowImplOptions(task_queue=shared.MoneyTransferTaskQueueName)
        
        logging.info(f"Starting transfer from account {input_data['SourceAccount']} to account {input_data['TargetAccount']} for {input_data['Amount']}")

        workflow_execution = await client.execute_workflow(app.MoneyTransferWorkflowImpl, input_data, options=options)
        
        logging.info(f"WorkflowID: {workflow_execution.workflow_id} RunID: {workflow_execution.run_id}")

        result = await workflow_execution.result()

        logging.info(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_workflow())
    loop.close()
