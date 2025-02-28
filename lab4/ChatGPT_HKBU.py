import configparser
import requests
import logging

class HKBU_ChatGPT:
    def __init__(self, config_='./config.ini'):
        if isinstance(config_, str):
            self.config = configparser.ConfigParser()
            self.config.read(config_)
        elif isinstance(config_, configparser.ConfigParser):
            self.config = config_

    def submit(self, message):
        try:
            conversation = [{"role": "user", "content": message}]
            url = (self.config['CHATGPT']['BASICURL'] +
                   "/deployments/" + self.config['CHATGPT']['MODELNAME'] +
                   "/chat/completions/?api-version=" +
                   self.config['CHATGPT']['APIVERSION'])
            headers = {
                'Content-Type': 'application/json',
                'api-key': self.config['CHATGPT']['ACCESS_TOKEN']
            }
            payload = {'messages': conversation}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            return data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logging.error("Request failed: %s", e)
            return f"Error: {e}"
        except Exception as e:
            logging.error("An error occurred: %s", e)
            return "An unexpected error occurred."

if __name__ == '__main__':
    ChatGPT_test = HKBU_ChatGPT()
    while True:
        user_input = input("Type anything to ChatGPT:\t")
        response = ChatGPT_test.submit(user_input)
        print(response)
