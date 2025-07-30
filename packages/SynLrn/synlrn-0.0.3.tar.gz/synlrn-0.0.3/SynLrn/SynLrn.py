import inspect
import os
import re
import random

import sqlite3
from pathlib import Path
import logging
from rapidfuzz import fuzz
from dotenv import load_dotenv
from google.genai import types


load_dotenv()
logger = logging.getLogger(__name__)


class SynLrn:
    def __init__(self, stages, learningDir="Learned", fallbacks=None, knowledgeBase=None):
        self.learningDir = self.getDir(learningDir)
        self.STAGES = stages
        self.stageData = {}
        self.fallbacks = fallbacks
        KB = knowledgeBase if knowledgeBase is not None else __import__("SLKnowledgebase.Knowledgebase", fromlist=[""])
        self.components = [
            obj() for name, obj in inspect.getmembers(KB, inspect.isclass)
            if issubclass(obj, KB.Base) and obj is not KB.Base
        ]

        self._initializeDatabase()
        try:
            for stage in self.STAGES:
                loaded = self.loadStageData(stage)
                self.stageData[stage] = loaded if loaded else []
            self.addKnowledgebase()
        except sqlite3.Error as e:
            print(f"An error occurred during initialization: {e}")
            logger.error(f"An error occurred during initialization:", exc_info=True)

    def getDbFile(self):
        """
        Get the path to the learned database file.
        :return: Path to the learned database file as a string.
        """
        return self.getDir(self.learningDir, "Learned.db")

    def getDir(self, *paths):
        """
        Get the absolute path for the specified directory.
        :param paths: Directory paths to be joined.
        :return: Absolute path as a string.
        """
        return str(Path(*paths).resolve())

    def _getShowProcess(self):
        """
        Check if the learning process should be shown based on environment variables.
        :return: Boolean indicating whether to show the learning process.
        """
        load_dotenv(override=True)
        return os.getenv('SHOW_LEARNING_PROCESS', 'False') == 'True'

    def _initializeDatabase(self):
        """
        Initialize the SQLite database and create tables for each stage.
        This method creates a database file in the specified learning directory
        and sets up tables for each stage defined in the STAGES list.
        """
        self.dbFile = self.getDbFile()
        os.makedirs(os.path.dirname(self.dbFile), exist_ok=True)
        try:
            with sqlite3.connect(self.dbFile) as conn:
                cursor = conn.cursor()
                for stage in self.STAGES:
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {stage}Data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            content TEXT NOT NULL,
                            UNIQUE(content)
                        )
                    """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred during database initialization: {e}")
            logger.error(f"An error occurred during database initialization:", exc_info=True)

    def loadStageData(self, stage: str) -> list:
        """
        Load entries from the learned database for a specific stage.
        :param stage: The stage to load data for.
        :return: List of entries for the specified stage.
        """
        self.dbFile = self.getDbFile()
        try:
            with sqlite3.connect(self.dbFile) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT content FROM {stage}Data")
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"An error occurred while loading {stage}: {e}")
            logger.error(f"An error occurred while loading {stage}:", exc_info=True)
            return []

    def getStageData(self, stage: str) -> list:
        """
        Get data for a specific stage from all components.
        :param stage: The stage to retrieve data for.
        :return: List of entries for the specified stage.
        """
        stage = stage.strip().lower()
        methodName = f"{stage}Data"
        if stage not in self.STAGES:
            return []
        combined = []
        for component in self.components:
            stageMethod = getattr(component, methodName, None)
            if stageMethod and callable(stageMethod):
                combined.extend(stageMethod())
        return combined

    def getFallbacks(self, fallbackType: str) -> list:
        """
        Get fallback entries for a specific type.
        :param fallbackType: The type of fallback to retrieve.
        :return: List of fallback entries for the specified type.
        """
        if not self.fallbacks:
            return []
        if callable(self.fallbacks):
            return self.fallbacks(fallbackType)
        return self.fallbacks.get(fallbackType.lower(), [])

    def _normalize(self, text: str) -> str:
        """
        Normalize the input text by removing punctuation, converting to lowercase,
        and collapsing whitespace.
        :param text: The text to normalize.
        :return: Normalized text as a string.
        """
        return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', (text or '').lower())).strip()

    def _extractContext(self, entry: str) -> str:
        """
        Extract the context from a learned entry.
        :param entry: The learned entry from which to extract context.
        :return: The context part of the entry as a string.
        """
        if entry.startswith("user:\n"):
            return entry.split("assistant:")[0].replace("user:\n", "").strip()
        return ""

    def _escapeInnerQuotes(self, response: str) -> str:
        """
        Escape inner quotes in the response string.
        :param response: The response string to process.
        :return: The response string with inner quotes escaped.
        """
        if isinstance(response, list):
            response = str(response)
        if response.startswith("['") and response.endswith("']"):
            return response.replace('"', '\\"')
        return response

    def splitEntry(self, entry: str):
        """
        Split a learned entry into context and response parts.
        :param entry: The learned entry to split.
        :return: A tuple containing the context and response parts.
        """
        try:
            ctx, res = entry.split("\n\nassistant:\n", 1)
            ctx = ctx.replace("user:\n", "").strip()
            res = res.strip()
            return ctx, res
        except ValueError:
            return "", entry.strip()

    def retrieve(self, ctx: str, stage: str, entries: list, minScore: int = 60, fallbackCount: int = 5, isLearningActivated: bool = False):
        """
        Retrieve entries for a specific stage based on user input context.
        :param ctx: The user input context to match against learned entries.
        :param stage: The stage to retrieve entries for.
        :param entries: List of learned entries for the specified stage.
        :param minScore: Minimum score threshold for matching entries.
        :param fallbackCount: Number of fallback entries to return if no matches found.
        :param isLearningActivated: Flag to indicate if learning is activated.
        :return: List of matched entries for the specified stage.
        """
        try:
            fallback = self.getFallbacks(stage)
            inputNorm = self._normalize(ctx)

            matches = []
            for entry in entries:
                entryContextRaw = self._extractContext(entry)
                entryContext = self._normalize(entryContextRaw)
                score = fuzz.partial_ratio(inputNorm, entryContext)
                matches.append((score, entryContextRaw, entry))
                if self._getShowProcess() or isLearningActivated:
                    print(f"Score: {score} | Context: '{inputNorm}' ↔ DB: '{entryContext}'")

            matches.sort(reverse=True, key=lambda x: x[0])
            matched = [(s, c, e) for s, c, e in matches if s >= minScore]

            if self._getShowProcess() or isLearningActivated:
                print(f"\n--- {stage.capitalize()} Matches (score ≥ {minScore}) ---")
                for score, contextText, _ in matched:
                    print(f"[{round(score)}%] {contextText}")
                print("-" * 40 + "\n")

            if not matched:
                eligible = [entry for entry in entries if entry not in fallback]
                selected = random.sample(eligible, k=min(fallbackCount, len(eligible))) if eligible else []
            else:
                selected = [e for _, _, e in matched]

            combined = selected + [f for f in fallback if f not in selected]
            return combined

        except Exception as e:
            print(f"Error retrieving {stage}s: {e}")
            logger.error(f"Error retrieving {stage}s:", exc_info=True)
            return []

    def retrieveStage(self, ctx: str, stage: str, minScore: int = 60, fallbackCount: int = 5, isLearningActivated: bool = False):
        """
        Retrieve entries for a specific stage based on user input context.
        :param ctx: The user input context to match against learned entries.
        :param stage: The stage to retrieve entries for.
        :param minScore: Minimum score threshold for matching entries.
        :param fallbackCount: Number of fallback entries to return if no matches found.
        :param isLearningActivated: Flag to indicate if learning is activated.
        :return: List of matched entries for the specified stage.
        """
        stage = stage.lower()
        entries = self.stageData.get(stage, [])
        results = self.retrieve(ctx, stage, entries, minScore, fallbackCount, isLearningActivated)
        return results

    def saveStageData(self, stage: str, entries: list):
        """
        Save entries to the learned database for a specific stage.
        :param stage: The stage to which the entries belong.
        :param entries: List of entries to save.
        """
        self.dbFile = self.getDbFile()
        try:
            with sqlite3.connect(self.dbFile) as conn:
                cursor = conn.cursor()
                query = f"INSERT OR IGNORE INTO {stage}Data (content) VALUES (?)"
                cursor.executemany(query, ((entry,) for entry in entries))
                conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while saving {stage}: {e}")
            logger.error(f"An error occurred while saving {stage}:", exc_info=True)

    def addToLearned(self, stage: str, ctx: str, response: str, isLearningActivated: bool = False):
        """
        Add a new entry to the learned database.
        :param stage: The stage to which the entry belongs.
        :param ctx: The context or user input.
        :param response: The response or assistant output.
        :param isLearningActivated: Flag to indicate if learning is activated.
        """
        stage = stage.lower()
        normalizedCtx = self._normalize(ctx)
        for existing in self.stageData[stage]:
            existingCtx = self._extractContext(existing)
            if self._normalize(existingCtx) == normalizedCtx:
                if self._getShowProcess() or isLearningActivated:
                    print(f"[LEARNED SKIPPED - DUPLICATE CONTEXT] Stage: '{stage}' | Context: '{ctx}'")
                return
        response = self._escapeInnerQuotes(response)
        entry = f"user:\n{ctx}\n\nassistant:\n{response}"
        self.saveStageData(stage, [entry])
        self.stageData[stage].append(entry)
        if self._getShowProcess() or isLearningActivated:
            print(f"[LEARNED ADDED] Stage: '{stage}'\n{entry}\n" + "-" * 60)

    def addKnowledgebase(self):
        """
        Add knowledge base entries to the learned database.
        This method iterates through all defined stages and retrieves data from the knowledge base.
        If the stage data does not already exist in the database, it adds the entries.
        """
        for stage in self.STAGES:
            existing = self.loadStageData(stage)
            if existing:
                continue
            entries = self.getStageData(stage)
            for entry in entries:
                ctx, res = entry.split("\n\nassistant:\n", 1)
                ctx = ctx.replace("user:\n", "").strip()
                self.addToLearned(stage, ctx, res)

    def viewDatabase(self, stage: str = None):
        """
        View the contents of the learned database for a specific stage or all stages.
        :param stage: Optional; if provided, view only the specified stage's database.
        """
        if stage:
            stage = stage.lower()
            if stage in self.STAGES:
                self.viewLearnedDatabase(f"{stage}Data", stage, "-" * 50)
        else:
            for stage in self.STAGES:
                self.viewLearnedDatabase(f"{stage}Data", stage, "-" * 50)

    def viewLearnedDatabase(self, tableName: str, label: str, separator: str = "-" * 50):
        """
        View the contents of a specific learned database table.
        :param tableName: Name of the database table to view.
        :param label: Label for the table (e.g., "user", "assistant").
        :param separator: Separator string to print between entries.
        """
        dbFile = self.getDbFile()
        try:
            with sqlite3.connect(dbFile) as conn:
                cursor = conn.cursor()
                print(f"\n\n-------Learned {label.capitalize()}-------\n\n")
                cursor.execute(f"SELECT content FROM {tableName}")
                rows = cursor.fetchall()
                if rows:
                    for index, (content,) in enumerate(rows, start=1):
                        print(f"#{index}.\n{content}\n{separator}")
                else:
                    print(f"No {label} found.")
        except sqlite3.Error as e:
            print(f"An error occurred while viewing {label} database: {e}")
            logger.error(f"An error occurred while viewing {label} database:", exc_info=True)

    def handleTypedFormat(self, role: str = "user", content: str = ""):
        """
        Format content for Google GenAI APIs.
        """
        role    = role.lower()
        allowed = {"system", "user", "model"}
        if role not in allowed:
            raise ValueError(
                f"Invalid role '{role}'. Must be one of {', '.join(allowed)}."
            )
        if role == "system":
            return types.Part.from_text(text=content)
        return types.Content(role=role, parts=[types.Part.from_text(text=content)])

    def handleJsonFormat(self, role: str = "user", content: str = ""):
        """
        Format content for OpenAI APIs.
        """
        role    = role.lower()
        allowed = {"system", "developer", "user", "assistant"}
        if role not in allowed:
            raise ValueError(
                f"Invalid role '{role}'. Must be one of {', '.join(allowed)}."
            )
        return {'role': role, 'content': content}

