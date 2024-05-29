from datetime import datetime
import logging
import requests

class BaseDataLoader:
    def __init__(self, endpoint=None):
        self._base_url = endpoint
        self.logger = logging.getLogger(__name__)

    def _get_req(self, resource, params=None):
        req_url = self._base_url + resource
        self.logger.info(f"Making GET request to {req_url}")
        if params is not None:
            response = requests.get(req_url, params=params)
        else:
            response = requests.get(req_url)
        if response.status_code != 200:
            msg = f"Unable to request data from {req_url}, status: {response.status_code}"
            if response.text and response.text.message:
                msg += f", message: {response.text.message}"
            self.logger.error(msg)
            raise RuntimeError(msg)
        return response.text

if __name__ == "__main__":
   
    logging.basicConfig(level=logging.DEBUG)
    
    
    file_handler = logging.FileHandler('data_loader.log')
    file_handler.setLevel(logging.INFO)  
    
   
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    
    
    loader = BaseDataLoader()
