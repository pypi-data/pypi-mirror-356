import logging
from typing import Optional
import difflib



class NLEParser:
    def __init__(self, config: dict, vocabulary: dict, stop_words: set):
        """
        The parser it's initialized with the static knowledge of the language.
        """
        self.config = config
        self.vocabulary = vocabulary
        self.stop_words = stop_words
        self.last_referenced_object: Optional[dict] = None
        self._logger = logging.getLogger(__name__)


    def _process_pronouns(self, tokens: list[str]) -> list[str]:
        """
        Substitutes pronouns for the last object referenced
        """
        pronouns = self.vocabulary["pronouns"]
        if not self.last_referenced_object:
            self._logger.debug("No last referenced object. Tokens unchanged: %s", tokens)
            return tokens  # No tokens to substitute

        new_tokens = []
        for token in tokens:
            if token in pronouns:
                self._logger.debug(
                    "Substituting pronoun '%s' with '%s'",
                    token,
                    self.last_referenced_object["canonical_name"],
                )
                new_tokens.append(self.last_referenced_object["canonical_name"])
            else:
                new_tokens.append(token)
        self._logger.debug("Tokens after pronoun processing: %s", new_tokens)
        return new_tokens

    def parse(self, command_input: str) -> Optional[dict]:
        """
        Receives a string from the player and returns a structured command.
        """
        self._logger.info("Parsing input: %s", command_input)
        # Lexical Analysis
        tokens = command_input.lower().split()
        self._logger.debug("Tokens after split: %s", tokens)
        cleaned_tokens = [t for t in tokens if t not in self.stop_words]
        self._logger.debug("Tokens after stop word removal: %s", cleaned_tokens)

        # Context resolution
        resolved_tokens = self._process_pronouns(cleaned_tokens)
        if not resolved_tokens:
            self._logger.warning("No tokens after pronoun processing.")
            return None

        self._logger.info("Resolved tokens: %s", resolved_tokens)

        # Debug block code
        verbs = self.vocabulary["verbs"]
        for token in resolved_tokens:
            if token in verbs:
                self._logger.info("Verb found: %s", token)

        objects = self.vocabulary["objects"]
        for token in resolved_tokens:
            if token in objects:
                self._logger.info("Object found: %s", token)

        # Syntax Analysis
        parsed_command = self._syntactic_analysis(resolved_tokens)
        return parsed_command

    def _syntactic_analysis(self, tokens: list[str]) -> Optional[dict]:
        """
        Analyse the structure of the tokens and return a strucutred command.
        Output example: {"verb": "pick", "object": "key"}
        """
        verbs = self.vocabulary["verbs"]
        objects = self.vocabulary["objects"]
        result = {}

        self._logger.debug("List tokens received: %s", tokens)

        for i, token in enumerate(tokens):
            if token in verbs:
                result["verb"] = token
                self._logger.debug("Verb found, syntactic Analysis: %s", token)
                # Procura o próximo token como objeto
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if next_token in objects:
                        self._logger.debug("Object found after verb: %s", next_token)
                        result["object"] = next_token
                    else:
                        suggestions = self._suggest_word(next_token, objects)
                        if suggestions:
                            self._logger.warning(
                                "Object '%s' not found. Did you mean: %s?",
                                next_token,
                                suggestions,
                            )
                break
            else:
                suggestions = self._suggest_word(token, verbs)
                if suggestions:
                    self._logger.warning(
                        "Verb '%s' not found. Did you mean: %s?", token, suggestions
                    )

        if "verb" in result:
            return result

        return None

    def update_context(self, last_object: dict):
        """
        Called in the main loop to update the last object of a well-succeeded command
        """
        self._logger.info("[Parser] Context updated. Last object: %s", last_object)
        self.last_referenced_object = last_object

    def _suggest_word(self, word: str, vocabulary: set) -> list[str]:
        """
        Suggest similar words from the vocabulary using difflib.
        """
        return difflib.get_close_matches(word, vocabulary, n=3, cutoff=0.6)
