# Using the Content Core Library

> **Note:** As of vNEXT, the default extraction engine is `'auto'`. Content Core will automatically select the best extraction method based on your environment and available API keys, with a smart fallback order for both URLs and files. For files/documents, `'auto'` now tries Docling first, then falls back to simple extraction. You can override the engine if needed, but `'auto'` is recommended for most users.

This documentation explains how to configure and use the **Content Core** library in your projects. The library allows customization of AI model settings through a YAML file and environment variables.

## Environment Variable for Configuration

The library uses the `CCORE_MODEL_CONFIG_PATH` environment variable to locate the custom YAML configuration file. If this variable is not set or the specified file is not found, the library will fall back to internal default settings.

To set the environment variable, add the following line to your `.env` file or set it directly in your environment:

```
CCORE_MODEL_CONFIG_PATH=/path/to/your/models_config.yaml
```

## YAML File Schema

The YAML configuration file defines the AI models that the library will use. The structure of the file is as follows:

- **speech_to_text**: Configuration for the speech-to-text model.
  - **provider**: Model provider (example: `openai`).
  - **model_name**: Model name (example: `whisper-1`).
- **default_model**: Configuration for the default language model.
  - **provider**: Model provider.
  - **model_name**: Model name.
  - **config**: Additional parameters like `temperature`, `top_p`, `max_tokens`.
- **cleanup_model**: Configuration for the content cleanup model.
  - **provider**: Model provider.
  - **model_name**: Model name.
  - **config**: Additional parameters.
- **summary_model**: Configuration for the summary model.
  - **provider**: Model provider.
  - **model_name**: Model name.
  - **config**: Additional parameters.

### Default YAML File

Here is the content of the default YAML file used by the library:

```yaml
speech_to_text:
  provider: openai
  model_name: whisper-1

default_model:
  provider: openai
  model_name: gpt-4o-mini
  config:
    temperature: 0.5
    top_p: 1
    max_tokens: 2000

cleanup_model:
  provider: openai
  model_name: gpt-4o-mini
  config:
    temperature: 0
    max_tokens: 8000
    output_format: json

summary_model:
  provider: openai
  model_name: gpt-4o-mini
  config:
    temperature: 0
    top_p: 1
    max_tokens: 2000
```

## Customization

You can customize any aspect of the YAML file to suit your needs. Change the providers, model names, or configuration parameters as desired.

To simplify setup, we suggest copying the provided sample files:
- Copy `.env.sample` to `.env` and adjust the environment variables, including `CCORE_MODEL_CONFIG_PATH`.
- Copy `models_config.yaml.sample` to your desired location and modify it as needed.

This will allow you to quickly start with customized settings without needing to create the files from scratch.

### Extraction Engine Selection

By default, Content Core uses the `'auto'` engine for both document and URL extraction tasks. The logic is as follows:
- **For URLs** (`url_engine`): Uses Firecrawl if `FIRECRAWL_API_KEY` is set, else Jina if `JINA_API_KEY` is set, else falls back to BeautifulSoup.
- **For files** (`document_engine`): Tries Docling extraction first (for robust document parsing), then falls back to simple extraction if needed.

You can override this behavior by specifying separate engines for documents and URLs in your config or function call, but `'auto'` is recommended for most users.

#### Docling Engine

Content Core supports an optional Docling engine for advanced document parsing. To enable Docling explicitly:

##### In YAML config
Add under the `extraction` section:
```yaml
extraction:
  document_engine: docling  # auto (default), simple, or docling
  url_engine: auto          # auto (default), simple, firecrawl, or jina
  docling:
    output_format: html     # markdown | html | json
```

##### Programmatically in Python
```python
from content_core.config import set_document_engine, set_url_engine, set_docling_output_format

# toggle document engine to Docling
set_document_engine("docling")

# toggle URL engine to Firecrawl
set_url_engine("firecrawl")

# pick format
set_docling_output_format("json")
```

#### Per-Execution Overrides
You can override the extraction engines and Docling output format on a per-call basis by including `document_engine`, `url_engine` and `output_format` in your input:

```python
from content_core.content.extraction import extract_content

# override document engine and format for this document
result = await extract_content({
    "file_path": "document.pdf",
    "document_engine": "docling",
    "output_format": "html"
})
print(result.content)

# override URL engine for this URL
result = await extract_content({
    "url": "https://example.com",
    "url_engine": "firecrawl"
})
print(result.content)
```

Or using `ProcessSourceInput`:

```python
from content_core.common.state import ProcessSourceInput
from content_core.content.extraction import extract_content

input = ProcessSourceInput(
    file_path="document.pdf",
    document_engine="docling",
    output_format="json"
)
result = await extract_content(input)
print(result.content)
```

## Support

If you have questions or encounter issues while using the library, open an issue in the repository or contact the support team.
