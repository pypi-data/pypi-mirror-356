import json
import uuid
from samsara_fn.clilogger import logger
from samsara_fn.commands.runners.args import RunArgs
from samsara_fn.commands.utils import load_function_config
from samsara_fn.commands.validate import is_one_level_str_dict
from samsara_fn.commands.runners.env import function_environment


def handle_manual_run(args: RunArgs, func_dir: str):
    """Handle manual function execution.

    This function:
    1. Loads the function configuration
    2. Handles parameter overrides:
       - Starts with base parameters from config
       - Adds manual trigger source
       - Applies any parameter overrides from file
       - Validates that all parameters are string values
    3. Sets up the function environment:
       - Creates unique run ID
       - Configures environment variables
       - Installs boto3 mocks
    4. Executes the function with parameters
    5. Ensures proper cleanup of environment

    Args:
        args: Command line arguments containing optional parametersOverride path
        func_dir: Directory containing the function code and configuration

    Returns:
        The function's return value or 1 on error
    """
    # Load function config
    config = load_function_config(func_dir)

    # Load parameters override if provided
    parameters = config.parameters.copy()
    parameters.update({"SamsaraFunctionTriggerSource": "manual"})
    if args.parametersOverride:
        with open(args.parametersOverride, "r") as f:
            override_params = json.load(f)
            if not is_one_level_str_dict("Parameters override", override_params):
                return 1
            parameters.update(override_params)

    runId = str(uuid.uuid4())
    logger.debug(
        f"Running Function {config.handler} manually with runId {runId} and parameters {parameters}"
    )

    with function_environment(runId, config.handler, func_dir) as func:
        return func(parameters, None)
