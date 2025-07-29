# Relevance Connect

Open connector to add integrations to Relevance AI.

## Getting Started

### Prerequisites

Install the Relevance Connect CLI:

```bash
pip install relevance_connect
```

For local development, you can install the package from the source:
```bash
pip install -e .
```

Login to your Relevance AI account: [Walkthrough](https://app.supademo.com/demo/cmc1fdg1gjf3dsn1rjt31ki1r):
```bash
relevance-connect login
```


## Creating a New Integration

Checkout the [example](example) for a complete example.

Follow these steps to create and submit a new integration:

### 1. Set Up Your Integration Folder

Create a new folder for your integration and navigate to it.

### 2. Create the Metadata File

Create a `metadata.json` file that defines your integration's configuration:

```json
{
    "name": "Firecrawl",
    "description": "Firecrawl is a tool that allows you to run firecrawl.",
    "inputs": [
        {
            "input_name": "website_url",
            "type": "string",
            "title": "Website URL",
            "description": "The URL of the website to crawl.",
            "default": "https://www.firecrawl.dev"
        },
        {
            "input_name": "firecrawl",
            "type": "string",
            "title": "Firecrawl API Key",
            "description": "The API key for firecrawl.",
            "metadata": {
                "content_type": "api_key",
                "is_fixed_param": true
            }
        }
    ],
    "required": ["website_url", "firecrawl"],
    "requirements": ["firecrawl"],
    "icon": "https://firecrawl.dev/favicon.ico",
    "long_output_mode": true,
    "timeout": 300
}
```

#### Metadata Fields

- **name**: Name of the integration
- **description**: Description of what the integration does
- **inputs**: Array of input configurations for the integration
- **required**: Array of required input field names
- **requirements**: *(Optional)* Python packages required by the integration
- **icon**: *(Optional)* URL to an icon for the integration
- **long_output_mode**: *(Optional)* Set to `true` if your code returns output greater than 10 million characters
- **timeout**: *(Optional)* Timeout in seconds (default: 300)

📖 **For detailed information about all available input types and their schemas, see [INPUTS.md](INPUTS.md).**

### 3. Create the Main Script

Create a `main.py` file containing your integration logic:

```python
from firecrawl import FirecrawlApp

# Initialize the FirecrawlApp with API key from secrets
app = FirecrawlApp(api_key="{{secrets.chains_firecrawl}}")

# Use the website URL from the params
scrape_status = app.scrape_url(params['website_url'])

# Return the scraped content
return scrape_status.markdown
```

#### Important Notes

- **Single file only**: The entire integration must be in one `main.py` file
- **Return statement required**: Your script must end with a `return` statement
- **Access inputs**: Use the `params` dictionary to access inputs (e.g., `params["website_url"]`)
- **API keys**: Reference API key inputs using the pattern `{{secrets.chains_XXX}}` where `XXX` is the input name

### 4. Test Your Integration

#### Create Test Inputs

Create an `inputs.json` file with test data:

```json
{
    "website_url": "https://www.example.com",
    "firecrawl": "your-test-api-key"
}
```

#### Run the Test

Execute your integration locally:

```bash
relevance-connect run
```

#### [Optional] Save the Integration

If you want to save the integration to your Relevance AI account, you can do so with the following command:

```bash
relevance-connect save
```

### 5. Submit Your Integration

Once your integration is working correctly, submit it to Relevance AI!


## Other Commands

### Logout

```bash
relevance-connect logout
```

### Run javascript integration
Javascript is also supported. For javascript, packages are not supported. Checkout the [js_example](js_example) for an example.

```bash
relevance-connect run-js
```
