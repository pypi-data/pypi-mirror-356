from json_repair import repair_json
import json
from typing import Dict, Optional
import re

class PostProcessor:

    def __init__(self, link_patterns: Optional[Dict[str, str]] = None) -> None:
        """Create a postprocessor with optional link recovery patterns.

        Args:
            link_patterns: Mapping of output field names to regex patterns. When
                provided, these patterns are used to populate missing URL fields
                from the cleaned content.
        """
        self.link_patterns = link_patterns or {
            "ftp_download": r"(ftp://[^\s)]+)",
            "movie_preview": r"(https?://[^\s)]+\.mov)",
            "thumbnail_image": r"(https?://[^\s)]+thumbnail[^\s)]*\.jpg)",
        }

    def process(
        self, response: str, preprocessed: Optional[str] = None
    ) -> dict:
        """Parse JSON from the LLM response and optionally fill missing URLs.

        Args:
            response: The raw text returned by the language model.
            preprocessed: The cleaned content that was provided to the model.

        Returns:
            A dictionary of the parsed JSON data. When ``preprocessed`` is
            supplied and ``link_patterns`` are set, missing URL fields are
            recovered by applying the regex patterns to the cleaned content.
        """
        json_response = {}
        try:
            # Extract the JSON from the generated text. Handle variations in
            # output format.
            json_string = response
            if "```json" in response:
                json_string = response.split("```json")[1].split("```", 1)[0]
            elif "{" in response and "}" in response:
                start_index = response.find("{")
                end_index = response.rfind("}") + 1
                json_string = response[start_index:end_index]

            json_response = json.loads(repair_json(json_string))
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            print(f"Generated text: {response}")
            json_response = {}

        if preprocessed:
            for field, pattern in self.link_patterns.items():
                if not json_response.get(field):
                    match = re.search(pattern, preprocessed)
                    if match:
                        json_response[field] = match.group(1)

        return json_response
