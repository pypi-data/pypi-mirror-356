# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Testing:**
```bash
# Run all tests
uv run --with pytest pytest

# Run specific test file
uv run --with pytest pytest tests/test_database.py

# Run tests with coverage
uv run --with pytest,pytest-cov pytest --cov=pinboard_tools
```

**Code Quality:**
```bash
# Format code
uv run --with ruff ruff format .

# Lint code
uv run --with ruff ruff check .

# Type checking
uv run --with mypy mypy pinboard_tools/
```

**Dependencies:**
```bash
# Add dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# Install all dependencies
uv sync
```

**Documentation:**
```bash
# Build documentation
cd docs && uv run --with sphinx sphinx-build -b html . _build/html

# Clean documentation build
rm -rf docs/_build

# View documentation (after building)
open docs/_build/html/index.html
```

**Read the Docs Hosting:**
- Configured with `.readthedocs.yaml` for automatic builds
- Uses uv for faster dependency management in RTD build environment
- Builds from `docs/conf.py` configuration
- Auto-deploys on git push to main branch

## Architecture Overview

This is a **Pinboard bookmark management library** with three core architectural layers:

### 1. Database Layer (`pinboard_tools/database/`)
- **Models**: SQLite-based storage with normalized tags via junction tables
- **Schema**: Full-text search support, sync status tracking, change triggers
- **Key Files**: `models.py` (database connection), `schema.sql` (complete schema)
- **Design**: Supports bidirectional sync with conflict detection and tag normalization

### 2. Sync Layer (`pinboard_tools/sync/`)
- **API Client**: Rate-limited Pinboard.in API wrapper with retry logic
- **Bidirectional Sync**: Handles local/remote conflicts and maintains sync state
- **Rate Limiting**: 3-second intervals between API requests (Pinboard requirement)

### 3. Analysis Layer (`pinboard_tools/analysis/`)
- **Tag Similarity**: Detects similar tags for consolidation
- **Tag Consolidation**: Merges duplicate tags across bookmarks
- **Utilities**: LLM chunking, datetime parsing for Pinboard format

## Database Schema Key Points

- **Normalized Tags**: Many-to-many relationship via `bookmark_tags` junction table
- **Sync Tracking**: `sync_status` field tracks pending changes ('synced', 'pending', 'error')
- **Change Detection**: Database triggers automatically mark bookmarks as needing sync
- **Full-Text Search**: FTS5 virtual table for content search
- **Conflict Resolution**: `original_tags` field stores pre-modification state

## API Integration Notes

- **Rate Limiting**: Pinboard API has 3-second minimum between requests
- **Authentication**: Requires Pinboard API token (format: `username:TOKEN`)
- **Sync Strategy**: Incremental sync based on last update timestamp
- **Error Handling**: Automatic retry on rate limit (429) errors

## Testing Approach

- **Temporary Databases**: Tests use `tempfile.NamedTemporaryFile` for isolation
- **Real API Testing**: Tests should use real Pinboard API (no mocking)
- **Fixtures**: Database fixture pattern in `tests/test_database.py`
- **Coverage**: Use pytest-cov for coverage reporting

## Key Dependencies

- **requests**: HTTP client for Pinboard API
- **sqlite3**: Built-in database (no external DB required)
- **typing**: Extensive type hints throughout codebase