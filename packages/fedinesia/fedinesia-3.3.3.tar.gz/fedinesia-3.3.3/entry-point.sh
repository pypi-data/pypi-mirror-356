#!/bin/sh
set -e

cd /run

if test -z "${AUDIT_LOG_FILE}" ; then
    AUDIT="--audit-log-file="
else
    AUDIT="--audit-log-file=${AUDIT_LOG_FILE}"
fi

if test -z "${AUDIT_STYLE}" ; then
    STYLE="--audit-log-style=PLAIN"
else
    STYLE="--audit-log-style=${AUDIT_STYLE}"
fi

if test -z "${LIMIT}" ; then
    MAX_DELETE="--limit=0"
else
    MAX_DELETE="--limit=${LIMIT}"
fi

if test -z "${DRY_RUN}" ; then
    RUN_DRY="--no-dry-run"
else
    RUN_DRY="--dry-run"
fi

if test -z "${PROGRESS_FILE}" ; then
    PROGRESS="--save-progress="
else
    PROGRESS="--save-progress=${PROGRESS_FILE}"
fi

if test -z "${CONTINUE_PROGRESS}" ; then
    CONTINUE="--no-continue"
else
    CONTINUE="--continue"
fi

if test -z "${LOGGING_CONFIG}" ; then
    LOGGING="--logging-config=/logging/logging-config.toml"
else
    LOGGING="--logging-config=${LOGGING_CONFIG}"
fi

if test -z "${PAUSE_IN_SECONDS}" ; then
    exit 1
fi

while true
do
    uv run fedinesia -c /config/config.json "${AUDIT}" "${STYLE}" "${MAX_DELETE}" "${RUN_DRY}" "${PROGRESS}" "${CONTINUE}" "${LOGGING}"
    printf "\n%s - Waiting for %s seconds.\n\n" "$(date +%R:%S)" "${PAUSE_IN_SECONDS}"
    sleep "${PAUSE_IN_SECONDS}"
done
