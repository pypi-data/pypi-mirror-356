import boto3
from loguru import logger
from contextlib import closing
from FinAnalytics.A.constants import BUCKET_NAME_FIN_TASKS


def main():
    with closing(boto3.client('s3')) as bucket:
        resp = bucket.put_object(
            Bucket=BUCKET_NAME_FIN_TASKS,
            Key="upload-tasks/",
        )
        logger.info(resp)

        resp = bucket.put_object(
            Bucket=BUCKET_NAME_FIN_TASKS,
            Key="examples/",
        )
        logger.info(resp)

        resp = bucket.put_bucket_lifecycle_configuration(
            Bucket=BUCKET_NAME_FIN_TASKS,
            LifecycleConfiguration={
                'Rules': [
                    {
                        'ID': 'DeleteUploadTasksAfter10Days',
                        'Prefix': "upload-tasks/",
                        'Status': 'Enabled',
                        'Expiration': {
                            'Days': 10
                        }
                    }
                ]
            }
        )

        logger.info(resp)


if __name__ == "__main__":
    main()
