import re

from sentence_transformers import SentenceTransformer, util


class SemanticToolRouter:
    def __init__(
        self,
        registry,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.registry = registry

        self.model = SentenceTransformer(model_name)

        self.tool_names = list(registry.get_tools().keys())

        self.tool_name_texts = []
        self.tool_descriptions = []

        for name in self.tool_names:
            schema = registry.get_tool_schema(name)
            function = schema["function"]

            description = function.get("description", "")

            # Keep only the core description, excluding parameter examples.
            description = re.split(
                r"\n\s*Args\s*:",
                description,
                maxsplit=1
            )[0].strip()

            self.tool_name_texts.append(
                name.replace("_", " ")
            )

            self.tool_descriptions.append(description)

        self.tool_name_embeddings = self.model.encode(
            self.tool_name_texts,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        self.tool_description_embeddings = self.model.encode(
            self.tool_descriptions,
            convert_to_tensor=True,
            normalize_embeddings=True
        )


    def split_request(self, user_input):
        """Split compound requests while preserving filenames and phrases."""

        action_words = (
            r"open|launch|start|run|search|look|find|locate|"
            r"create|make|delete|remove|copy|move|rename|"
            r"read|write|save|close|switch|focus|increase|"
            r"decrease|set|check|show|list|take|capture"
        )

        parts = re.split(
            rf"\s*(?:;|\band\s+then\b|\bthen\b)\s*"
            rf"|\s+and\s+(?=(?:{action_words})\b)"
            rf"|,\s*(?=(?:{action_words})\b)",
            user_input,
            flags=re.IGNORECASE
        )

        parts = [part.strip() for part in parts if part.strip()]

        return parts if parts else [user_input]


    def get_rule_based_tool(self, user_input):
        """Identify clear tool intents before using semantic ranking."""

        text = user_input.lower().strip()

        # Application switching
        if re.search(
            r"\b(switch\s+to|focus(?:\s+on)?|activate|bring\s+to\s+front)\b",
            text
        ):
            return "focus_app"

        # Close an application
        if re.search(
            r"\b(close|quit|exit)\s+(?:the\s+)?"
            r"(?:application|app|program|software|notepad|calculator|"
            r"chrome|edge|firefox|browser|word|excel)\b",
            text
        ):
            return "close_app"

        # Keyboard shortcuts must be checked before single-key presses.
        if re.search(
            r"\b(ctrl|control|alt|shift|win|windows)\b",
            text
        ) and re.search(
            r"\b(press|hit|use|hold)\b",
            text
        ):
            return "hotkey"

        # Browser back navigation
        if re.search(
            r"\b(go\s+back|back\s+to\s+the\s+previous\s+page|"
            r"previous\s+webpage)\b",
            text
        ):
            return "go_back"


        # File search must be checked before general web search.
        if re.search(
            r"\b(find|locate|search\s+for)\b.*"
            r"\b(file|document)\b",
            text
        ):
            return "find_file"

        # Web searching
        if re.search(
            r"\b(search\s+(?:the\s+)?(?:web|internet)|look\s+up)\b",
            text
        ):
            return "search_web"


        # Website navigation
        website_names = (
            "google",
            "youtube",
            "github",
            "gmail",
            "wikipedia",
            "reddit",
            "amazon",
            "facebook",
            "instagram",
            "linkedin",
            "twitter",
            "stackoverflow",
            "chatgpt",
            "openai"
        )

        website_pattern = (
            r"\b(?:open|visit|go\s+to|navigate\s+to)\s+"
            r"(?:the\s+)?(?:"
            + "|".join(re.escape(name) for name in website_names)
            + r")\b"
        )

        if re.search(website_pattern, text):
            return "open_url"

        # Explicit URL navigation
        if re.search(
            r"\b(?:open|visit|go\s+to|navigate\s+to)\s+"
            r"(?:https?://|www\.)",
            text
        ):
            return "open_url"

        # Browser application launching
        browser_names = (
            "google chrome",
            "chrome",
            "microsoft edge",
            "edge",
            "firefox",
            "brave",
            "opera"
        )

        browser_pattern = (
            r"\b(?:open|launch|start|run)\s+"
            r"(?:the\s+)?(?:"
            + "|".join(
                re.escape(name) for name in browser_names
            )
            + r")\b"
        )

        if re.search(browser_pattern, text):
            return "open_app"

        # Generic text editor launching
        if re.search(
            r"\b(bring\s+up|open|launch|start|run)\b.*"
            r"\b(plain\s+text\s+editor|text\s+editor)\b",
            text
        ):
            return "open_app"
        # General application launching. Website names and URLs have
        # already been handled above.
        if re.search(
            r"\b(?:open|launch|start|run)\s+"
            r"(?:the\s+)?(?:notepad|calculator|calc|"
            r"paint|word|excel|powerpoint|file\s+explorer|"
            r"task\s+manager|command\s+prompt|cmd|"
            r"powershell|vscode|visual\s+studio\s+code)\b",
            text
        ):
            return "open_app"

        # System date and time
        if re.search(
            r"\b(date\s+today|today'?s\s+date|current\s+date|"
            r"what\s+date\s+is\s+it|what\s+is\s+the\s+date)\b",
            text
        ):
            return "get_date"

        if re.search(
            r"\b(time\s+now|current\s+time|what\s+time\s+is\s+it|"
            r"what'?s\s+the\s+time|tell\s+me\s+the\s+time)\b",
            text
        ):
            return "get_time"

        # Battery status
        if re.search(
            r"\b(battery|battery\s+level|remaining\s+battery|"
            r"power\s+remaining)\b",
            text
        ):
            return "get_battery"

        # Volume controls: specific direction before generic volume.
        if re.search(
            r"\b(mute|silence)\b",
            text
        ):
            return "mute_volume"

        if re.search(
            r"\b(unmute|turn\s+(?:the\s+)?sound\s+on)\b",
            text
        ):
            return "unmute_volume"

        if re.search(
            r"\b(increase|raise)\s+(?:the\s+)?volume\b|"
            r"\bturn\s+up\s+(?:the\s+)?volume\b|"
            r"\bmake\s+(?:the\s+)?volume\s+louder\b",
            text
        ):
            return "increase_volume"

        if re.search(
            r"\b(decrease|lower)\s+(?:the\s+)?volume\b|"
            r"\bturn\s+down\s+(?:the\s+)?volume\b|"
            r"\bmake\s+(?:the\s+)?volume\s+quieter\b",
            text
        ):
            return "decrease_volume"

        if re.search(
            r"\b(set|change)\s+(?:the\s+)?volume\b",
            text
        ):
            return "set_volume"

        # Brightness controls
        if re.search(
            r"\b(increase|raise|turn\s+up|brighten)\b.*\bbrightness\b|"
            r"\bbrightness\b.*\b(increase|raise|higher|up)\b",
            text
        ):
            return "increase_brightness"

        if re.search(
            r"\b(decrease|lower|dim|turn\s+down)\b.*\bbrightness\b|"
            r"\bbrightness\b.*\b(decrease|lower|dimmer|down)\b",
            text
        ):
            return "decrease_brightness"

        if re.search(
            r"\b(set|change)\s+(?:the\s+)?brightness\b",
            text
        ):
            return "set_brightness"

        # Text entry and keyboard input
        if re.search(
            r"\b(type|write|enter)\s+",
            text
        ):
            return "type_text"

        if re.search(
            r"\b(press|hit)\s+(?:the\s+)?"
            r"(enter|return|tab|escape|esc|space|backspace|"
            r"delete|home|end|up|down|left|right)\b",
            text
        ):
            return "press_key"

        # Mouse input
        if re.search(r"\b(double[\s-]?click|right[\s-]?click|click)\b", text):
            return "click"

        if re.search(r"\b(scroll|scrolling)\b", text):
            return "scroll"

        # Screenshot
        if re.search(
            r"\b(take|capture)\s+(?:a\s+)?screenshot\b|"
            r"\bscreenshot\s+(?:of|my|the)\b",
            text
        ):
            return "take_screenshot"

        # Clipboard
        if re.search(
            r"\b(read|show|get|check)\s+(?:the\s+)?clipboard\b",
            text
        ):
            return "read_clipboard"

        if re.search(
            r"\b(copy|put|write)\s+.+\s+to\s+(?:the\s+)?clipboard\b|"
            r"\bwrite\s+to\s+(?:the\s+)?clipboard\b",
            text
        ):
            return "write_clipboard"

        if re.search(
            r"\b(clear|empty)\s+(?:the\s+)?clipboard\b",
            text
        ):
            return "clear_clipboard"

        # File and folder operations
        # Reading document contents
        if re.search(
            r"\b(read|retrieve|get|show|display)\b.*"
            r"\b(contents?|text)\b.*"
            r"\b(document|file)\b",
            text
        ):
            return "read_file"
        if re.search(
            r"\b(create|make|new)\s+(?:a\s+)?folder\b",
            text
        ):
            return "create_folder"

        if re.search(
            r"\b(list|show)\s+(?:all\s+)?files\b|"
            r"\blist\s+(?:the\s+)?contents\s+of\b",
            text
        ):
            return "list_files"

        if re.search(
            r"\b(find|search\s+for|locate)\s+(?:the\s+)?file\b",
            text
        ):
            return "find_file"

        if re.search(r"\b(read|open)\s+(?:the\s+)?file\b", text):
            return "read_file"

        if re.search(
            r"\b(create|make)\s+(?:a\s+)?(?:new\s+)?file\b",
            text
        ):
            return "create_file"

        if re.search(r"\b(write|save)\s+.+\s+to\s+(?:the\s+)?file\b", text):
            return "write_file"

        if re.search(r"\b(rename)\s+(?:the\s+)?file\b", text):
            return "rename_file"

        if re.search(r"\b(copy)\s+(?:the\s+)?file\b", text):
            return "copy_file"

        if re.search(r"\b(move)\s+(?:the\s+)?file\b", text):
            return "move_file"

        if re.search(r"\b(delete|remove)\s+(?:the\s+)?file\b", text):
            return "delete_file"

        if re.search(
            r"\b(file\s+information|file\s+info|file\s+details|"
            r"file\s+properties|metadata)\b",
            text
        ):
            return "get_file_info"

        # Running applications
        if re.search(
            r"\b(list|show|check)\s+(?:the\s+)?"
            r"(?:currently\s+)?running\s+apps?\b",
            text
        ):
            return "list_running_apps"

        return None


    def _rank_tools_batch(self, user_inputs):
        """Rank multiple requests using a single embedding call."""

        if not user_inputs:
            return []

        query_embeddings = self.model.encode(
            user_inputs,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        name_scores = util.cos_sim(
            query_embeddings,
            self.tool_name_embeddings
        )

        description_scores = util.cos_sim(
            query_embeddings,
            self.tool_description_embeddings
        )

        combined_scores = (
            0.80 * name_scores
            + 0.20 * description_scores
        )

        batch_results = []

        for row in combined_scores:
            ranked_indices = row.argsort(
                descending=True
            ).tolist()

            ranked_tools = [
                {
                    "name": self.tool_names[index],
                    "score": float(row[index])
                }
                for index in ranked_indices
            ]

            batch_results.append(ranked_tools)

        return batch_results


    def rank_tools(self, user_input):
        """Rank tools using their names and core descriptions."""

        return self._rank_tools_batch([user_input])[0]



    def select_tools(
        self,
        user_input,
        top_k=8,
        min_similarity=0.25,
        tools_per_part=1
    ):
        """Select tools using rule-based routing and batch semantic ranking."""

        request_parts = self.split_request(user_input)

        tool_scores = {}
        semantic_parts = []


        # First resolve all rule-based matches.
        for part in request_parts:

            rule_based_tool = self.get_rule_based_tool(part)

            if (
                rule_based_tool
                and rule_based_tool in self.tool_names
            ):
                tool_scores[rule_based_tool] = max(
                    tool_scores.get(rule_based_tool, 0.0),
                    1.0
                )

            else:
                semantic_parts.append(part)


        # Encode all semantic requests together.
        if semantic_parts:
            batch_rankings = self._rank_tools_batch(
                semantic_parts
            )

            for ranked_tools in batch_rankings:

                matching_tools = [
                    tool for tool in ranked_tools
                    if tool["score"] >= min_similarity
                ][:max(1, tools_per_part)]

                if not matching_tools and ranked_tools:
                    matching_tools = ranked_tools[:1]

                for tool in matching_tools:
                    name = tool["name"]
                    score = tool["score"]

                    tool_scores[name] = max(
                        tool_scores.get(name, 0.0),
                        score
                    )

        selected_tools = sorted(
            [
                {
                    "name": name,
                    "score": score
                }
                for name, score in tool_scores.items()
            ],
            key=lambda tool: tool["score"],
            reverse=True
        )

        return selected_tools[:top_k]
