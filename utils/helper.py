import http

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from controller.context_manager import context_api_id, context_log_meta
from logger import logger
from models.base import GenericResponseModel


def build_api_response(generic_response: GenericResponseModel) -> JSONResponse:
    try:
        if not generic_response.api_id:
            generic_response.api_id = context_api_id.get()
        if not generic_response.status_code:
            generic_response.status_code = http.HTTPStatus.OK if not generic_response.errors \
                else http.HTTPStatus.UNPROCESSABLE_ENTITY
        response_json = jsonable_encoder(generic_response)
        res = JSONResponse(status_code=generic_response.status_code, content=response_json)
        logger.info(extra=context_log_meta.get(),
                    msg="build_api_response: Generated Response with status_code:"
                        + f"{generic_response.status_code}")
        return res
    except Exception as e:
        logger.error(extra=context_log_meta.get(), msg=f"exception in build_api_response error : {e}")
        return JSONResponse(status_code=generic_response.status_code, content=generic_response.errors)
