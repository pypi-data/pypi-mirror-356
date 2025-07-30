import argparse
import os.path
from dataclasses import dataclass, field

from src.canadian_address_parser.address_parser import AddressParser
from test_addresses import test_addresses


@dataclass(frozen=True)
class CommandArgs:
    model_path: str = field()
    samples_path: str = field()
    hf_token: str = field()
    log_path: str = field()
    max_samples: int = field()

def get_params() -> CommandArgs:
    parser = argparse.ArgumentParser()

    parser.add_argument('hf_token', default='', type=str)
    parser.add_argument("model_path", default="", type=str)
    parser.add_argument("samples_path", default="", type=str)
    parser.add_argument("log_path", default="", type=str)
    parser.add_argument('--max_samples', default=-1, type=int)

    args = parser.parse_args()

    return CommandArgs(
        model_path=args.model_path,
        log_path=args.log_path,
        samples_path=args.samples_path,
        hf_token=args.hf_token,
        max_samples=args.max_samples
    )

if __name__ == "__main__":
    params = get_params()

    address_parser = AddressParser(params.hf_token, params.model_path)
    test_addresses(address_parser, params.samples_path, os.path.relpath(params.log_path), params.model_path, max_samples=params.max_samples)