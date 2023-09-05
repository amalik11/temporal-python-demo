import time
import datetime
import shared
import activity_def
from temporalio import activity, workflow
from temporalio.common import RetryPolicy
@workflow.defn(name="MoneyTransferWorkflow")
class MoneyTransferWorkflow:
    @workflow.run
    async def run(cls, input: shared.PaymentDetails) -> str:
        retrypolicy = RetryPolicy(
            initial_interval=datetime.timedelta(seconds=1),
            backoff_coefficient=2.0,
            maximum_interval=datetime.timedelta(seconds=100),
            maximum_attempts=0,
            non_retryable_error_types={"InvalidAccountError", "InsufficientFundsError"}
        )
        
        options = workflow.ActivityOptions(
            start_to_close_timeout=datetime.timedelta(minutes=1),
            retry_policy=retrypolicy
        )
        
        ctx = workflow.new_activity_context(options=options)
        
        try:
            withdraw_output = await ctx.execute_activity(activity_def.Withdraw, input)
        except Exception as withdraw_err:
            return str(withdraw_err)
        
        try:
            deposit_output = await ctx.execute_activity(activity_def.Deposit, input)
        except Exception as deposit_err:
            try:
                result = await ctx.execute_activity(activity_def.RefundRefund, input)
            except Exception as refund_err:
                return f"Deposit: failed to deposit money into {input['TargetAccount']}: {deposit_err}. Money could not be returned to {input['SourceAccount']}: {refund_err}"
            
            return f"Deposit: failed to deposit money into {input['TargetAccount']}: Money returned to {input['SourceAccount']}: {deposit_err}"
        
        result = f"Transfer complete (transaction IDs: {withdraw_output}, {deposit_output})"
        return result
