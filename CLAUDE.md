# Running the Scraper

## Virtual Environment
```bash
./venv/bin/python3 example_usage.py
```

## Linting/Typecheck
```bash
./venv/bin/python3 -m flake8 scraper.py --max-line-length=100
```

## Tests
No automated tests currently. Run examples for validation.

## Key Functions

### 1. `scrape_transfer_articulation(from_school, to_school, debug=False)`
- **Fast**: ~1-2 seconds
- **Returns**: Agreement metadata (institution name, code, supported years)
- **Reliable**: 100% - Uses REST API only

### 2. `get_degree_information(from_school, to_school, include_course_url=True, debug=False)`
- **Fast**: ~1-2 seconds
- **Returns**: Agreement + pre-filled course URL for assist.org
- **Recommended**: Best option for hackathon - provides all needed info with fast performance
- **Course URL Format**: `https://www.assist.org/?from={from_id}&to={to_id}&year={year_id}`

## Recommended Usage Strategy

**DO NOT use** `scrape_course_articulation()` - it requires Playwright and is unreliable due to assist.org's SPA architecture.

**DO use** `get_degree_information()` - fast, reliable, and returns clean agreement data + link to assist.org.

## Example
```python
from scraper import get_degree_information

result = get_degree_information(
    "Berkeley City College",
    "University of California, Berkeley"
)

if not result.get('error'):
    agreement = result['agreement']
    print(f"From: {agreement['from_school']}")
    print(f"To: {agreement['to_school']}")
    print(f"Pathway: {agreement['institution_name']}")
    print(f"Years: {agreement['years_supported']}")
    print(f"View: {result['assist_url']}")
```

Returns:
- `from_school`, `to_school`: The transfer pair
- `institution_name`, `institution_code`: Pathway (e.g., "Vista Community College")
- `years_supported`: Number of years the agreement covers
- `is_community_college`: Boolean
- `assist_url`: Link to assist.org for users to view course details
