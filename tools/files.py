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




