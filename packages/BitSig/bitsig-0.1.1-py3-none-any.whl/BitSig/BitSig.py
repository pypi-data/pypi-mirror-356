
import logging
from pathlib import Path
from datetime import datetime, timedelta
import threading
import time
import os
import re
import hashlib
from dotenv import load_dotenv

logCleanupLock  = threading.Lock()
LOG_ENTRY_START = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} \[\w+\]")

load_dotenv()

LOG_RETENTION_HOURS = int(os.getenv("LOG_RETENTION_HOURS", "24"))  # Default to 24 hours if not set

class SybilErrorPrefixFilter(logging.Filter):
    """
    Prefixes error/critical log messages with Sybil's signature phrase.
    """
    def filter(self, record):
        if record.levelno >= logging.ERROR and not str(record.msg).startswith("I have detected this error in the system:"):
            record.msg = f"I have detected this error in the system: {record.msg}"
        return True

class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

class DedupFileHandler(logging.FileHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            msgLines = msg.splitlines()
            if not msgLines:
                # nothing to write
                return

            # Normalize the body (everything after the timestamp line)
            newBody = "\n".join(msgLines[1:]).rstrip("\n")

            path = Path(self.baseFilename)
            if path.exists():
                with path.open("r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Split the existing file into entries
                entries = []
                current = []
                for line in lines:
                    if LOG_ENTRY_START.match(line):
                        if current:
                            entries.append(current)
                            current = []
                    current.append(line)
                if current:
                    entries.append(current)

                # Re-write only those entries whose body != newBody
                with path.open("w", encoding="utf-8") as f:
                    for entry in entries:
                        existingBody = "".join(entry[1:]).rstrip("\n")
                        if existingBody != newBody:
                            f.writelines(entry)

            # Now write the new, latest entry
            super().emit(record)

        except Exception:
            self.handleError(record)

def cleanOldLogs(logsDir):
    with logCleanupLock:
        cutoff = datetime.now() - timedelta(hours=LOG_RETENTION_HOURS)

        for file in logsDir.glob("*.txt"):
            if not file.is_file():
                continue

            retainedLines = []
            currentEntry  = []

            with file.open("r", encoding="utf-8") as f:
                for line in f:
                    if LOG_ENTRY_START.match(line):
                        if currentEntry:
                            if isRecentLogEntry(currentEntry[0], cutoff):
                                retainedLines.extend(currentEntry)
                            currentEntry = []
                    currentEntry.append(line)

                if currentEntry and isRecentLogEntry(currentEntry[0], cutoff):
                    retainedLines.extend(currentEntry)

            with file.open("w", encoding="utf-8") as f:
                f.writelines(retainedLines)

def isRecentLogEntry(firstLine, cutoff):
    try:
        timestampStr = firstLine.split(" [")[0]
        logTime = datetime.strptime(timestampStr, "%Y-%m-%d %H:%M:%S,%f")
        return logTime >= cutoff
    except Exception:
        return True  # Preserve malformed entries

def startCleanupThread(logsDir):
    def runCleanupLoop():
        while True:
            try:
                cleanOldLogs(logsDir)
            except Exception:
                pass
            time.sleep(60 * 60)

    thread = threading.Thread(target=runCleanupLoop, daemon=True)
    thread.start()

def configureBitSig(logsDir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logsDir.mkdir(parents=True, exist_ok=True)

    cleanOldLogs(logsDir)
    startCleanupThread(logsDir)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    logLevels = {
        'DEBUG':    logging.DEBUG,
        'INFO':     logging.INFO,
        'WARNING':  logging.WARNING,
        'ERROR':    logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    for levelName, levelValue in logLevels.items():
        filePath = logsDir / f"{levelName.capitalize()}.txt"
        handler  = DedupFileHandler(str(filePath), encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        handler.addFilter(LevelFilter(levelValue))
        if levelValue >= logging.ERROR:
            handler.addFilter(SybilErrorPrefixFilter())
        logger.addHandler(handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.ERROR)  # Only error and critical to console
    consoleHandler.setFormatter(formatter)
    consoleHandler.addFilter(SybilErrorPrefixFilter())
    logger.addHandler(consoleHandler)


BitSig=configureBitSig