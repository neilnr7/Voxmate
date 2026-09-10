import os
import shutil

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


def write_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return {
            "success": True,
            "path": path,
            "message": "File written successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def rename_file(path, new_name):
    try:
        directory = os.path.dirname(path)
        new_path = os.path.join(directory, new_name)

        os.rename(path, new_path)

        return {
            "success": True,
            "old_path": path,
            "new_path": new_path,
            "message": "File renamed successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }




def copy_file(source, destination):
    try:
        shutil.copy2(source, destination)

        return {
            "success": True,
            "source": source,
            "destination": destination,
            "message": "File copied successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


import os
import shutil


def move_file(source, destination):
    try:
        # Check if source exists
        if not os.path.exists(source):
            return {
                "success": False,
                "error": f"Source does not exist: {source}"
            }

        # Prevent moving an item onto itself
        if os.path.abspath(source) == os.path.abspath(destination):
            return {
                "success": False,
                "error": "Source and destination are the same."
            }

        # If destination is an existing folder,
        # move the source inside that folder
        if os.path.isdir(destination):
            final_path = os.path.join(
                destination,
                os.path.basename(os.path.normpath(source))
            )
        else:
            final_path = destination

        # Prevent overwriting an existing destination
        if os.path.exists(final_path):
            return {
                "success": False,
                "error": f"Destination already exists: {final_path}"
            }

        shutil.move(source, final_path)

        # Verify the move actually happened
        if os.path.exists(final_path) and not os.path.exists(source):
            return {
                "success": True,
                "source": source,
                "destination": final_path,
                "message": "File or folder moved successfully."
            }

        return {
            "success": False,
            "error": "Move operation could not be verified."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def delete_file(path, recursive=False):
    try:
        # Check whether the path exists
        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"File or folder does not exist: {path}"
            }

        # Delete a file
        if os.path.isfile(path):
            os.remove(path)

            if not os.path.exists(path):
                return {
                    "success": True,
                    "path": path,
                    "message": "File deleted successfully."
                }

        # Delete a folder
        elif os.path.isdir(path):
            # Only delete non-empty folders when explicitly requested
            if not recursive and os.listdir(path):
                return {
                    "success": False,
                    "error": (
                        "Folder is not empty. "
                        "Use recursive=True to delete the folder and its contents."
                    )
                }

            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)

            if not os.path.exists(path):
                return {
                    "success": True,
                    "path": path,
                    "message": "Folder deleted successfully."
                }

        return {
            "success": False,
            "error": "Delete operation could not be verified."
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }



import os
from datetime import datetime


def get_file_info(path):
    try:
        # Check whether the path exists
        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"File or folder does not exist: {path}"
            }

        # Get basic information
        absolute_path = os.path.abspath(path)
        stats = os.stat(path)

        # Determine whether it is a file or folder
        if os.path.isfile(path):
            item_type = "file"
            extension = os.path.splitext(path)[1]
        elif os.path.isdir(path):
            item_type = "folder"
            extension = ""
        else:
            item_type = "other"
            extension = ""

        return {
            "success": True,
            "path": absolute_path,
            "name": os.path.basename(os.path.normpath(path)),
            "type": item_type,
            "extension": extension,
            "size_bytes": stats.st_size,
            "created": datetime.fromtimestamp(
                stats.st_ctime
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(
                stats.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "accessed": datetime.fromtimestamp(
                stats.st_atime
            ).strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

