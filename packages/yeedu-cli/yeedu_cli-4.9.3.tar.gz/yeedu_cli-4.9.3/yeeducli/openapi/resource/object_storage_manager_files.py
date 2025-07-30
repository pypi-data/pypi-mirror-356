from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.file_utils import FileUtils
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys
import os

logger = Logger.get_logger(__name__, True)


class ObjectStorageManagerFiles:
    def list_object_storage_manager_files_by_id_or_name(pageNumber, limit, object_storage_manager_id=None, object_storage_manager_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/files"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "object_storage_manager_id": object_storage_manager_id,
                    "object_storage_manager_name": object_storage_manager_name,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_object_storage_manager_files_by_id_or_name_and_file_name(file_name, pageNumber, limit, object_storage_manager_id=None, object_storage_manager_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/files/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "file_name": file_name,
                    "object_storage_manager_id": object_storage_manager_id,
                    "object_storage_manager_name": object_storage_manager_name,
                    "pageNumber": pageNumber,
                    "limit": limit
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_object_storage_manager_files_by_id_or_name(object_storage_manager_id=None, object_storage_manager_name=None, file_id=None, file_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/file"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "object_storage_manager_id": object_storage_manager_id,
                    "object_storage_manager_name": object_storage_manager_name,
                    "file_id": file_id,
                    "file_name": file_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_object_storage_manager_files(local_file_path, overwrite, object_storage_manager_id=None, object_storage_manager_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/files"

            config.headers_files['X-File-Name'] = os.path.basename(
                local_file_path)

            config.headers_files['X-File-Size'] = str(
                os.path.getsize(local_file_path))

            chunk_size = 8 * 1024 * 1024  # 8 MB

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers_files,
                timeout=900,
                data=FileUtils.read_file_in_chunks(
                    local_file_path, chunk_size),
                params={
                    "object_storage_manager_id": object_storage_manager_id,
                    "object_storage_manager_name": object_storage_manager_name,
                    "overwrite": overwrite,
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_object_storage_manager_file_by_id_or_name(object_storage_manager_id=None, object_storage_manager_name=None, file_id=None, file_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/file"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "object_storage_manager_id": object_storage_manager_id,
                    "object_storage_manager_name": object_storage_manager_name,
                    "file_id": file_id,
                    "file_name": file_name
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
