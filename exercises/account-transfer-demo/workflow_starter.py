import logging
import asyncio
from temporalio import workflow , activity
import asyncio
import shared 
import json
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import MoneyTransferWorkflow
from activity_def import  Withdraw,Deposit,Refund

async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233")
    input_data = shared.PaymentDetails(source_account="12345", target_account="67890", amount=50, reference_id="PAY12345")
    # Convert PaymentDetails to a dictionary
    ##payment_dict = shared.PaymentDetails.to_dict(input_data)

    # Serialize the dictionary to JSON
    json_string = json.dumps(input_data)
    ##options = MoneyTransferWorkflow()
        
    ##logging.info(f"Starting transfer from account {input_data['source_account']} to account {input_data['target_account']} for {input_data['amount']}")

    ##workflow_execution = await client.execute_workflow(MoneyTransferWorkflow.run, input_data, id= "pay-invoice-701", task_queue=shared.MoneyTransferTaskQueueName)   
    ##logging.info(f"WorkflowID: {workflow_execution.workflow_id} RunID: {workflow_execution.run_id}")
    async with Worker(
        client,
        task_queue="TRANSFER_MONEY_TASK_QUEUE",
        workflows=[MoneyTransferWorkflow],
        activities=[Withdraw,Deposit,Refund],
    ):

        # While the worker is running, use the client to run the workflow and
        # print out its result. Note, in many production setups, the client
        # would be in a completely separate process from the worker.
        result = await client.execute_workflow(
            MoneyTransferWorkflow.run,
            json_string,
            id="pay-invoice-701",
            task_queue=shared.MoneyTransferTaskQueueName,
            
        )
        print(f"Result: {result}")
if __name__ == "__main__":
    asyncio.run(main())
