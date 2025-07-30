# AI Prompter: Professional Prompt Management Made Simple

**Stop hardcoding prompts. Start building maintainable, reusable AI prompt templates.**

AI Prompter is a powerful Python library that transforms how you manage AI prompts. Using familiar Jinja2 templating, you can create dynamic, reusable prompts that scale with your applications - whether you're building chatbots, content generators, or complex AI workflows.

## Why AI Prompter?

- **🎯 Template-Driven**: Write prompts once, reuse everywhere with dynamic variables
- **📁 Organized**: Keep prompts in separate files, organized and version-controlled  
- **🔧 Flexible**: Works with any LLM provider - OpenAI, Anthropic, local models
- **⚡ LangChain Ready**: Seamless integration with LangChain workflows
- **🏗️ Structured Output**: Built-in support for JSON, Pydantic models, and custom parsers
- **🎨 Modular**: Include and compose templates for complex prompt engineering

## Quick Start

### Installation

```bash
pip install ai-prompter

# For LangChain integration
pip install ai-prompter[langchain]
```

### 30-Second Example

```python
from ai_prompter import Prompter

# Create a simple prompt template
prompter = Prompter(template_text="""
You are a {{ role }} expert. Help the user with their {{ task_type }} question.

User Question: {{ question }}

Please provide a {{ tone }} and detailed response.
""")

# Use it with different scenarios
response = prompter.render({
    "role": "Python programming",
    "task_type": "debugging", 
    "question": "Why is my list comprehension not working?",
    "tone": "friendly"
})

print(response)
# Output: You are a Python programming expert. Help the user with their debugging question...
```

### File-Based Templates (Recommended)

Create a `prompts/` folder in your project and save templates as `.jinja` files:

```jinja
<!-- prompts/code_review.jinja -->
You are an experienced {{ language }} developer conducting a code review.

Code to review:
```{{ language }}
{{ code }}
```

Focus on:
{% for focus_area in focus_areas %}
- {{ focus_area }}
{% endfor %}

Provide specific, actionable feedback with examples.
```

```python
from ai_prompter import Prompter

# Load the template by name (finds prompts/code_review.jinja automatically)
reviewer = Prompter(prompt_template="code_review")

prompt = reviewer.render({
    "language": "python",
    "code": "def calculate(x, y): return x + y",
    "focus_areas": ["error handling", "documentation", "performance"]
})
```

## Features

- Define prompts as Jinja templates.
- Load default templates from `src/ai_prompter/prompts`.
- Override templates via `PROMPTS_PATH` environment variable.
- Automatic project root detection for prompt templates.
- Render prompts with arbitrary data or Pydantic models.
- Export to LangChain `ChatPromptTemplate`.
- Automatic output parser integration for structured outputs.

## Installation & Setup

### Basic Installation

```bash
# Install from PyPI
pip install ai-prompter

# Or using uv (recommended for Python projects)
uv add ai-prompter
```

### With LangChain Integration

```bash
pip install ai-prompter[langchain]
# or
uv add ai-prompter[langchain]
```

### Development Installation

```bash
git clone https://github.com/lfnovo/ai-prompter
cd ai-prompter
uv sync  # installs with all dev dependencies
```

## Configuration

Configure a custom template path by creating a `.env` file in the project root:

```dotenv
PROMPTS_PATH=path/to/custom/templates
```

## Usage

### Basic Usage

```python
from ai_prompter import Prompter

# Initialize with a template name
prompter = Prompter('my_template')

# Render a prompt with variables
prompt = prompter.render({'variable': 'value'})
print(prompt)
```

### Custom Prompt Directory

You can specify a custom directory for your prompt templates using the `prompt_dir` parameter:

```python
prompter = Prompter(template_text='Hello {{ name }}!', prompt_dir='/path/to/your/prompts')
```

### Using Environment Variable for Prompt Path

Set the `PROMPTS_PATH` environment variable to point to your custom prompts directory:

```bash
export PROMPTS_PATH=/path/to/your/prompts
```

You can specify multiple directories separated by `:` (colon):

```bash
export PROMPTS_PATH=/path/to/templates1:/path/to/templates2
```

### Template Search Order

The `Prompter` class searches for templates in the following locations (in order of priority):

1. **Custom directory** - If you provide `prompt_dir` parameter when initializing Prompter
2. **Environment variable paths** - Directories specified in `PROMPTS_PATH` (colon-separated)
3. **Current directory prompts** - `./prompts` subfolder in your current working directory
4. **Project root prompts** - Automatically detects your Python project root (by looking for `pyproject.toml`, `setup.py`, `setup.cfg`, or `.git`) and checks for a `prompts` folder there
5. **Home directory** - `~/ai-prompter` folder
6. **Package defaults** - Built-in templates at `src/ai_prompter/prompts`

This allows you to organize your project with prompts at the root level, regardless of your package structure:
```
my-project/
├── prompts/           # <- Templates here will be found automatically
│   └── my_template.jinja
├── src/
│   └── my_package/
│       └── main.py
└── pyproject.toml
```

### Using File-based Templates

You can store your templates in files and reference them by name. The library will search through all configured paths (see Template Search Order above) until a matching template is found.

**Template naming**: You can reference templates either with or without the `.jinja` extension:
- `prompt_template="greet"` → searches for `greet.jinja`
- `prompt_template="greet.jinja"` → also searches for `greet.jinja`

Both approaches work identically, so use whichever feels more natural for your workflow.

```python
from ai_prompter import Prompter

# Will search for 'greet.jinja' in all configured paths
prompter = Prompter(prompt_template="greet")
result = prompter.render({"name": "World"})
print(result)  # Output depends on the content of greet.jinja
```

You can also specify multiple search paths via environment variable:

```python
import os
from ai_prompter import Prompter

# Set multiple search paths
os.environ["PROMPTS_PATH"] = "/path/to/templates1:/path/to/templates2"

prompter = Prompter(prompt_template="greet")
result = prompter.render({"name": "World"})
print(result)  # Uses greet.jinja from the first path where it's found
```

### Raw text template

```python
from ai_prompter import Prompter

template = """Write an article about {{ topic }}."""
prompter = Prompter(template_text=template)
prompt = prompter.render({"topic": "AI"})
print(prompt)  # Write an article about AI.
```

### Using Raw Text Templates

Alternatively, you can provide the template content directly as raw text using the `template_text` parameter or the `from_text` class method.

```python
from ai_prompter import Prompter

# Using template_text parameter
prompter = Prompter(template_text="Hello, {{ name }}!")
result = prompter.render({"name": "World"})
print(result)  # Output: Hello, World!

# Using from_text class method
prompter = Prompter.from_text("Hi, {{ person }}!", model="gpt-4")
result = prompter.render({"person": "Alice"})
print(result)  # Output: Hi, Alice!
```

### LangChain Integration

You can convert your prompts to LangChain's `ChatPromptTemplate` format for use in LangChain workflows. This works for both text-based and file-based templates.

```python
from ai_prompter import Prompter

# With text-based template
text_prompter = Prompter(template_text="Hello, {{ name }}!")
lc_text_prompt = text_prompter.to_langchain()

# With file-based template
file_prompter = Prompter(prompt_template="greet")
lc_file_prompt = file_prompter.to_langchain()
```

**Note**: LangChain integration requires the `langchain-core` package. Install it with `pip install .[langchain]`.

### Using Output Parsers

The Prompter class supports LangChain output parsers to automatically inject formatting instructions into your prompts. When you provide a parser, it will call the parser's `get_format_instructions()` method and make the result available as `{{ format_instructions }}` in your template.

```python
from ai_prompter import Prompter
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Define your output model
class Article(BaseModel):
    title: str = Field(description="Article title")
    summary: str = Field(description="Brief summary")
    tags: list[str] = Field(description="Relevant tags")

# Create a parser
parser = PydanticOutputParser(pydantic_object=Article)

# Create a prompter with the parser
prompter = Prompter(
    template_text="""Write an article about {{ topic }}.

{{ format_instructions }}""",
    parser=parser
)

# Render the prompt - format instructions are automatically included
prompt = prompter.render({"topic": "AI Safety"})
print(prompt)
# Output will include the topic AND the parser's format instructions
```

This works with file-based templates too:

```jinja
# article_structured.jinja
Write an article about {{ topic }}.

Please format your response according to these instructions:
{{ format_instructions }}
```

```python
prompter = Prompter(
    prompt_template="article_structured",
    parser=parser
)
```

The parser integration supports any LangChain output parser that implements `get_format_instructions()`, including:
- `PydanticOutputParser` - For structured Pydantic model outputs
- `OutputFixingParser` - For fixing malformed outputs
- `RetryOutputParser` - For retrying failed parsing attempts
- `StructuredOutputParser` - For dictionary-based structured outputs

## Real-World Examples

### Content Generation Pipeline

```python
# prompts/blog_post.jinja
You are a professional content writer specializing in {{ niche }}.

Write a {{ post_type }} blog post about "{{ title }}" for {{ target_audience }}.

Requirements:
- Length: {{ word_count }} words
- Tone: {{ tone }}
- Include {{ num_sections }} main sections
{% if seo_keywords -%}
- SEO Keywords to include: {{ seo_keywords|join(', ') }}
{% endif %}
{% if call_to_action -%}
- End with this call-to-action: {{ call_to_action }}
{% endif %}

{{ format_instructions }}
```

```python
from ai_prompter import Prompter
from pydantic import BaseModel, Field

class BlogPost(BaseModel):
    title: str = Field(description="SEO-optimized title")
    sections: list[dict] = Field(description="List of sections with headers and content")
    meta_description: str = Field(description="SEO meta description")
    tags: list[str] = Field(description="Relevant tags")

# Create content generator
blog_generator = Prompter(
    prompt_template="blog_post",
    parser=PydanticOutputParser(pydantic_object=BlogPost)
)

# Generate different types of content
tech_post = blog_generator.render({
    "niche": "technology",
    "title": "Getting Started with AI Prompt Engineering", 
    "target_audience": "software developers",
    "post_type": "how-to guide",
    "word_count": 1500,
    "tone": "technical but accessible",
    "num_sections": 5,
    "seo_keywords": ["AI prompts", "prompt engineering", "LLM"],
    "call_to_action": "Try AI Prompter in your next project!"
})
```

### Multi-Language Support

```python
# prompts/customer_support.jinja
{% set greetings = {
    'en': 'Hello',
    'es': 'Hola', 
    'fr': 'Bonjour',
    'de': 'Hallo'
} %}

{{ greetings[language] }}! I'm here to help you with {{ issue_type }}.

Customer Issue: {{ customer_message }}

{% if language != 'en' -%}
Please respond in {{ language }}.
{% endif %}

Provide a {{ tone }} response that:
1. Acknowledges the customer's concern
2. Offers a specific solution or next steps
3. Includes relevant {{ company_name }} policies if applicable
```

```python
support_agent = Prompter(prompt_template="customer_support")

# Handle support tickets in different languages
spanish_response = support_agent.render({
    "language": "es",
    "issue_type": "billing inquiry",
    "customer_message": "No puedo encontrar mi factura",
    "tone": "empathetic and professional",
    "company_name": "TechCorp"
})
```

### Dynamic Email Campaigns

```python
# prompts/email_campaign.jinja
Subject: {% if user.is_premium %}Exclusive{% else %}Special{% endif %} {{ campaign_type }} - {{ subject_line }}

Hi {{ user.first_name|default('there') }},

{% if user.last_purchase_days_ago < 30 -%}
Thanks for your recent purchase of {{ user.last_product }}! 
{% elif user.last_purchase_days_ago > 90 -%}
We miss you! It's been a while since your last order.
{% endif %}

{{ main_message }}

{% if user.is_premium -%}
As a premium member, you get:
{% for benefit in premium_benefits -%}
✓ {{ benefit }}
{% endfor %}
{% else -%}
{% if upgrade_offer -%}
Upgrade to premium and save {{ upgrade_discount }}%!
{% endif %}
{% endif %}

{{ call_to_action }}

Best regards,
{{ sender_name }}
```

```python
email_generator = Prompter(prompt_template="email_campaign")

# Personalized emails based on user data
campaign_email = email_generator.render({
    "user": {
        "first_name": "Sarah",
        "is_premium": False,
        "last_purchase_days_ago": 45,
        "last_product": "Python Course"
    },
    "campaign_type": "Sale",
    "subject_line": "50% Off All Programming Courses",
    "main_message": "Master new skills with our comprehensive programming courses.",
    "upgrade_offer": True,
    "upgrade_discount": 25,
    "premium_benefits": ["Early access to new courses", "1-on-1 mentoring", "Certificate priority"],
    "call_to_action": "Shop Now →",
    "sender_name": "The Learning Team"
})
```

### API Documentation Generator

```python
# prompts/api_docs.jinja
# {{ endpoint.method }} {{ endpoint.path }}

{{ endpoint.description }}

## Request

{% if endpoint.parameters -%}
### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
{% for param in endpoint.parameters -%}
| `{{ param.name }}` | {{ param.type }} | {{ "Yes" if param.required else "No" }} | {{ param.description }} |
{% endfor %}
{% endif %}

{% if endpoint.body_schema -%}
### Request Body

```json
{{ endpoint.body_schema|tojson(indent=2) }}
```
{% endif %}

## Response

```json
{{ endpoint.response_example|tojson(indent=2) }}
```

{% if endpoint.error_codes -%}
## Error Codes

{% for error in endpoint.error_codes -%}
- **{{ error.code }}**: {{ error.description }}
{% endfor %}
{% endif %}

## Example

```bash
curl -X {{ endpoint.method }} "{{ base_url }}{{ endpoint.path }}" \
{% for header in endpoint.headers -%}
  -H "{{ header.name }}: {{ header.value }}" \
{% endfor %}
{% if endpoint.body_example -%}
  -d '{{ endpoint.body_example|tojson }}'
{% endif %}
```
```

```python
docs_generator = Prompter(prompt_template="api_docs")

endpoint_doc = docs_generator.render({
    "base_url": "https://api.example.com",
    "endpoint": {
        "method": "POST",
        "path": "/users",
        "description": "Create a new user account",
        "parameters": [
            {"name": "api_key", "type": "string", "required": True, "description": "Your API key"}
        ],
        "body_schema": {"name": "string", "email": "string", "role": "string"},
        "body_example": {"name": "John Doe", "email": "john@example.com", "role": "user"},
        "response_example": {"id": 123, "name": "John Doe", "created_at": "2024-01-01T00:00:00Z"},
        "error_codes": [
            {"code": 400, "description": "Invalid request data"},
            {"code": 409, "description": "Email already exists"}
        ],
        "headers": [{"name": "Authorization", "value": "Bearer YOUR_API_KEY"}]
    }
})
```

## Best Practices

### 1. Organize Templates by Use Case

```
prompts/
├── content/
│   ├── blog_post.jinja
│   ├── social_media.jinja
│   └── email_newsletter.jinja
├── analysis/
│   ├── code_review.jinja
│   ├── data_analysis.jinja
│   └── competitor_research.jinja
└── support/
    ├── customer_support.jinja
    └── technical_troubleshooting.jinja
```

### 2. Use Descriptive Variable Names

```python
# Good ✅
prompter.render({
    "user_expertise_level": "beginner",
    "preferred_learning_style": "visual",
    "target_completion_time": "2 weeks"
})

# Avoid ❌
prompter.render({
    "level": "beginner", 
    "style": "visual",
    "time": "2 weeks"
})
```

### 3. Include Validation and Defaults

```jinja
<!-- prompts/content_generator.jinja -->
{% if not topic -%}
{{ raise_error("topic is required") }}
{% endif %}

Generate content about {{ topic }} for {{ audience|default("general audience") }}.

Word count: {{ word_count|default(500) }}
Tone: {{ tone|default("professional") }}
```

### 4. Leverage Jinja2 Features

```jinja
<!-- Use filters for formatting -->
Today's date: {{ current_time|strftime("%B %d, %Y") }}
Uppercase title: {{ title|upper }}
Comma-separated tags: {{ tags|join(", ") }}

<!-- Use conditionals for dynamic content -->
{% if user.subscription_type == "premium" %}
You have access to premium features!
{% else %}
Upgrade to premium for advanced features.
{% endif %}

<!-- Use loops for repetitive content -->
{% for step in instructions %}
{{ loop.index }}. {{ step }}
{% endfor %}
```

### 5. Version Control Your Prompts

```bash
# Track prompt changes with git
git add prompts/
git commit -m "feat: add support for multi-language customer service prompts"

# Use branches for prompt experiments  
git checkout -b experiment/new-tone-testing
```

### 6. Test Templates with Sample Data

```python
# Create test data for your templates
test_data = {
    "user": {"name": "Test User", "level": "beginner"},
    "product": {"name": "AI Course", "price": 99.99},
    "current_time": "2024-01-15 10:30:00"
}

# Test all your templates
for template_name in ["welcome", "product_recommendation", "follow_up"]:
    prompter = Prompter(prompt_template=template_name)
    result = prompter.render(test_data)
    print(f"Template: {template_name}")
    print(f"Length: {len(result)} characters")
    print("---")
```

## Advanced Features

### Including Other Templates

You can include other template files within a template using Jinja2's `{% include %}` directive. This allows you to build modular templates.

```jinja
# outer.jinja
This is the outer file

{% include 'inner.jinja' %}

This is the end of the outer file
```

```jinja
# inner.jinja
This is the inner file

{% if type == 'a' %}
    You selected A
{% else %}
    You didn't select A
{% endif %}
```

```python
from ai_prompter import Prompter

prompter = Prompter(prompt_template="outer")
prompt = prompter.render(dict(type="a"))
print(prompt)
# This is the outer file
# 
# This is the inner file
# 
#     You selected A
# 
# 
# This is the end of the outer file
```

### Using Variables

Templates can use variables that you pass in through the `render()` method. You can use Jinja2 filters and conditionals to control the output based on your data.

```python
from ai_prompter import Prompter

prompter = Prompter(template_text="Hello {{name|default('Guest')}}!")
prompt = prompter.render()  # No data provided, uses default
print(prompt)  # Hello Guest!
prompt = prompter.render({"name": "Alice"})  # Data provided
print(prompt)  # Hello Alice!
```

The library also automatically provides a `current_time` variable with the current timestamp in format "YYYY-MM-DD HH:MM:SS".

```python
from ai_prompter import Prompter

prompter = Prompter(template_text="Current time: {{current_time}}")
prompt = prompter.render()
print(prompt)  # Current time: 2025-04-19 23:28:00
```

### File-based template

Place a Jinja file (e.g., `article.jinja`) in the default prompts directory (`src/ai_prompter/prompts`) or your custom path:

```jinja
Write an article about {{ topic }}.
```

```python
from ai_prompter import Prompter

prompter = Prompter(prompt_template="article")
prompt = prompter.render({"topic": "AI"})
print(prompt)
```

## Troubleshooting

### Common Issues

**Template Not Found Error**
```python
# Check where AI Prompter is looking for templates
prompter = Prompter(prompt_template="my_template")
print("Template locations searched:")
for folder in prompter.prompt_folders:
    print(f"  - {folder}")

# Verify template location
location = prompter.template_location("my_template") 
print(f"Template location: {location}")
```

**Jinja2 Syntax Errors**
```python
# Test templates in isolation
from jinja2 import Template

template_content = "Hello {{ name }}!"
template = Template(template_content)
result = template.render(name="World")  # Test basic rendering
```

**Environment Variable Issues**
```bash
# Check current PROMPTS_PATH
echo $PROMPTS_PATH

# Set for current session
export PROMPTS_PATH="/path/to/templates"

# Set permanently in ~/.bashrc or ~/.zshrc  
echo 'export PROMPTS_PATH="/path/to/templates"' >> ~/.bashrc
```

### Performance Tips

- **Cache Prompter instances** for frequently used templates
- **Use file-based templates** for better performance with includes
- **Keep template files small** and modular
- **Minimize variable processing** in templates when possible

```python
# Good: Reuse prompter instances
email_prompter = Prompter(prompt_template="email_template")
for user in users:
    email = email_prompter.render({"user": user})
    send_email(email)

# Avoid: Creating new instances repeatedly  
for user in users:  # Less efficient
    prompter = Prompter(prompt_template="email_template")
    email = prompter.render({"user": user})
```

## Interactive Examples

Explore AI Prompter features interactively:

```bash
# Clone the repository
git clone https://github.com/lfnovo/ai-prompter
cd ai-prompter

# Install with dev dependencies
uv sync

# Launch Jupyter notebook
uv run jupyter lab notebooks/prompter_usage.ipynb
```

## Testing & Development

```bash
# Run all tests
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=ai_prompter

# Run specific test file
uv run pytest tests/test_prompter.py -v

# Format code
uv run black src/
uv run isort src/
```

## Community & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/lfnovo/ai-prompter/issues)
- **Discussions**: [Ask questions and share templates](https://github.com/lfnovo/ai-prompter/discussions)  
- **Examples**: [Community template gallery](https://github.com/lfnovo/ai-prompter/wiki/Template-Gallery)

## Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Add tests** for new functionality
4. **Ensure tests pass**: `uv run pytest`
5. **Submit a Pull Request**

### Contributing Templates

Share your templates with the community:

1. Add your template to `examples/community-templates/`
2. Include documentation and example usage
3. Submit a PR with the `template-contribution` label

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to transform your prompt management?** 

```bash
pip install ai-prompter
```

Start building better AI applications with organized, maintainable prompts today!