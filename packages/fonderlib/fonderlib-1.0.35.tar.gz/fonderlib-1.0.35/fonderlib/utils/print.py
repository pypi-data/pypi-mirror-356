def show_execution_results(logger, resume):
    logger.info("=== Execution resume ===")
    logger.info(f"Total tasks: {resume['total_count']}")
    logger.info(f"Total success tasks: {resume['success_count']}")
    logger.info(
        f"Total failed tasks: {resume['total_count'] - resume['success_count']}"
    )