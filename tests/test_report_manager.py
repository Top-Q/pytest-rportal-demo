def test_report_manager(report):
    report.debug("This is a debug message")
    report.info("This is an info message")
    report.trace("This is a trace message")
    report.error("This is an error message")
