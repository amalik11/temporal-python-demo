import asyncio
import logging
from temporalio import activity, workflow
from Banking import BankingService,bank,mockBank

# Define the Withdraw activity
@activity.defn(name="Withdraw")
async def Withdraw(amount, data):
    logging.info(f"Withdrawing ${amount} from account {data['SourceAccount']}.\n\n")
    
    reference_id = f"{data['ReferenceID']}-withdrawal"
    bank = BankingService("bank-api.example.com")
    confirmation, err = bank.Withdraw(data['SourceAccount'], amount, reference_id)
    return confirmation, err
# Define the Deposit activity
@activity.defn(name="Deposit")
async def Deposit(amount, data):
    logging.info(f"Depositing ${amount} into account {data['TargetAccount']}.\n\n")
    
    reference_id = f"{data['ReferenceID']}-deposit"
    bank = BankingService("bank-api.example.com")
    # Uncomment the next line and comment the one after that to simulate an unknown failure
    # confirmation, err = bank.DepositThatFails(data['TargetAccount'], amount, reference_id)
    confirmation, err = bank.Deposit(data['TargetAccount'], amount, reference_id)
    return confirmation, err
# Define the Refund activity
@activity.defn(name="Refund")
async def Refund(amount, data):
    logging.info(f"Refunding ${amount} back into account {data['SourceAccount']}.\n\n")
    
    reference_id = f"{data['ReferenceID']}-refund"
    bank = BankingService("bank-api.example.com")
    confirmation, err = bank.Deposit(data['SourceAccount'], amount, reference_id)
    return confirmation, err
