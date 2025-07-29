import subprocess

from srunx.logging import get_logger
from srunx.models import BaseJob, JobStatus

logger = get_logger(__name__)


def get_job_status(job_id: int) -> BaseJob:
    """Get job status and information.

    Args:
        job_id: SLURM job ID.

    Returns:
        Job object with current status.

    Raises:
        subprocess.CalledProcessError: If status query fails.
        ValueError: If job information cannot be parsed.
    """
    logger.debug(f"Querying status for job {job_id}")

    try:
        result = subprocess.run(
            [
                "sacct",
                "-j",
                str(job_id),
                "--format",
                "JobID,JobName,State",
                "--noheader",
                "--parsable2",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to query job {job_id} status: {e}")
        raise

    lines = result.stdout.strip().split("\n")
    if not lines or not lines[0]:
        error_msg = f"No job information found for job {job_id}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Parse the first line (main job entry)
    job_data = lines[0].split("|")
    if len(job_data) < 3:
        error_msg = f"Cannot parse job data for job {job_id}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    job_id_str, job_name, status_str = job_data[:3]
    logger.debug(f"Job {job_id} status: {status_str}")

    # Create job object with available information
    job = BaseJob(
        name=job_name,
        job_id=int(job_id_str),
        status=JobStatus(status_str),
    )

    return job
