from cloudwatch_logger import CloudWatchLogger as logger

def function_that_raises_exception():
    """
    A sample function that intentionally raises an exception.
    """
    raise ValueError("This is a test exception")

if __name__ == "__main__":
    try:
        # Call the function that will raise an exception
        function_that_raises_exception()
    except Exception as e:
        # Log the exception using CloudWatchLogger
        logger.log(e)
