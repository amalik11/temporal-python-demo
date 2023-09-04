# Define the shared task queue name in Python
MoneyTransferTaskQueueName = "TRANSFER_MONEY_TASK_QUEUE"
# Define the PaymentDetails struct in Python
class PaymentDetails:
    def __init__(self, source_account, target_account, amount, reference_id):
        self.SourceAccount = source_account
        self.TargetAccount = target_account
        self.Amount = amount
        self.ReferenceID = reference_id
