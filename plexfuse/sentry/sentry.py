sdk = None


def sentry(dsn: str = None):
    if not dsn:
        return

    try:
        import sentry_sdk
    except ImportError:
        print("Unable to init sentry: sentry_sdk package not installed")
        return

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
