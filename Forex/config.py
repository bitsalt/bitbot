import os
import sys
import v20
import yaml

DEFAULT_ENV = "bitbot"
DEFAULT_PATH = "../.account.conf"


class ConfigPathError(Exception):
    """
    Exception to catch when the account.conf file is not found.
    """
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'Config file {self.path} cannot be loaded.'


class ConfigValueError(Exception):
    """
    Exception to catch when the config file is missing a required value.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'Config file is missing value for {self.value}'


class Config(object):
    """
    The Config object encapsulates all of the configuration required to create
    a v20 API context and configure it to work with a specific Account.

    Using the Config object enables the scripts to exist without many command
    line arguments (host, token, accountID, etc)
    """
    def __init__(self):
        """
        Initialize an empty Config object
        """
        self.hostname = None
        self.streaming_hostname = None
        self.port = 443
        self.ssl = True
        self.token = None
        self.username = None
        self.accounts = []
        self.active_account = None
        self.path = None
        self.datetime_format = "RFC3339"

    def __str__(self):
        """
        Create the string (YAML) representation of the Config instance
        """

        s = ""
        s += "hostname: {}\n".format(self.hostname)
        s += "streaming_hostname: {}\n".format(self.streaming_hostname)
        s += "port: {}\n".format(self.port)
        s += "ssl: {}\n".format(str(self.ssl).lower())
        s += "token: {}\n".format(self.token)
        s += "username: {}\n".format(self.username)
        s += "datetime_format: {}\n".format(self.datetime_format)
        s += "accounts:\n"
        for a in self.accounts:
            s += "- {}\n".format(a)
        s += "active_account: {}".format(self.active_account)

        return s

    def dump(self, path):
        """
        Dump the YAML representation of the Config instance to a file.

        Args:
            path: The location to write the config YAML
        """

        path = os.path.expanduser(path)

        with open(path, "w") as f:
            print(str(self), file=f)

    def load(self, path):
        """
        Load the YAML config representation from a file into the Config
        instance

        Args:
            path: The location to read the config YAML from
        """

        self.path = path

        try:
            with open(os.path.expanduser(path)) as f:
                y = yaml.load(f, Loader=yaml.FullLoader)
                self.hostname = y.get("hostname", self.hostname)
                self.streaming_hostname = y.get(
                    "streaming_hostname", self.streaming_hostname
                )
                self.port = y.get("port", self.port)
                self.ssl = y.get("ssl", self.ssl)
                self.username = y.get("username", self.username)
                self.token = y.get("token", self.token)
                self.accounts = y.get("accounts", self.accounts)
                self.active_account = y.get(
                    "active_account", self.active_account
                )
                self.datetime_format = y.get(
                    "datetime_format", self.datetime_format
                )
        except Exception:
            raise ConfigPathError(path)

    def validate(self):
        """
        Ensure that the Config instance is valid
        """

        if self.hostname is None:
            raise ConfigValueError("hostname")
        if self.streaming_hostname is None:
            raise ConfigValueError("hostname")
        if self.port is None:
            raise ConfigValueError("port")
        if self.ssl is None:
            raise ConfigValueError("ssl")
        if self.username is None:
            raise ConfigValueError("username")
        if self.token is None:
            raise ConfigValueError("token")
        if self.accounts is None:
            raise ConfigValueError("account")
        if self.active_account is None:
            raise ConfigValueError("account")
        if self.datetime_format is None:
            raise ConfigValueError("datetime_format")

    def update_from_input(self):
        """
        Populate the configuration instance by interacting with the user using
        prompts
        """

        environments = [
            "fxtrade",
            "fxpractice"
        ]

        hostnames = [
            "api-fxtrade.oanda.com",
            "api-fxpractice.oanda.com"
        ]

        streaming_hostnames = [
            "stream-fxtrade.oanda.com",
            "stream-fxpractice.oanda.com"
        ]

        index = 0

        try:
            index = hostnames.index(self.hostname)
        except Exception:
            pass

        environment = input.get_from_list(
            environments,
            "Available environments:",
            "Select environment",
            index
        )

        index = environments.index(environment)

        self.hostname = hostnames[index]
        self.streaming_hostname = streaming_hostnames[index]

        print("> API host selected is: {}".format(self.hostname))
        print(
            "> Streaming host selected is: {}".format(self.streaming_hostname)
        )
        print("")

        self.username = input.get_string("Enter username", self.username)

        print("> username is: {}".format(self.username))
        print("")

        self.token = input.get_string(
            "Enter personal access token", self.token
        )

        print("> Using personal access token: {}".format(self.token))

        ctx = v20.Context(
            self.hostname,
            self.port,
            self.ssl
        )

        ctx.set_token(self.token)

        ctx_streaming = v20.Context(
            self.streaming_hostname,
            self.port,
            self.ssl
        )

        ctx_streaming.set_token(self.token)

        response = ctx.account.list()

        if response.status != 200:
            print(response)
            sys.exit()

        self.accounts = [
            account.id for account in response.body.get("accounts")
        ]

        self.accounts.sort()

        if len(self.accounts) == 0:
            print("No Accounts available")
            sys.exit()

        index = 0

        try:
            index = self.accounts.index(self.active_account)
        except Exception:
            pass

        print("")

        self.active_account = input.get_from_list(
            self.accounts,
            "Available Accounts:",
            "Select Active Account",
            index
        )

        print("> Active Account is: {}".format(self.active_account))
        print("")

        time_formats = ["RFC3339", "UNIX"]

        index = 0

        try:
            index = time_formats.index(self.datetime_format)
        except Exception:
            pass

        self.datetime_format = input.get_from_list(
            time_formats,
            "Available Time Formats:",
            "Select Time Format",
            index
        )

    def create_context(self):
        """
        Initialize an API context based on the Config instance
        """
        ctx = v20.Context(
            self.hostname,
            self.port,
            self.ssl,
            application="sample_code",
            token=self.token,
            datetime_format=self.datetime_format
        )

        return ctx

    def create_streaming_context(self):
        """
        Initialize a streaming API context based on the Config instance
        """
        ctx = v20.Context(
            self.streaming_hostname,
            self.port,
            self.ssl,
            application="sample_code",
            token=self.token,
            datetime_format=self.datetime_format
        )

        return ctx


def make_config_instance(path=None):
    """
    Create a config instance, load its state from the given path, and
    validate it.
    """
    if not path:
        path = default_config_path()

    config = Config()
    config.load(path)
    config.validate()
    return config

def default_config_path():
    """
    Determine the default configuration file path and set it as an environment variable.
    """
    global DEFAULT_PATH
    global DEFAULT_ENV

    os.environ.setdefault('DEFAULT_ENV', DEFAULT_ENV)
    os.environ.setdefault('DEFAULT_PATH', DEFAULT_PATH)
    return os.environ.get('DEFAULT_PATH')

