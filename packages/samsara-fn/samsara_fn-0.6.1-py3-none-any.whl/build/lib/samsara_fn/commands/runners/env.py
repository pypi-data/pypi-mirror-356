import os
from typing import Callable
from contextlib import contextmanager
from samsara_fn.commands.utils import (
    get_code_dir,
    get_temp_dir,
    func_name_from_dir,
)
from samsara_fn.commands.runners.loader import load_handler_module

SamsaraSimulatorRunIdEnvVar = "__DoNotUseSamsaraSimulatorRunId"
SamsaraSimulatorConfigDirEnvVar = "__DoNotUseSamsaraSimulatorConfigDir"


def get_env_for_function(suffix: str, func_dir: str) -> dict:
    """
    Get the environment for a function.

    This function provides a set of environment variables that simulate
    the AWS Lambda and Samsara Functions environment. The suffix parameter
    allows for unique identification of different function executions.

    Only these specified environment variables will be available to the function,
    similar to how AWS Lambda isolates the environment.

    Args:
        suffix: A unique identifier for the function execution

    Returns:
        Dictionary of environment variables
    """
    function_name = func_name_from_dir(func_dir)
    org_id = os.environ.get("SAMSARA_ORG_ID", "1")
    code_path = get_code_dir(function_name)
    temp_storage_path = get_temp_dir(function_name)

    return {
        # AWS Lambda environment
        "AWS_EXECUTION_ENV": f"samsara-functions-simulator-env-{suffix}",
        # Samsara Functions environment
        "SamsaraFunctionExecRoleArn": f"arn:aws:iam::123456789012:role/samsara-functions-simulator-{suffix}",
        "SamsaraFunctionSecretsPath": f"samsara-functions-simulator-secrets-path-{suffix}",
        "SamsaraFunctionStorageName": f"samsara-functions-simulator-storage-name-{suffix}",
        "SamsaraFunctionName": function_name,
        "SamsaraFunctionOrgId": org_id,
        "SamsaraFunctionCodePath": code_path,
        "SamsaraFunctionTempStoragePath": temp_storage_path,
        SamsaraSimulatorRunIdEnvVar: suffix,
        SamsaraSimulatorConfigDirEnvVar: func_dir,
    }


def override_env_for_invocation(env: dict) -> Callable[[], None]:
    """
    Create a function to override environment variables for a function invocation.

    This function:
    1. Removes all existing environment variables
    2. Sets only the specified function-specific environment variables
    3. Returns a cleanup function to restore the original environment

    Args:
        env: Dictionary of environment variables to set

    Returns:
        A cleanup function that restores the original environment
    """
    # Store original environment
    original_env = dict(os.environ)

    def cleanup():
        """Restore the original environment."""
        os.environ.clear()
        os.environ.update(original_env)

    # Clear all existing environment variables
    os.environ.clear()
    # Set only the specified environment variables
    os.environ.update(env)

    return cleanup


@contextmanager
def function_environment(suffix: str, handler: str, func_dir: str):
    """
    Context manager for function environment handling.

    This ensures that:
    1. Only the specified environment variables are present
    2. All other environment variables are removed
    3. Environment is cleaned up after function execution
    4. Cleanup happens even if the function raises an exception
    5. Boto3 services are mocked
    6. Function is loaded within the environment context

    Args:
        suffix: A unique identifier for the function execution
        handler: The handler string in format "path.to.module.function_name"
        func_dir: The absolute path to the function directory

    Yields:
        The loaded function ready to be executed
    """
    cleanup = None

    try:
        # Set up the environment
        env = get_env_for_function(suffix, func_dir)
        cleanup = override_env_for_invocation(env)

        # Load the function with our mock
        code_dir = get_code_dir(func_dir)
        func = load_handler_module(handler, code_dir)

        yield func
    finally:
        # Always clean up the environment
        if cleanup:
            cleanup()
