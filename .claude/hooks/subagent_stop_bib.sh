#!/bin/bash
# BibTeX validation hook for SubagentStop
# Validates .bib files when domain-literature-researcher agent exits.
# Returns JSON with decision: "allow" or "block" with reason.

set -e

# Parse subagent context from stdin (Claude Code passes JSON via stdin)
SUBAGENT_CONTEXT=$(cat)

# Extract agent name and working directory
AGENT_NAME=$(echo "$SUBAGENT_CONTEXT" | jq -r '.agent_name // .subagent_type // empty')
WORKING_DIR=$(echo "$SUBAGENT_CONTEXT" | jq -r '.cwd // "."')

# Only validate for domain-literature-researcher agent
if [[ "$AGENT_NAME" != "domain-literature-researcher" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Find .bib files in working directory
BIB_FILES=$(find "$WORKING_DIR" -maxdepth 1 -name "*.bib" -type f 2>/dev/null || true)

if [[ -z "$BIB_FILES" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Validate each .bib file using CLAUDE_PROJECT_DIR for the validator path
ALL_ERRORS=""
for bib_file in $BIB_FILES; do
    # Run BibTeX syntax validator
    RESULT=$(python "$CLAUDE_PROJECT_DIR/.claude/hooks/bib_validator.py" "$bib_file" 2>&1 || true)
    VALID=$(echo "$RESULT" | jq -r '.valid // "true"')

    if [[ "$VALID" == "false" ]]; then
        # Extract errors and append to collection
        ERRORS=$(echo "$RESULT" | jq -r '.errors[]' 2>/dev/null || echo "$RESULT")
        ALL_ERRORS="${ALL_ERRORS}${ERRORS}
"
    fi

    # Run metadata provenance validator (checks fields against API JSON output)
    JSON_DIR="${WORKING_DIR}/intermediate_files/json"
    if [[ -d "$JSON_DIR" ]]; then
        METADATA_RESULT=$(python "$CLAUDE_PROJECT_DIR/.claude/hooks/metadata_validator.py" "$bib_file" "$JSON_DIR" 2>&1 || true)
        METADATA_VALID=$(echo "$METADATA_RESULT" | jq -r '.valid // "true"')

        if [[ "$METADATA_VALID" == "false" ]]; then
            METADATA_ERRORS=$(echo "$METADATA_RESULT" | jq -r '.errors[]' 2>/dev/null || echo "$METADATA_RESULT")
            ALL_ERRORS="${ALL_ERRORS}${METADATA_ERRORS}
"
        fi
    fi
done

# If there are errors, block with reason
if [[ -n "$ALL_ERRORS" ]]; then
    # Format errors as JSON-safe string
    REASON=$(printf '%s' "$ALL_ERRORS" | jq -Rs .)
    echo "{\"decision\": \"block\", \"reason\": $REASON}"
    exit 2
fi

echo '{"decision": "allow"}'
exit 0
