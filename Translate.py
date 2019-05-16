# -*- coding: utf-8 -*-

# This simple app uses the '/translate' resource to translate text from
# one language to another.

# This sample runs on Python 2.7.x and Python 3.x.
# You may need to install requests and uuid.
# Run: pip install requests uuid

import os, requests, uuid, json

# Checks to see if the Translator Text subscription key is available
# as an environment variable. If you are setting your subscription key as a
# string, then comment these lines out.
# if 'TRANSLATOR_TEXT_KEY' in os.environ:
#     subscriptionKey = os.environ['TRANSLATOR_TEXT_KEY']
# else:
#     print('Environment variable for TRANSLATOR_TEXT_KEY is not set.')
#     exit()
# If you want to set your subscription key as a string, uncomment the next line.
subscriptionKey = '595d98c5e31b4cfb844e074cb463e847'

# If you encounter any issues with the base_url or path, make sure
# that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
base_url = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'
# params = '&to=de&to=it'
params = '&from=zh-Hans&to=en'
constructed_url = base_url + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


def translate(file_path, trans_path):
    # texts = []
    f_save = open(trans_path, "w", encoding="utf-8")

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            tmp_line = line.strip()
            text = tmp_line
            body = [{'text': text}]
            request = requests.post(constructed_url, headers=headers, json=body)
            response = request.json()[0]
            print(text)
            print(response)
            result = response['translations'][0]['text']
            f_save.write(result + '\n')

    f_save.close()

    # body = [{'text': _t} for _t in texts]
    #
    # print(body)
    # request = requests.post(constructed_url, headers=headers, json=body)
    # response = request.json()
    # print(response)
    #
    # f_save = open(trans_path, "w", encoding="utf-8")
    #
    # for r in response:
    #     print(r)
    #     for t in r['translations']:
    #         text = t["text"]
    #         f_save.write(text + "\n")
    #
    # f_save.close()

if __name__ == "__main__":
    translate("zh_info.txt", "en_bing.txt")
