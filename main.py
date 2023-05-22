import os
import openai

openai.organization = os.getenv("OPENAI_API_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAi:
    @staticmethod
    def model_list():
        openai.Model.list()

    @staticmethod
    def create_completion(model, prompt):
        completion = openai.Completion.create(model=model, prompt=prompt)
        print(completion.choices[0].text)

    @staticmethod
    def create_image(prompt, n, size):
        image_resp = openai.Image.create(prompt=prompt, n=n, size=size, response_format='b64_json')
        print(image_resp['data'][0]['b64_json'])


if __name__ == '__main__':
    OpenAi.model_list()
    OpenAi.create_image(
        prompt='There is a boat floating in the vast Pacific Ocean. A giant panda and a tiger on board are fighting. The eagles in the sky are cheering for them, but the dolphins in the water persuade them not to fight.',
        n=1, size="512x512")
