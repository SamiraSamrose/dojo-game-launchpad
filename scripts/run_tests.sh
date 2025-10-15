#!/bin/bash
# scripts/run_tests.sh
# Run all tests

set -e

echo "🧪 Running Tests..."

# Install test dependencies
pip install -q pytest pytest-asyncio pytest-cov httpx

# Run tests with coverage
pytest backend/tests/ -v --cov=backend --cov-report=html --cov-report=term

echo "✅ All tests passed!"
echo "📊 Coverage report: htmlcov/index.html"
