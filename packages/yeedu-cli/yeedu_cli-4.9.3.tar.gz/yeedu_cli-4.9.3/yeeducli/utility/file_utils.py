from yeeducli.utility.logger_utils import Logger
import json
import os
import sys

logger = Logger.get_logger(__name__, True)


class FileUtils:

    def checkFilePathExists(file_path, argument, check_extension=False, extension=None, check_dir=False):
        try:
            if file_path == None:
                logger.error("Please provide a local file path\n")
                sys.exit(-1)
            else:
                if check_dir:
                    if file_path is not None and not os.path.isdir(file_path):
                        file_error = {
                            "error": f"The directory '{file_path}' cannot be found for the argument --{argument}"}
                        logger.error(json.dumps(file_error, indent=2))
                        sys.exit(-1)
                    else:
                        return file_path
                else:

                    if (file_path is not None and os.path.isfile(file_path)):

                        # checking if the file extension is of provided exxtension

                        if check_extension and extension is not None and os.path.splitext(file_path)[1] != extension:
                            extension_error = {
                                "error": f"The file at the provided path '{file_path}' must have the extension '{extension}'."
                            }
                            logger.error(json.dumps(extension_error, indent=2))
                            sys.exit(-1)
                        else:
                            return file_path
                    else:
                        file_error = {
                            "error": f"The file cannot be found at '{file_path}' for the argument --{argument}"}
                        logger.error(json.dumps(file_error, indent=2))
                        sys.exit(-1)
        except Exception as e:
            logger.error(f"Failed to check file path exists due to: {e}")
            sys.exit(-1)

    def readFileContent(file_path, validate_json=False):
        try:
            # 'with' statement automatically closes the file after the block is done
            with open(file_path, 'r') as f:
                file_content = f.read()

            if validate_json:
                try:
                    json_content = json.loads(file_content)
                    return json_content
                except json.JSONDecodeError as json_err:
                    logger.error(
                        f"Failed to read JSON file content from '{file_path}' due to: {json_err}")
                    sys.exit(-1)
            else:
                return file_content

        except Exception as e:
            logger.error(
                f"Failed to read file content from '{file_path}' due to: {e}")
            sys.exit(-1)

    def writeFileContent(file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)

            return {
                "message": f"Export successful and stored at location: {file_path}"
            }

        except Exception as e:
            logger.error(
                f"Failed to read file content from {file_path} due to: {e}")
            sys.exit(-1)

    def read_file_in_chunks(local_file_path, chunk_size=5242880):
        with open(local_file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
