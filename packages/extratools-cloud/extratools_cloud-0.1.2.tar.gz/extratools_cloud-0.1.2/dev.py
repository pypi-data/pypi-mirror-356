import logging

import uvicorn
from extratools_api.crudl import add_crudl_endpoints_for_mapping
from fastapi import FastAPI

from extratools_cloud.aws.sqs import get_resource_dict as get_sqs_resource_dict

app = FastAPI(debug=True)

add_crudl_endpoints_for_mapping(
    app,
    "/aws/sqs",
    get_sqs_resource_dict(json_only=True),
    values_in_list=True,
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level=logging.DEBUG,
    )
