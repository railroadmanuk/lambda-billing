def lambda_handler(event, context):
    import boto3 # AWS Python library
    sts_client = boto3.client('sts')
    budget_client = boto3.client('budgets') # create a budgets client
    sns_client = boto3.client('sns') # create a separate SNS client
    account_details = sts_client.get_caller_identity()
    topics = sns_client.list_topics()
    for topic in topics['Topics']:
        if 'billing' in topic['TopicArn']:
            billing_topic = topic['TopicArn']
    budgets = budget_client.describe_budgets(AccountId=account_details['Account'])
    for budget in budgets['Budgets']:
        print ("Actual spend: $"+budget['CalculatedSpend']['ActualSpend']['Amount'])
        print ("Forecasted spend: $"+budget['CalculatedSpend']['ForecastedSpend']['Amount'])
        sns_client.publish(
            TopicArn=billing_topic,
            Subject='Daily Billing Report',
            Message=(
                'Current actual spend is $'
                +budget['CalculatedSpend']['ActualSpend']['Amount']
                +', forecast for the month is $'
                +budget['CalculatedSpend']['ForecastedSpend']['Amount']
            )
        )