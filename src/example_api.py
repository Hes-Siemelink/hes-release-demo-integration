import logging
import requests
from digitalai.release.container import BaseTask

logger = logging.getLogger('Digitalai')


class ExampleApi(BaseTask):
    """
       This class represents an API that retrieves information about a product.
    """
    def __init__(self, params):
        """
        Initializes the task with the given parameters.
        """
        super().__init__()
        self.params = params

    def execute(self) -> None:
        """Execute the task to retrieve information about a product."""

        # Log the task property values for debugging purposes
        logger.debug(f"Task property values are  : {self.params}")

        try:
            # Construct the request URL using the 'productId' parameter
            request_url = "https://dummyjson.com/products/" + self.params['productId']

            # Add a comment to the task log with the request URL
            self.add_comment(f"Request URL is {request_url}")

            # Send a GET request to the URL and raise an exception if the response is not successful
            response = requests.get(request_url)
            response.raise_for_status()

            # Extract the 'title' and 'brand' fields from the response and store them in the output properties
            output_properties = self.get_output_properties()
            output_properties['productName'] = response.json()['title']
            output_properties['brand'] = response.json()['brand']

        # Catch, log and set the exit code any unexpected errors that occurred
        except Exception as e:
            logger.error("Unexpected error occurred.", exc_info=True)
            self.set_exit_code(1)
            self.set_error_message(str(e))
