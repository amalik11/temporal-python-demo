import logging
import asyncio
from temporalio import activity,worker, client
from workflow import MoneyTransferWorkflow
from Banking import BankingService
from activity_def import  Withdraw,Deposit,Refund
# ...
# ...
async def main():
    logging.basicConfig(level=logging.INFO)
    client = await client.connect("localhost:7233")
    worker = worker(
        client,
        task_queue="TRANSFER_MONEY_TASK_QUEUE",
        workflows=[MoneyTransferWorkflow],
        activities=[Withdraw,Deposit,Refund],
    )
       # Start listening to the Task Queue
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
