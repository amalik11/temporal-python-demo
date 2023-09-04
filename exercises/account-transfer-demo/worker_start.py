import logging
import asyncio
from temporal.activity import Activity
from temporal.workerfactory import WorkerFactory

import money_transfer_project_template_go.app as app

def main():
    logging.basicConfig(level=logging.INFO)

    # Connect to the Temporal service
    worker_factory = WorkerFactory("localhost", 7233)
    worker = worker_factory.new_worker("TRANSFER_MONEY_TASK_QUEUE")

    # Register workflows and activities
    worker.register_workflow_implementation_type(app.MoneyTransferWorkflowImpl)
    worker.register_activities_implementation(app.BankingService())
    
    # Start listening to the Task Queue
    worker.start()
    
    # Run the event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

if __name__ == "__main__":
    main()

import asyncio

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from workflow import CertificateGeneratorWorkflow


async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client,
        task_queue="TRANSFER_MONEY_TASK_QUEUE",
        workflows=[CertificateGeneratorWorkflow],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())