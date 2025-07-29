import argparse
import json
import os
import sys
from typing import Any, Dict, Optional
import dotenv

# Import shared pipeline modules
from .preprocessor import BasicPreprocessor
from .ai_extractor import AIExtractor, OllamaLLMClient
from .postprocessor import PostProcessor

# Default patterns used by PostProcessor to recover missing URLs
DEFAULT_LINK_PATTERNS = {
    "ftp_download": r"(ftp://[^\s)]+)",
    "movie_preview": r"(https?://[^\s)]+\.mov)",
    "thumbnail_image": r"(https?://[^\s)]+thumbnail[^\s)]*\.jpg)",
}
from .pipeline import Pipeline
from .crawler import crawl_urls

from pydantic import BaseModel, Field, create_model


def parse_schema_input(schema_input: str) -> BaseModel:
    """Parse a schema definition string into a ``BaseModel`` subclass.

    The input may be one of the following formats:
        * JSON Schema definition
        * A Python ``BaseModel`` class declaration
        * A list of ``name: type`` lines

    Args:
        schema_input: Text describing the desired schema.

    Returns:
        A dynamically created ``BaseModel`` representing the schema.
    """
    schema_input = schema_input.strip()
    # Detect the schema format and convert it into a BaseModel
    if not schema_input:
        return create_model(
            "DefaultSchema",
            title=(Optional[str], Field(default=None, description="Title of the content")),
            content=(Optional[str], Field(default=None, description="Main content")),
        )

    if schema_input.startswith("{"):
        schema_dict = json.loads(schema_input)
        return json_schema_to_basemodel(schema_dict)

    if "class " in schema_input and "BaseModel" in schema_input:
        return python_class_to_basemodel(schema_input)

    return simple_fields_to_basemodel(schema_input)


def json_schema_to_basemodel(schema_dict: Dict[str, Any]) -> BaseModel:
    """Convert a JSON Schema dictionary to a dynamic ``BaseModel``."""
    fields = {}
    properties = schema_dict.get("properties", {})
    for field_name, field_info in properties.items():
        field_type = get_python_type(field_info.get("type", "string"))
        field_description = field_info.get("description", "")
        fields[field_name] = (
            Optional[field_type],
            Field(default=None, description=field_description),
        )

    return create_model("DynamicSchema", **fields)


def python_class_to_basemodel(class_definition: str) -> BaseModel:
    """Execute a class definition and return it as a ``BaseModel`` instance."""
    namespace = {"BaseModel": BaseModel, "Field": Field, "str": str, "int": int,
                "float": float, "bool": bool, "list": list, "dict": dict}
    exec(class_definition, namespace)
    for name, obj in namespace.items():
        if isinstance(obj, type) and issubclass(obj, BaseModel) and obj is not BaseModel:
            fields = {}
            for field_name, field in obj.model_fields.items():
                fields[field_name] = (
                    Optional[field.annotation],
                    Field(default=None, description=field.description or ""),
                )
            return create_model(f"{obj.__name__}Dynamic", **fields)
    raise ValueError("No BaseModel class found in definition")


def simple_fields_to_basemodel(fields_text: str) -> BaseModel:
    """Parse ``name: type`` pairs into a ``BaseModel``."""
    fields = {}
    for line in fields_text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            parts = line.split(":", 1)
            field_name = parts[0].strip()
            type_and_desc = parts[1].strip()
            if "=" in type_and_desc:
                type_part, desc_part = type_and_desc.split("=", 1)
                field_type = get_python_type(type_part.strip())
                description = desc_part.strip().strip('"\'')
            else:
                field_type = get_python_type(type_and_desc.strip())
                description = ""
            fields[field_name] = (Optional[field_type], Field(default=None, description=description))
        else:
            field_name = line.strip()
            fields[field_name] = (Optional[str], Field(default=None, description=""))

    if not fields:
        raise ValueError("No valid fields found in schema definition")
    return create_model("DynamicSchema", **fields)


def get_python_type(type_str: str):
    """Return the Python type object for a simple string alias."""
    type_str = type_str.lower().strip()
    mapping = {
        "string": str,
        "str": str,
        "integer": int,
        "int": int,
        "number": float,
        "float": float,
        "boolean": bool,
        "bool": bool,
        "array": list,
        "list": list,
        "object": dict,
        "dict": dict,
    }
    return mapping.get(type_str, str)


def run_pipeline(
    content: str,
    is_url: bool,
    schema_text: str,
    model_name: str,
    *,
    debug: bool = False,
) -> Dict[str, Any]:
    """Run the entire extraction pipeline for a single piece of content."""
    # Parse the schema text into a Pydantic model
    schema_model = parse_schema_input(schema_text)
    # Template used to construct the LLM prompt
    prompt_template = (
        "Extract structured data from the cleaned web content below using the provided schema.\n\n"
        "Content to analyze:\n{content}\n\nSchema requirements:\n{schema}\n\n"
        "Guidelines:\n"
        "- Use only the information present in the content. Do not guess values.\n"
        "- Resolve any relative URLs against the 'Source URL' prefix if one is given.\n"
        "- Output a single JSON object matching the schema exactly. Use null when information is missing."
    )

    # Create pipeline components
    preprocessor = BasicPreprocessor(config={"keep_tags": False})
    llm = OllamaLLMClient(
        config={
        "host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        "model_name": os.getenv("OLLAMA_MODEL", model_name),
        }
    )
    ai_extractor = AIExtractor(llm_client=llm, prompt_template=prompt_template)
    postprocessor = PostProcessor(link_patterns=DEFAULT_LINK_PATTERNS)
    pipeline = Pipeline(preprocessor, ai_extractor, postprocessor, debug=debug)
    # Execute the pipeline
    result = pipeline.run(content, is_url, schema_model)

    if is_url and "url" in schema_model.model_fields:
        result["url"] = content

    for field_name in schema_model.model_fields:
        result.setdefault(field_name, None)

    # Validate the resulting JSON against the provided schema
    try:
        validated = schema_model(**result)
        return validated.model_dump()
    except Exception as exc:  # Catch validation errors
        print(f"Schema validation error: {exc}", file=sys.stderr)
        return result


def crawl_and_extract(
    start_url: str,
    schema_text: str,
    model_name: str,
    max_pages: int,
    *,
    debug: bool = False,
) -> Dict[str, Any]:
    """Crawl ``start_url`` and run the extraction pipeline on each page."""
    # Find all pages starting from ``start_url``
    urls = crawl_urls(start_url, max_pages)
    print("URLs found:", file=sys.stderr)
    for url in urls:
        print(url, file=sys.stderr)
    results: Dict[str, Any] = {}
    # Run the pipeline on each discovered URL
    for url in urls:
        results[url] = run_pipeline(
            url,
            True,
            schema_text,
            model_name,
            debug=debug,
        )
    return results


def main() -> None:
    """Entry point for the ``web2json`` command line interface."""
    parser = argparse.ArgumentParser(description="Convert web content to JSON")
    parser.add_argument("content", help="URL or raw text to process")
    parser.add_argument("--url", action="store_true", help="Treat content as a URL")
    parser.add_argument("--crawl", action="store_true", help="Crawl starting from the given URL")
    parser.add_argument("--max_pages", type=int, default=10, help="Maximum pages to crawl")
    parser.add_argument("--schema", default="config/default.json", help="Schema text or path to file")
    parser.add_argument("--model_name", default="gemma3:12b", help="Name of the Ollama model to use.")
    parser.add_argument(
        "--output",
        help="Save the resulting JSON to a file instead of only printing",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print intermediate preprocessing and extraction information to stderr",
    )
    args = parser.parse_args()

    dotenv.load_dotenv()

    schema_text = args.schema
    if os.path.isfile(schema_text):
        with open(schema_text, "r", encoding="utf-8") as fh:
            schema_text = fh.read()

    if args.crawl:
        results = crawl_and_extract(
            args.content,
            schema_text,
            args.model_name,
            args.max_pages,
            debug=args.debug,
        )
        output_json = json.dumps(results, indent=2, ensure_ascii=False)
        print(output_json)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(output_json)

    else:
        result = run_pipeline(
            args.content,
            args.url,
            schema_text,
            args.model_name,
            debug=args.debug,
        )
        if not result or "error" in result:  # Check for empty result or error key
            print("Error: Failed to process content.", file=sys.stderr)
            sys.exit(1)
        output_json = json.dumps(result, indent=2, ensure_ascii=False)
        print(output_json)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(output_json)


if __name__ == "__main__":
    main()
