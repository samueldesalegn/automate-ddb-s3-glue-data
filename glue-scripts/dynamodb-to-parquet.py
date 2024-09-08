import boto3
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Your DynamoDB table name and S3 bucket details
table_name = "event_feedback"
bucket_name = "aws-customer-survey-analytics"
output_path = "events_parquet/"

# Fetch data from DynamoDB
def fetch_dynamodb_data():
    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response['Items']
    return items

# Convert the data to Parquet format
def convert_to_parquet(data):
    df = pd.DataFrame(data)
    
    # Ensure schema is aligned
    df['event_rate'] = pd.to_numeric(df['event_rate'], errors='coerce')
    df['presentation_content'] = pd.to_numeric(df['presentation_content'], errors='coerce')
    df['session_duration'] = pd.to_numeric(df['session_duration'], errors='coerce')

    table = pa.Table.from_pandas(df)
    return table

# Upload the Parquet file to S3
def upload_to_s3(parquet_table):
    pq.write_table(parquet_table, '/tmp/temp_data.parquet')
    s3.upload_file('/tmp/temp_data.parquet', bucket_name, output_path + 'data.parquet')

# Main function
def main():
    # Fetch the data
    dynamo_data = fetch_dynamodb_data()

    # Convert to Parquet
    parquet_data = convert_to_parquet(dynamo_data)

    # Upload to S3
    upload_to_s3(parquet_data)

if __name__ == "__main__":
    main()
