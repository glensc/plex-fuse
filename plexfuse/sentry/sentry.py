sdk = None


def sentry(dsn: str = None):
    if not dsn:
        return

    import sentry_sdk

    sentry_sdk.init(
        dsn=dsn,
    )

    # this is a pointer to the module object instance itself.
    import sys
    module = sys.modules[__name__]
    module.sdk = sentry_sdk


def capture_message(*args, **kwargs):
    if sdk:
        sdk.capture_message(*args, **kwargs)


def capture_exception(*args, **kwargs):
    if sdk:
        sdk.capture_exception(*args, **kwargs)
