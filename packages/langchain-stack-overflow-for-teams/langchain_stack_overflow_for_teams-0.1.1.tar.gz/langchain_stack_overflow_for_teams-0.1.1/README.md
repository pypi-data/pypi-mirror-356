# Stack Overflow for Teams for LangChain

This library provides a basic LangChain document loader for Stack Overflow for Teams.

## Document Loader Usage

### Free, Basic, and Business

```
loader = StackOverflowTeamsApiV3Loader(
    access_token=os.environ.get("SO_API_TOKEN"),
    team="my team",
    content_type="articles",
    date_from="2025-05-1T00:00:00.000",
)
docs = loader.load()
```

### Enterprise

```
loader = StackOverflowTeamsApiV3Loader(
    endpoint="mysite.mydomain.com/api",
    access_token=os.environ.get("SO_API_TOKEN"),
    content_type="articles",
    date_from="2025-05-1T00:00:00.000",
)
docs = loader.load()
```

### Enterprise with Private Team

```
loader = StackOverflowTeamsApiV3Loader(
    endpoint="mysite.mydomain.com/api",
    access_token=os.environ.get("SO_API_TOKEN"),
    team="my team",
    content_type="articles",
    date_from="2025-05-1T00:00:00.000",
)
docs = loader.load()
```
