# API Test CLI

A command-line tool for testing HTTP APIs. Send requests, save them, create templates, search response content, and optionally analyze response sentiment.

## Installation

```bash
pip install apitest-cli
```

## Usage

Run `apitest --help` for a list of commands. Below are examples:

### Send a GET Request
```bash
apitest get https://jsonplaceholder.typicode.com/posts
```

### Search in Response
```bash
apitest get https://jsonplaceholder.typicode.com/posts --search "title"
```

### Analyze Sentiment
```bash
apitest get https://jsonplaceholder.typicode.com/posts --analyze
```

### Send a POST Request
```bash
apitest post https://jsonplaceholder.typicode.com/posts --data '{"title": "Hello", "body": "Test"}' --header "Content-Type: application/json"
```

### Save a Request
```bash
apitest save myrequest
```

### Replay a Saved Request
```bash
apitest replay myrequest
```

### Create a Template
```bash
apitest template mytemplate --url https://jsonplaceholder.typicode.com/posts --method GET --header "Content-Type: application/json"
```

### Use a Template
```bash
apitest use-template mytemplate
```

## Features
- Send GET/POST requests with custom headers and JSON data.
- Save and replay requests.
- Create and use request templates.
- Search keywords in responses with highlighted results.
- Optional sentiment analysis of response text (English only).
- Responses saved as JSON files in `responses/` directory.

## Requirements
- Python 3.8+
- Install dependencies: `pip install click requests rich textblob`
- Download TextBlob corpora (optional): `python -m textblob.download_corpora`

## License
MIT