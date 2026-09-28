import sys
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from extract import extract
from transform import transform
from load import get_engine, create_schema, load
from quality_check import check_missing, check_percentage_range

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("Pipeline dimulai")

    raw_df = extract()
    logger.info(f"Extract selesai: {len(raw_df)} baris")

    dim_country, fact_energy_yearly = transform(raw_df)
    logger.info(f"Transform selesai: dim_country={len(dim_country)}, fact_energy_yearly={len(fact_energy_yearly)}")

    check_missing(dim_country, "dim_country")
    check_missing(fact_energy_yearly, "fact_energy_yearly")

    engine = get_engine()
    create_schema(engine)
    load(dim_country, fact_energy_yearly, engine)
    logger.info("Load selesai, pipeline sukses")


if __name__ == "__main__":
    run_pipeline()