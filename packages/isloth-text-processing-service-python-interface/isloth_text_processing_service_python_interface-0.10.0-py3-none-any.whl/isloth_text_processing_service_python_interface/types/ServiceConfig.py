"""
ServiceConfig.py
----------------
Defines service connection configuration and builder for inter-service communication.
"""

from pydantic import BaseModel, Field
from isloth_python_common_lib.types.abstracts.BaseBuilder import BaseBuilder


class ServiceConfigModel(BaseModel):
    """
    Represents configuration for accessing another service.

    Attributes
    ----------
    protocol : str
        The network protocol, e.g., 'http' or 'https'.
    host : str
        The hostname or IP of the target service.
    port : int
        The port number the service listens on.
    version : str
        The API version to use when making requests.
    """
    protocol: str = Field(default='http', min_length=1)
    host: str = Field(default='localhost', min_length=1)
    port: int = Field(..., gt=0)
    version: str = Field(..., min_length=1)


class ServiceConfigBuilder(BaseBuilder[ServiceConfigModel]):
    """
    Builder class for constructing ServiceConfigModel instances.
    """

    def __init__(self) -> None:
        super().__init__(ServiceConfigModel)

    def set_protocol(self, protocol: str) -> 'ServiceConfigBuilder':
        """
        Sets the protocol (e.g., 'http').

        Parameters
        ----------
        protocol : str
            The protocol to use.

        Returns
        -------
        ServiceConfigBuilder
            The current builder instance.
        """
        self.data['protocol'] = protocol
        return self

    def set_host(self, host: str) -> 'ServiceConfigBuilder':
        """
        Sets the host address.

        Parameters
        ----------
        host : str
            Hostname or IP address.

        Returns
        -------
        ServiceConfigBuilder
            The current builder instance.
        """
        self.data['host'] = host
        return self

    def set_port(self, port: int) -> 'ServiceConfigBuilder':
        """
        Sets the port number.

        Parameters
        ----------
        port : int
            Port to connect to.

        Returns
        -------
        ServiceConfigBuilder
            The current builder instance.
        """
        self.data['port'] = port
        return self

    def set_version(self, version: str) -> 'ServiceConfigBuilder':
        """
        Sets the API version string.

        Parameters
        ----------
        version : str
            Version identifier.

        Returns
        -------
        ServiceConfigBuilder
            The current builder instance.
        """
        self.data['version'] = version
        return self
