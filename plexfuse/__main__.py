if len(__package__) == 0:
    import sys

    print(
        f"""

The '__main__' module does not seem to have been run in the context of a
runnable package ... did you forget to add the '-m' flag?

Usage: {sys.executable} -m plexfuse {' '.join(sys.argv[1:])}

"""
    )
    sys.exit(2)

from plexfuse.fs.main import main

main()
