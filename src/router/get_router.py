from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from utils import DataStruct
from utils.request import get_logger, get_db_manager, get_ini_dict


get_router = APIRouter()


@get_router.get("/sensor_data/", response_model=List[DataStruct])
def get_sensor_data(db_manager=Depends(get_db_manager), logger=Depends(get_logger), ini_dict=Depends(get_ini_dict)) -> list:
    try:
        db_items = db_manager.get_recent_sensor_data(ini_dict)
        json_list = [item for item in db_items]
        
        logger.info("GET Router | DB List Data sent successfully")
        logger.info(f"GET Router | DB List Data sent successfully: {json_list}")
        return json_list

    except Exception as e:
        logger.error(f"GET Router | ERROR | Exception occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
