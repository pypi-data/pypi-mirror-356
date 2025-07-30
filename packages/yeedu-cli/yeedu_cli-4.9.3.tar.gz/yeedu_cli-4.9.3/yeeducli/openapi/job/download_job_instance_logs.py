from requests.structures import CaseInsensitiveDict
from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class DownloadJobInstanceLogs:
    def get_job_instance_log_records(workspace_id, log_type, job_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job/{job_id}/log/{log_type}"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                stream=True
            ).send_http_request()

            if (response.status_code == 200 and CaseInsensitiveDict(response.headers).get('Content-Type') == 'text/plain' and CaseInsensitiveDict(response.headers).get('Content-disposition')):
                try:
                    for line in response.iter_lines(decode_unicode=True):
                        if line:
                            logger.info(line)

                    return True

                except Exception as e:
                    logger.exception(
                        f"Failed to get spark job instance logs due to : {e}")
                    sys.exit(-1)
            else:
                return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
