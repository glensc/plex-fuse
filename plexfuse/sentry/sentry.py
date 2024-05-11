def sentry(dsn: str = None):
    if not dsn:
        return

    import sentry_sdk

    sentry_sdk.init(
        dsn=dsn,
    )
