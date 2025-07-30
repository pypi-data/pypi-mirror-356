"""
This file runs the immunization data pipeline.
"""

import logging
from collections.abc import Callable, Sequence
from pathlib import Path

import pandas as pd
import requests

from minnesota_immunization_core.aisr.actions import AISRActionFailedError
from minnesota_immunization_core.aisr.authenticate import AISRAuthResponse

logger = logging.getLogger(__name__)


class ETLExecutionFailureError(Exception):
    """Custom exception for ETL execution failures."""

    def __init__(self, message: str):
        super().__init__(message)


def run_etl(
    extract: Callable[[], pd.DataFrame],
    transform: Callable[[pd.DataFrame], pd.DataFrame],
    load: Callable[[pd.DataFrame], None],
) -> str:
    """
    Run the ETL data pipeline with functions passed in.

    Returns:
        str: A message stating the run succeeded or failed
    """
    logger.info("Starting ETL process.")

    df_in = extract()
    transformed_df = transform(df_in)
    load(transformed_df)

    logger.info("ETL process completed successfully.")
    return "Data pipeline executed successfully"


def run_etl_on_folder(
    input_folder: Path, output_folder: Path, etl_fn: Callable[[Path, Path], str]
):
    """
    Runs the ETL pipeline for all CSV files in the input folder (AISR downloads)
    and saves the results to the output folder.

    The input_folder should contain CSV files downloaded from AISR.
    """
    logger.info("Starting ETL on folder: %s", input_folder)

    output_folder.mkdir(parents=True, exist_ok=True)

    # Iterate over each CSV file in the input folder and run the ETL pipeline
    for input_file in input_folder.glob("*.csv"):
        logger.info("Processing file: %s", input_file)
        try:
            etl_fn(input_file, output_folder)
        except ETLExecutionFailureError:
            logger.error("ETL failed for file: %s", input_file, exc_info=True)

    logger.info("ETL on folder completed.")


def run_aisr_workflow(
    login: Callable[[requests.Session], AISRAuthResponse],
    aisr_actions: Sequence[Callable[..., None]],
    logout: Callable[[requests.Session], None],
) -> None:
    """
    Logs into MIIC, runs a series of actions, and logs out of MIIC.
    """
    with requests.Session() as session:
        aisr_response = login(session)

        for action in aisr_actions:
            try:
                action(session, aisr_response.access_token)
            except AISRActionFailedError as e:
                logger.error(
                    "Error occurred during %s: %s",
                    action.__name__,
                    e,
                )

        logout(session)

        logger.info("Completed AISR workflow")
