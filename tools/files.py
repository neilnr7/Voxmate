import os


def list_files(path):
    try:
        items = os.listdir(path)

        return {
            "success": True,
            "path": path,
            "files": items
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def find_file(query, path):
    matches = []

    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                if query.lower() in file.lower():
                    matches.append(os.path.join(root, file))

        return {
            "success": True,
            "query": query,
            "matches": matches
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        return {
            "success": True,
            "path": path,
            "content": content
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def create_file(path):
    try:
        with open(path, "x", encoding="utf-8"):
            pass

        return {
            "success": True,
            "path": path,
            "message": "File created successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


