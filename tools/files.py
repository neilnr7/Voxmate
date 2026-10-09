import os
import shutil
from datetime import datetime




def list_files(path):
    try:
        if not isinstance(path, str) or not path.strip():
            return {
                "success": False,
                "error": "Invalid path: a non-empty directory path is required."
            }

        path = os.path.abspath(os.path.expanduser(path.strip()))

        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"Path does not exist: {path}"
            }

        if not os.path.isdir(path):
            return {
                "success": False,
                "error": f"Path is not a directory: {path}"
            }

        items = sorted(os.listdir(path), key=str.lower)

        files = []
        folders = []

        for item in items:
            item_path = os.path.join(path, item)

            try:
                if os.path.isdir(item_path):
                    folders.append(item)
                else:
                    files.append(item)
            except OSError:
                # Keep inaccessible entries in the listing.
                files.append(item)

        return {
            "success": True,
            "path": path,
            "total_items": len(items),
            "total_files": len(files),
            "total_folders": len(folders),
            "files": files,
            "folders": folders
        }

    except PermissionError:
        return {
            "success": False,
            "error": f"Permission denied while accessing: {path}"
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": "The directory was removed or could not be found."
        }

    except NotADirectoryError:
        return {
            "success": False,
            "error": f"Path is not a directory: {path}"
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"Unable to list directory: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while listing files: {e}"
        }



def find_file(query, path):
    try:
        if not isinstance(query, str) or not query.strip():
            return {
                "success": False,
                "error": "Invalid search query: enter a filename or part of a filename."
            }

        if not isinstance(path, str) or not path.strip():
            return {
                "success": False,
                "error": "Invalid search path: a directory path is required."
            }

        query = query.strip()
        path = os.path.abspath(os.path.expanduser(path.strip()))

        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"Search path does not exist: {path}"
            }

        if not os.path.isdir(path):
            return {
                "success": False,
                "error": f"Search path is not a directory: {path}"
            }

        matches = []
        inaccessible = []
        scan_errors = []

        def handle_walk_error(error):
            scan_errors.append(str(error))

        for root, dirs, files in os.walk(
            path,
            onerror=handle_walk_error
        ):
            # Ignore directories that cannot be accessed.
            accessible_dirs = []

            for directory in dirs:
                directory_path = os.path.join(root, directory)

                if os.access(directory_path, os.R_OK | os.X_OK):
                    accessible_dirs.append(directory)
                else:
                    inaccessible.append(directory_path)

            dirs[:] = accessible_dirs

            for filename in files:
                if query.casefold() in filename.casefold():
                    matches.append(os.path.join(root, filename))

        matches.sort(key=str.casefold)

        return {
            "success": True,
            "query": query,
            "search_path": path,
            "total_matches": len(matches),
            "matches": matches,
            "inaccessible_directories": inaccessible,
            "scan_errors": scan_errors,
            "message": (
                f"Found {len(matches)} matching file(s)."
                if matches
                else "No matching files were found in the accessible locations."
            )
        }

    except PermissionError:
        return {
            "success": False,
            "error": f"Permission denied while searching: {path}"
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": "The search directory no longer exists."
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"File search failed: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while searching for files: {e}"
        }



def read_file(path):
    try:
        if not isinstance(path, str) or not path.strip():
            return {
                "success": False,
                "error": "Invalid path: a file path is required."
            }

        path = os.path.abspath(os.path.expanduser(path.strip()))

        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"File does not exist: {path}"
            }

        if not os.path.isfile(path):
            return {
                "success": False,
                "error": f"Path is not a file: {path}"
            }

        if not os.access(path, os.R_OK):
            return {
                "success": False,
                "error": f"Permission denied: cannot read file: {path}"
            }

        with open(path, "r", encoding="utf-8-sig") as file:
            content = file.read()

        return {
            "success": True,
            "path": path,
            "content": content,
            "message": "File read successfully."
        }

    except PermissionError:
        return {
            "success": False,
            "error": f"Permission denied while reading: {path}"
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": f"File does not exist: {path}"
        }

    except IsADirectoryError:
        return {
            "success": False,
            "error": f"Path is a directory, not a file: {path}"
        }

    except UnicodeDecodeError:
        return {
            "success": False,
            "error": "The file is not valid UTF-8 text and cannot be read as a text file."
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"Unable to read file: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while reading file: {e}"
        }


def create_file(path):
    try:
        if not isinstance(path, str) or not path.strip():
            return {
                "success": False,
                "error": "Invalid path: a file path is required."
            }

        path = os.path.abspath(os.path.expanduser(path.strip()))

        parent_dir = os.path.dirname(path)

        if not os.path.isdir(parent_dir):
            return {
                "success": False,
                "error": f"Parent directory does not exist: {parent_dir}"
            }

        if os.path.isdir(path):
            return {
                "success": False,
                "error": f"A directory already exists at this path: {path}"
            }

        # Exclusive mode prevents overwriting existing files.
        with open(path, "x", encoding="utf-8"):
            pass

        return {
            "success": True,
            "path": path,
            "message": "File created successfully."
        }

    except FileExistsError:
        return {
            "success": False,
            "error": f"A file already exists at this path: {path}"
        }

    except PermissionError:
        return {
            "success": False,
            "error": f"Permission denied while creating file: {path}"
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"Unable to create file: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while creating file: {e}"
        }



def write_file(path, content):
    try:
        if not isinstance(path, str) or not path.strip():
            return {
                "success": False,
                "error": "Invalid path: a file path is required."
            }

        if not isinstance(content, str):
            return {
                "success": False,
                "error": "Invalid content: content must be a string."
            }

        path = os.path.abspath(os.path.expanduser(path.strip()))

        if os.path.isdir(path):
            return {
                "success": False,
                "error": f"Path is a directory, not a file: {path}"
            }

        parent_dir = os.path.dirname(path)

        if not os.path.isdir(parent_dir):
            return {
                "success": False,
                "error": f"Parent directory does not exist: {parent_dir}"
            }

        # Create a new file or overwrite an existing file.
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return {
            "success": True,
            "path": path,
            "characters_written": len(content),
            "message": "File written successfully."
        }

    except PermissionError:
        return {
            "success": False,
            "error": f"Permission denied while writing to: {path}"
        }

    except IsADirectoryError:
        return {
            "success": False,
            "error": f"Path is a directory, not a file: {path}"
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"Unable to write to file: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while writing file: {e}"
        }






def rename_file(path, new_name):
    try:
        if not isinstance(path, str) or not path.strip():
            return {
                "success": False,
                "error": "Invalid path: the existing file path is required."
            }

        if not isinstance(new_name, str) or not new_name.strip():
            return {
                "success": False,
                "error": "Invalid new name: a non-empty filename is required."
            }

        path = os.path.abspath(os.path.expanduser(path.strip()))
        new_name = new_name.strip()

        if new_name in {".", ".."} or os.path.basename(new_name) != new_name:
            return {
                "success": False,
                "error": "Invalid new name: provide a filename, not a path."
            }

        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"File or folder does not exist: {path}"
            }

        if not os.path.isfile(path):
            return {
                "success": False,
                "error": f"Path is not a file: {path}"
            }

        directory = os.path.dirname(path)
        new_path = os.path.join(directory, new_name)

        if os.path.normcase(path) == os.path.normcase(new_path):
            return {
                "success": False,
                "error": "The new name is the same as the current name."
            }

        if os.path.exists(new_path):
            return {
                "success": False,
                "error": f"A file or folder already exists at: {new_path}"
            }

        # Rename without intentionally replacing an existing destination.
        os.rename(path, new_path)

        if os.path.isfile(new_path) and not os.path.exists(path):
            return {
                "success": True,
                "old_path": path,
                "new_path": new_path,
                "message": "File renamed successfully."
            }

        return {
            "success": False,
            "error": "Rename operation could not be verified."
        }

    except PermissionError:
        return {
            "success": False,
            "error": "Permission denied. The file may be in use or protected."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": f"The source file or destination directory was not found: {path}"
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"Unable to rename file: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while renaming file: {e}"
        }





def copy_file(source, destination):
    try:
        if not isinstance(source, str) or not source.strip():
            return {
                "success": False,
                "error": "Invalid source: a source file path is required."
            }

        if not isinstance(destination, str) or not destination.strip():
            return {
                "success": False,
                "error": "Invalid destination: a destination path is required."
            }

        source = os.path.abspath(os.path.expanduser(source.strip()))
        destination = os.path.abspath(os.path.expanduser(destination.strip()))

        if not os.path.exists(source):
            return {
                "success": False,
                "error": f"Source file does not exist: {source}"
            }

        if not os.path.isfile(source):
            return {
                "success": False,
                "error": f"Source is not a file: {source}"
            }

        if os.path.isdir(destination):
            destination = os.path.join(
                destination, os.path.basename(source)
            )

        parent_dir = os.path.dirname(destination)

        if not os.path.isdir(parent_dir):
            return {
                "success": False,
                "error": f"Destination directory does not exist: {parent_dir}"
            }

        if os.path.exists(destination):
            return {
                "success": False,
                "error": f"Destination already exists: {destination}"
            }

        shutil.copy2(source, destination)

        if os.path.isfile(destination):
            return {
                "success": True,
                "source": source,
                "destination": destination,
                "message": "File copied successfully."
            }

        return {
            "success": False,
            "error": "Copy operation could not be verified."
        }

    except PermissionError:
        return {
            "success": False,
            "error": "Permission denied while copying the file."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": "The source file or destination directory was not found."
        }

    except shutil.SameFileError:
        return {
            "success": False,
            "error": "Source and destination refer to the same file."
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"Unable to copy file: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while copying file: {e}"
        }



def move_file(source, destination):
    try:
        if not isinstance(source, str) or not source.strip():
            return {
                "success": False,
                "error": "Invalid source: a file or folder path is required."
            }

        if not isinstance(destination, str) or not destination.strip():
            return {
                "success": False,
                "error": "Invalid destination: a destination path is required."
            }

        source = os.path.abspath(os.path.expanduser(source.strip()))
        destination = os.path.abspath(os.path.expanduser(destination.strip()))

        if not os.path.exists(source):
            return {
                "success": False,
                "error": f"Source file or folder does not exist: {source}"
            }

        if os.path.normcase(source) == os.path.normcase(destination):
            return {
                "success": False,
                "error": "Source and destination are the same."
            }

        if os.path.isdir(destination):
            final_path = os.path.join(
                destination,
                os.path.basename(os.path.normpath(source))
            )
        else:
            final_path = destination

            parent_dir = os.path.dirname(final_path)

            if not os.path.isdir(parent_dir):
                return {
                    "success": False,
                    "error": f"Destination directory does not exist: {parent_dir}"
                }

        if os.path.exists(final_path):
            return {
                "success": False,
                "error": f"Destination already exists: {final_path}"
            }

        # Prevent moving a directory into itself or one of its descendants.
        if os.path.isdir(source):
            try:
                if os.path.commonpath([source, final_path]) == source:
                    return {
                        "success": False,
                        "error": "Cannot move a folder into itself or its own subfolder."
                    }
            except ValueError:
                pass

        shutil.move(source, final_path)

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

    except PermissionError:
        return {
            "success": False,
            "error": "Permission denied. The file or folder may be in use or protected."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": f"The source or destination path could not be found: {source}"
        }

    except shutil.Error as e:
        return {
            "success": False,
            "error": f"Unable to move file or folder: {e}"
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"Unable to move file or folder: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while moving file or folder: {e}"
        }




def delete_file(path, recursive=False):
    try:
        if not isinstance(path, str) or not path.strip():
            return {
                "success": False,
                "error": "Invalid path: a file or folder path is required."
            }

        if not isinstance(recursive, bool):
            return {
                "success": False,
                "error": "Invalid recursive value: expected True or False."
            }

        path = os.path.abspath(os.path.expanduser(path.strip()))

        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"File or folder does not exist: {path}"
            }

        if os.path.isfile(path):
            os.remove(path)

            if not os.path.exists(path):
                return {
                    "success": True,
                    "path": path,
                    "message": "File deleted successfully."
                }

        elif os.path.isdir(path):
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

    except PermissionError:
        return {
            "success": False,
            "error": "Permission denied. The file or folder may be in use or protected."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": f"File or folder does not exist: {path}"
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"Unable to delete file or folder: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while deleting: {e}"
        }






def get_file_info(path):
    try:
        if not isinstance(path, str) or not path.strip():
            return {
                "success": False,
                "error": "Invalid path: a file or folder path is required."
            }

        path = os.path.abspath(os.path.expanduser(path.strip()))

        if not os.path.exists(path):
            return {
                "success": False,
                "error": f"File or folder does not exist: {path}"
            }

        stats = os.stat(path)

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
            "path": path,
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

    except PermissionError:
        return {
            "success": False,
            "error": f"Permission denied while accessing: {path}"
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": f"File or folder does not exist: {path}"
        }

    except OSError as e:
        return {
            "success": False,
            "error": f"Unable to retrieve file information: {e}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error while retrieving file information: {e}"
        }

def create_folder(path):
    """Create a folder, including any missing parent directories."""
    try:
        path = os.path.abspath(path)

        if os.path.exists(path):
            if os.path.isdir(path):
                return {
                    "success": True,
                    "path": path,
                    "message": "Folder already exists."
                }

            return {
                "success": False,
                "error": "A file already exists at the requested path."
            }

        os.makedirs(path, exist_ok=False)

        return {
            "success": True,
            "path": path,
            "message": "Folder created successfully."
        }

    except OSError as e:
        return {
            "success": False,
            "error": str(e)
        }        