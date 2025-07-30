from aws_s3_controller import load_excel_in_bucket, scan_bucket


def load_menuESAFE500068(date_ref=None):
    bucket = 'dataset-system'
    bucket_prefix = 'dataset-menuESAFE500068'
    regex = f'menuESAFE500068-account000000000-at{date_ref.replace("-","")}' if date_ref else f'menuESAFE500068-account000000000'
    file_name = scan_bucket(bucket=bucket, bucket_prefix=bucket_prefix, regex=regex, option='name')[-1]
    df = load_excel_in_bucket(bucket=bucket, bucket_prefix=bucket_prefix, regex=file_name)
    return df