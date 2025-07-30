import datetime
import json
import time
from random import shuffle

from src.canadian_address_parser.address_parser import AddressParser
from src.canadian_address_parser.data.raw_address import RawAddress
from src.canadian_address_parser.errors.unable_parse_model_output import UnableToParseModelOutputError

def create_sample_test_log(input: str, output: str, duration: float | None) -> str:
    return '\n'.join([f'Input:  {input}', f'Output: {output}', f'Duration: {f"{duration:.2f}s" if duration else "N/A"}'])

def create_log_headers(headers: list[tuple[str, str]]) -> str:
    return '\n'.join(f'{label}: {value}' for label, value in headers)

def create_results_log(sample_count: int, model_path: str, sample_logs: list[str]) -> str:
    headers = [
        ('Sample Count', f'{sample_count}'),
        ('Model Path', f'{model_path}'),
        ('Date', f'{datetime.datetime.now().strftime("%Y/%m/%d %H:%M")}'),
    ]
    log = f'{create_log_headers(headers)}\n\n\n{'\n\n'.join(sample_logs)}'
    return log

def test_addresses(address_parser: AddressParser, jonas_samples_path: str, log_file_path: str, model_path: str, max_samples: int = -1) -> None:
    with open(jonas_samples_path, 'r') as f_handle:
        file_content = f_handle.read()

    json_content = json.loads(file_content)
    shuffle(json_content)

    res = list(filter(lambda x: x.province_code is not None,
                      [RawAddress(
                            address_line_1=x["AddressLine1"],
                            address_line_2=x["AddressLine2"],
                            address_line_3=x["AddressLine3"],
                            address_line_4=x["AddressLine4"],
                            postal_code=x["PostalZipCode"],
                            province_code=x["ProvinceStateCountyCode"]
                      ) for x in [x['raw'] for x in json_content]]))[:max_samples]

    sample_logs: list[str] = []

    for sample in res:
        try:
            start_time = time.time()
            output = address_parser.parse_address(sample)
            end_time = time.time()
            sample_logs.append(create_sample_test_log(f'{sample}', f'{output}', end_time - start_time))
        except UnableToParseModelOutputError:
            sample_logs.append(create_sample_test_log(f'{sample}', 'ERROR - Unable to parse the output from the model', None))

    results_log = create_results_log(len(res), model_path, sample_logs)
    with open(log_file_path, 'w') as f_handle:
        f_handle.write(results_log)