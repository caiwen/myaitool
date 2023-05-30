import os
import openai

import approot
from tools.mytools import MyTools

openai.organization = os.getenv("OPENAI_API_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAi:
    @staticmethod
    def model_list():
        openai.Model.list()

    @staticmethod
    def create_completion(model, prompt):
        completion = openai.Completion.create(model=model, prompt=prompt)
        return completion

    @staticmethod
    def create_image(prompt, n, size, response_format='b64_json'):
        image_resp = openai.Image.create(prompt=prompt, n=n, size=size, response_format=response_format)
        return image_resp


if __name__ == '__main__':
    data = OpenAi.create_image(
        prompt="一只狗",
        n=5, size="512x512", response_format='url')
    print(data)