class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, function):
        self.tools[name] = function

    def execute(self, name, arguments):
        if name not in self.tools:
            return {
                "success": False,
                "error": f"Unknown tool: {name}"
            }

        try:
            result = self.tools[name](**arguments)

            return {
                "success": True,
                "result": result
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_tools(self):
        return self.tools