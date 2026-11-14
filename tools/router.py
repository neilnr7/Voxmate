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
        """Split compound requests without breaking filenames."""

        parts = re.split(
            r"\b(?:and then|then|and)\b|[,;]",
            user_input,
            flags=re.IGNORECASE
        )

        parts = [
            part.strip()
            for part in parts
            if part.strip()
        ]

        if not parts:
            return [user_input]

        return parts

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

        # Web searching
        if re.search(
            r"\b(search\s+(?:the\s+)?(?:web|internet)|"
            r"search\s+for|look\s+up)\b",
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
            r"\b(increase|raise|turn\s+up|make\s+(?:the\s+)?"
            r"volume\s+louder)\b",
            text
        ):
            return "increase_volume"

        if re.search(
            r"\b(decrease|lower|turn\s+down|make\s+(?:the\s+)?"
            r"volume\s+quieter)\b",
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

    def rank_tools(self, user_input):
        """Rank tools using their names and core descriptions."""

        query_embedding = self.model.encode(
            user_input,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        name_scores = util.cos_sim(
            query_embedding,
            self.tool_name_embeddings
        )[0]

        description_scores = util.cos_sim(
            query_embedding,
            self.tool_description_embeddings
        )[0]

        combined_scores = (
            0.80 * name_scores
            + 0.20 * description_scores
        )

        ranked_indices = combined_scores.argsort(
            descending=True
        ).tolist()

        ranked_tools = []

        for index in ranked_indices:
            ranked_tools.append({
                "name": self.tool_names[index],
                "score": float(combined_scores[index])
            })

        return ranked_tools

    def select_tools(
        self,
        user_input,
        top_k=8,
        min_similarity=0.25,
        tools_per_part=1
    ):
        """Select relevant tools using rules first, then semantic ranking."""

        request_parts = self.split_request(user_input)

        tool_scores = {}

        for part in request_parts:
            # Use deterministic rules first. This avoids embedding
            # near-matches such as get_time for a get_date request.
            rule_based_tool = self.get_rule_based_tool(part)

            if (
                rule_based_tool
                and rule_based_tool in self.tool_names
            ):
                matching_tools = [{
                    "name": rule_based_tool,
                    "score": 1.0
                }]
            else:
                ranked_tools = self.rank_tools(part)

                matching_tools = [
                    tool for tool in ranked_tools
                    if tool["score"] >= min_similarity
                ][:1]

                if not matching_tools and ranked_tools:
                    matching_tools = ranked_tools[:1]

            for tool in matching_tools:
                name = tool["name"]
                score = tool["score"]

                if name not in tool_scores:
                    tool_scores[name] = score
                else:
                    tool_scores[name] = max(
                        tool_scores[name],
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
