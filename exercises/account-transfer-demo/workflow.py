import time
from temporalio import activity, workflow, retry_policy
class MoneyTransferWorkflow:
    @workflow.money_transfer
    async def money_transfer(cls, input: PaymentDetails) -> str:
        retrypolicy = retry_policy(
            initial_interval=datetime.timedelta(seconds=1),
            backoff_coefficient=2.0,
            maximum_interval=datetime.timedelta(seconds=100),
            maximum_attempts=0,
            non_retryable_error_types={"InvalidAccountError", "InsufficientFundsError"}
        )
        
        options = Workflow.ActivityOptions(
            start_to_close_timeout=datetime.timedelta(minutes=1),
            retry_policy=retrypolicy
        )
        
        ctx = Workflow.new_activity_context(options=options)
        
        try:
            withdraw_output = await ctx.execute_activity(Withdraw, input)
        except Exception as withdraw_err:
            return str(withdraw_err)
        
        try:
            deposit_output = await ctx.execute_activity(Deposit, input)
        except Exception as deposit_err:
            try:
                result = await ctx.execute_activity(Refund, input)
            except Exception as refund_err:
                return f"Deposit: failed to deposit money into {input['TargetAccount']}: {deposit_err}. Money could not be returned to {input['SourceAccount']}: {refund_err}"
            
            return f"Deposit: failed to deposit money into {input['TargetAccount']}: Money returned to {input['SourceAccount']}: {deposit_err}"
        
        result = f"Transfer complete (transaction IDs: {withdraw_output}, {deposit_output})"
        return result
