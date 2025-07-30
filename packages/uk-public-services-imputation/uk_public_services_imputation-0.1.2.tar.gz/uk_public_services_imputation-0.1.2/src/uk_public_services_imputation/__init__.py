import argparse
import logging
from uk_public_services_imputation.main import impute_public_services


def main() -> None:
    """Run the NHS consumption imputation."""
    parser = argparse.ArgumentParser(
        description="UK Public Services Imputation CLI"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Import here to avoid circular imports
    from uk_public_services_imputation.nhs.impute_nhs_consumption import (
        main as nhs_main,
    )

    # Run the NHS imputation
    nhs_main()

    from uk_public_services_imputation.etb.impute_services import (
        main as etb_main,
    )

    etb_main()
