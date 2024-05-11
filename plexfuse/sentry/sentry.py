def sentry(dsn: str):
    import sentry_sdk

    sentry_sdk.init(
        dsn=dsn,
    )
