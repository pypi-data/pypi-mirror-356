import logging
import os
from abc import ABC, abstractmethod
import openai

# Placeholder for Claude SDK import
# from claude_sdk import ClaudeClient as ClaudeAPIClient

class LLMStrategy(ABC):
    @abstractmethod
    def process(self, md_file):
        pass

class SaveLocally(LLMStrategy):
    def process(self, md_file):
        logging.info(f"File saved locally: {md_file}")

class OpenAIClient(LLMStrategy):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")

        if not self.api_key:
            raise ValueError("Missing OpenAI API key. Please set it in the environment.")

        try:
            self.client = openai.OpenAI(api_key=self.api_key)
        except openai.OpenAIError as e:
            logging.error(f"Failed to initialize OpenAI client: {e}")
            raise ValueError("Invalid OpenAI API key.")

    def process(self, md_file):
        try:
            with open(md_file, "r", encoding="utf-8") as file:
                content = file.read()

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Process this Markdown content."},
                    {"role": "user", "content": content}
                ]
            )

            llm_response = response.choices[0].message.content
            logging.info(f"OpenAI Response for {md_file}: {llm_response}")

        except FileNotFoundError:
            logging.error(f"Markdown file not found: {md_file}")
        except openai.OpenAIError as e:
            logging.error(f"OpenAI API error while processing {md_file}: {e}")
        except Exception as e:
            logging.exception(f"Unexpected error processing {md_file}: {e}")

class ClaudeClient(LLMStrategy):
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        self.model = os.getenv("CLAUDE_MODEL", "claude-v1")

        if not self.api_key:
            raise ValueError("Missing Claude API key. Please set it in the environment.")

        # Initialize Claude client here (replace with actual SDK code)
        # self.client = ClaudeAPIClient(api_key=self.api_key)

    def process(self, md_file):
        try:
            with open(md_file, "r", encoding="utf-8") as file:
                content = file.read()

            # Replace with actual Claude API call
            # response = self.client.complete(prompt=content, model=self.model)

            # Dummy placeholder response
            response_text = f"Simulated Claude response for {md_file}"

            logging.info(f"Claude Response for {md_file}: {response_text}")

        except FileNotFoundError:
            logging.error(f"Markdown file not found: {md_file}")
        except Exception as e:
            logging.exception(f"Unexpected error processing {md_file}: {e}")

class GeminiClient(LLMStrategy):
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-pro")

        if not self.api_key:
            raise ValueError("Missing Gemini API key. Please set it in the environment.")

        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def process(self, md_file):
        try:
            import requests

            with open(md_file, "r", encoding="utf-8") as file:
                content = file.read()

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "contents": [
                    {"parts": [{"text": content}]}
                ]
            }

            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()

            reply = response.json()
            text = reply["candidates"][0]["content"]["parts"][0]["text"]
            logging.info(f"Gemini Response for {md_file}: {text}")

        except FileNotFoundError:
            logging.error(f"Markdown file not found: {md_file}")
        except Exception as e:
            logging.exception(f"Gemini processing error: {e}")
class MistralClient(LLMStrategy):
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = os.getenv("MISTRAL_MODEL", "mistral-medium")

        if not self.api_key:
            raise ValueError("Missing Mistral API key. Please set it in the environment.")

        self.api_url = "https://api.mistral.ai/v1/chat/completions"

    def process(self, md_file):
        try:
            import requests

            with open(md_file, "r", encoding="utf-8") as file:
                content = file.read()

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Process this Markdown content."},
                    {"role": "user", "content": content}
                ]
            }

            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            message = result["choices"][0]["message"]["content"]
            logging.info(f"Mistral Response for {md_file}: {message}")

        except FileNotFoundError:
            logging.error(f"Markdown file not found: {md_file}")
        except Exception as e:
            logging.exception(f"Mistral processing error: {e}")


class LLMFactory:
    @staticmethod
    def get_llm(client_name: str) -> LLMStrategy:
        client_name = client_name.lower()
        if client_name == "openai":
            return OpenAIClient()
        elif client_name == "claude":
            return ClaudeClient()
        elif client_name == "gemini":
            return GeminiClient()
        elif client_name == "mistral":
            return MistralClient()
        else:
            raise ValueError(f"Unknown LLM client: {client_name}")

