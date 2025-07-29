import sys
import logging
import _jprint


class JavaOut:
    """
    Redirects Python's sys.stdout to Java's System.out.println
    """

    def write(self, text, *args, **kwargs):
        _jprint.write(text)

    def flush(self):
        pass


class JavaErr:
    """
    Redirects Python's sys.stderr to Java's System.out.println
    """

    def write(self, text, *args, **kwargs):
        _jprint.write(text)

    def flush(self):
        pass


sys.stdout = JavaOut()
sys.stderr = JavaErr()

# logging.getLogger().info = sys.stdout.write
# logging.getLogger().error = sys.stderr.write
