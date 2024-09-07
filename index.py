import boto3
import json
import time

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Step 1: Create the table
def create_table():
    try:
        table = dynamodb.create_table(
            TableName='event_feedback',
            KeySchema=[
                {
                    'AttributeName': 'event_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'event_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName='event_feedback')
        print("Table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")

# Step 2: Batch write the data from the JSON file
def batch_write_data():
    table = dynamodb.Table('event_feedback')

    # Load data from the JSON file
    with open('batch_events.json', 'r') as json_file:
        events = json.load(json_file)

    with table.batch_writer() as batch:
        for event in events:
            batch.put_item(Item=event)
    print("Batch write completed!")

# Main function to run the process
if __name__ == "__main__":
    create_table()
    time.sleep(5)  # Wait for the table to be fully created
    batch_write_data()
