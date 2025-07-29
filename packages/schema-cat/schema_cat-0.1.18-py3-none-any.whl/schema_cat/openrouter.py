import logging
import os
from xml.etree import ElementTree

import httpx

from schema_cat.prompt import build_system_prompt
from schema_cat.retry import with_retry
from schema_cat.xml import xml_from_string, XMLParsingError

logger = logging.getLogger("schema_cat")


@with_retry()
async def call_openrouter(model: str,
                          sys_prompt: str,
                          user_prompt: str,
                          xml_schema: str,
                          max_tokens: int = 8192,
                          temperature: float = 0.0,
                          max_retries: int = 5,
                          initial_delay: float = 1.0,
                          max_delay: float = 60.0) -> ElementTree.XML:
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    system_prompt = build_system_prompt(sys_prompt, xml_schema)
    data = {
        "model": model,
        "messages": [
            {"role": "system",
             "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", "https://www.thefamouscat.com"),
        "X-Title": os.getenv("OPENROUTER_X_TITLE", "SchemaCat"),
        "Content-Type": "application/json"
    }

    logger.info(f"Calling OpenRouter API with model {model}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()

    logger.info("Successfully received response from OpenRouter")
    logger.debug(f"Raw response content: {content}")

    # Parse the response content as XML
    try:
        root = xml_from_string(content)
        logger.debug("Successfully parsed response as XML")
        return root
    except XMLParsingError as e:
        if max_retries > 0:
            from schema_cat import Provider
            from schema_cat.model_providers import get_model_name_by_common_name_and_provider
            return await call_openrouter(user_prompt=content,
                                         sys_prompt="Convert this data into valid XML according to the schema",
                                         xml_schema=xml_schema,
                                         model=get_model_name_by_common_name_and_provider("claude-haiku",
                                                                                          Provider.OPENROUTER),
                                         max_retries=0
                                         )
        else:
            raise e
