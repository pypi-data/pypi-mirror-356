import re

import torch
from transformers import BitsAndBytesConfig, AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoConfig
from peft import AutoPeftModelForCausalLM
import transformers

from ..errors.model_not_loaded import ModelNotLoaded
from ..errors.model_already_loaded import ModelAlreadyLoaded


class AddressParserModel:
    __RESPONSE_START_TOKEN = '<start_of_turn>model\n'
    __RESPONSE_END_TOKEN = '<end_of_turn>'

    def __init__(self, hf_model_path: str, hf_token: str, max_output_length: int=300):
        self.__model_path = hf_model_path
        self.__hf_token = hf_token
        self.__max_output_length = max_output_length
        self.__tokenizer = None
        self.__model = None

    def __create_model_kwargs__(self) -> dict[str, str | bool]:
        model_args: dict[str, str | bool] = {
            'torch_dtype': torch.bfloat16,
            'token': self.__hf_token,
            'quantization_config': BitsAndBytesConfig(load_in_4bit=True),
            'device': 'cuda'
        }

        return model_args

    def load(self):
        transformers.logging.set_verbosity_error()

        if self.__tokenizer is not None or self.__model is not None:
            raise ModelAlreadyLoaded

        self.__tokenizer = AutoTokenizer.from_pretrained(
            self.__model_path,
            token=self.__hf_token
        )
        self.__model = AutoPeftModelForCausalLM.from_pretrained(self.__model_path, **self.__create_model_kwargs__()).eval()

    @staticmethod
    def __create_prompt__(raw_address_text: str) -> str:
        return f'Convert the following address to JSON:\n{raw_address_text}'


    def parse_address(self, raw_address_text: str) -> str:
        if self.__tokenizer is None or self.__model is None:
            raise ModelNotLoaded

        conversation = [{'role': x[0], 'content': [{'type': 'text', 'text': x[1]}]} for x in [
            ('system', 'You are a JSON-only canadian address parser. Given the input address fields, extract and output only a valid JSON object with these keys: [\"address_line\", \"city\", \"province_code\", \"postal_code\"]. Do not emit any extra text, explanations, or punctuation outside the JSON.'),
            ('user', self.__create_prompt__(raw_address_text))
        ]]

        tokenized = self.__tokenizer.apply_chat_template(
            conversation,
            padding=True,
            truncation=True,
            return_tensors='pt',
            add_generation_prompt=True
        ).to('cuda')
        res = self.__model.generate(tokenized, max_new_tokens=self.__max_output_length)
        res = str(self.__tokenizer.batch_decode(res)[0])

        res = re.sub(r'```json\n?', '', res)
        res = res.replace('```', '')
        res = res[res.index(self.__RESPONSE_START_TOKEN) + len(self.__RESPONSE_START_TOKEN):]
        res = res[:res.index(self.__RESPONSE_END_TOKEN)].strip()

        return res