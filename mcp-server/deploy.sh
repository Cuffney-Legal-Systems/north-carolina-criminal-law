#!/usr/bin/env bash
# Deploy (or update) the NC AOC CR Forms MCP server via AWS SAM.
#
# First run:  sam deploy --guided creates samconfig.toml with your choices.
# Subsequent: sam deploy reads samconfig.toml — no prompts needed.
#
# Prerequisites: aws CLI configured, sam CLI installed, Python 3.13 available.

set -euo pipefail
cd "$(dirname "$0")"

echo "==> sam build"
sam build

if [ -f samconfig.toml ]; then
  echo "==> sam deploy (using samconfig.toml)"
  sam deploy
else
  echo "==> sam deploy --guided (first run — will create samconfig.toml)"
  sam deploy --guided
fi

echo ""
echo "==> Stack outputs"
STACK=$(grep -A1 'stack_name' samconfig.toml 2>/dev/null | tail -1 | tr -d ' ="' || echo "nc-aoc-cr-forms-mcp")
REGION=$(grep -A1 'region' samconfig.toml 2>/dev/null | tail -1 | tr -d ' ="' || echo "us-east-1")
aws cloudformation describe-stacks \
  --stack-name "$STACK" \
  --region "$REGION" \
  --query 'Stacks[0].Outputs' \
  --output table
