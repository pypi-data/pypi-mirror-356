from typing import TypeVar, Optional
import warnings
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from crypticorn.hive import HiveClient
from crypticorn.klines import KlinesClient
from crypticorn.pay import PayClient

from crypticorn.trade import TradeClient
from crypticorn.metrics import MetricsClient
from crypticorn.auth import AuthClient
from crypticorn.common import (
    BaseUrl,
    ApiVersion,
    Service,
    apikey_header as aph,
    CrypticornDeprecatedSince217,
)
from importlib.metadata import version
from typing_extensions import deprecated

ConfigT = TypeVar("ConfigT")
SubClient = TypeVar("SubClient")


class BaseAsyncClient:
    """
    Base class for Crypticorn API clients containing shared functionality.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        jwt: Optional[str] = None,
        base_url: BaseUrl = BaseUrl.PROD,
        is_sync: bool = False,
        http_client: Optional[ClientSession] = None,
    ):
        """
        :param api_key: The API key to use for authentication (recommended).
        :param jwt: The JWT to use for authentication (not recommended).
        :param base_url: The base URL the client will use to connect to the API.
        :param is_sync: Whether this client should operate in synchronous mode.
        :param http_client: Optional aiohttp ClientSession to use for HTTP requests.
        """
        self._base_url = base_url
        self._api_key = api_key
        self._jwt = jwt
        self._is_sync = is_sync
        self._http_client = http_client
        self._owns_http_client = http_client is None  # whether we own the http client

        self._service_classes: dict[Service, type[SubClient]] = {
            Service.HIVE: HiveClient,
            Service.TRADE: TradeClient,
            Service.KLINES: KlinesClient,
            Service.PAY: PayClient,
            Service.METRICS: MetricsClient,
            Service.AUTH: AuthClient,
        }

        self._services: dict[Service, SubClient] = self._create_services()

    def _create_services(self) -> dict[Service, SubClient]:
        """Create services with the appropriate configuration based on sync/async mode."""
        services = {}
        for service, client_class in self._service_classes.items():
            config = self._get_default_config(service)
            # For sync clients, don't pass the persistent http_client
            # Let each operation manage its own session
            if self._is_sync:
                services[service] = client_class(
                    config, http_client=None, is_sync=self._is_sync
                )
            else:
                services[service] = client_class(
                    config, http_client=self._http_client, is_sync=self._is_sync
                )
        return services

    @property
    def base_url(self) -> BaseUrl:
        """
        The base URL the client will use to connect to the API.
        """
        return self._base_url

    @property
    def api_key(self) -> Optional[str]:
        """
        The API key the client will use to connect to the API.
        This is the preferred way to authenticate.
        """
        return self._api_key

    @property
    def jwt(self) -> Optional[str]:
        """
        The JWT the client will use to connect to the API.
        This is the not the preferred way to authenticate.
        """
        return self._jwt

    @property
    def version(self) -> str:
        """
        The version of the client.
        """
        return version("crypticorn")

    @property
    def is_sync(self) -> bool:
        """
        Whether this client operates in synchronous mode.
        """
        return self._is_sync

    @property
    def http_client(self) -> Optional[ClientSession]:
        """
        The HTTP client session being used, if any.
        """
        return self._http_client

    @property
    def hive(self) -> HiveClient:
        """
        Entry point for the Hive AI API ([Docs](https://docs.crypticorn.com/api/?api=hive-ai-api)).
        """
        return self._services[Service.HIVE]

    @property
    def trade(self) -> TradeClient:
        """
        Entry point for the Trading API ([Docs](https://docs.crypticorn.com/api/?api=trading-api)).
        """
        return self._services[Service.TRADE]

    @property
    def klines(self) -> KlinesClient:
        """
        Entry point for the Klines API ([Docs](https://docs.crypticorn.com/api/?api=klines-api)).
        """
        return self._services[Service.KLINES]

    @property
    def metrics(self) -> MetricsClient:
        """
        Entry point for the Metrics API ([Docs](https://docs.crypticorn.com/api/?api=metrics-api)).
        """
        return self._services[Service.METRICS]

    @property
    def pay(self) -> PayClient:
        """
        Entry point for the Payment API ([Docs](https://docs.crypticorn.com/api/?api=payment-api)).
        """
        return self._services[Service.PAY]

    @property
    def auth(self) -> AuthClient:
        """
        Entry point for the Auth API ([Docs](https://docs.crypticorn.com/api/?api=auth-api)).
        """
        return self._services[Service.AUTH]

    def configure(self, config: ConfigT, service: Service) -> None:
        """
        Update a sub-client's configuration by overriding with the values set in the new config.
        Useful for testing a specific service against a local server instead of the default proxy.

        :param config: The new configuration to use for the sub-client.
        :param service: The service to configure.

        Example:
        >>> # For async client
        >>> async with AsyncClient() as client:
        ...     client.configure(config=HiveConfig(host="http://localhost:8000"), service=Service.HIVE)
        >>>
        >>> # For sync client
        >>> with SyncClient() as client:
        ...     client.configure(config=HiveConfig(host="http://localhost:8000"), service=Service.HIVE)
        """
        assert Service.validate(service), f"Invalid service: {service}"
        client = self._services[service]
        new_config = client.config
        for attr in vars(config):
            new_value = getattr(config, attr)
            if new_value:
                setattr(new_config, attr, new_value)

        # Recreate service with new config and appropriate parameters
        if self._is_sync:
            self._services[service] = type(client)(
                new_config, is_sync=self._is_sync, http_client=self._http_client
            )
        else:
            self._services[service] = type(client)(
                new_config, http_client=self._http_client
            )

    def _get_default_config(self, service, version=None):
        if version is None:
            version = ApiVersion.V1
        config_class = self._service_classes[service].config_class
        return config_class(
            host=f"{self.base_url}/{version}/{service}",
            access_token=self.jwt,
            api_key={aph.scheme_name: self.api_key} if self.api_key else None,
        )

    async def close(self):
        """Close the client and clean up resources."""
        # close each service
        for service in self._services.values():
            if (
                hasattr(service, "base_client")
                and hasattr(service.base_client, "close")
                and self._owns_http_client
            ):
                await service.base_client.close()
        # close shared http client if we own it
        if self._http_client and self._owns_http_client:
            await self._http_client.close()
            self._http_client = None

    def _ensure_session(self) -> None:
        """
        Lazily create the shared HTTP client when first needed and pass it to all subclients.
        """
        if self._http_client is None:
            self._http_client = ClientSession(
                timeout=ClientTimeout(total=30.0),
                connector=TCPConnector(limit=100, limit_per_host=20),
                headers={"User-Agent": f"crypticorn/python/{self.version}"},
            )
            # Update services to use the new session
            self._services = self._create_services()


class AsyncClient(BaseAsyncClient):
    """
    The official async Python client for interacting with the Crypticorn API.
    It is consisting of multiple microservices covering the whole stack of the Crypticorn project.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        jwt: Optional[str] = None,
        base_url: BaseUrl = BaseUrl.PROD,
        *,
        http_client: Optional[ClientSession] = None,
    ):
        """
        :param api_key: The API key to use for authentication (recommended).
        :param jwt: The JWT to use for authentication (not recommended).
        :param base_url: The base URL the client will use to connect to the API.
        :param http_client: The HTTP client to use for the client.
        """
        # Initialize as async client
        super().__init__(api_key, jwt, base_url, is_sync=False, http_client=http_client)

    async def close(self):
        await super().close()

    async def __aenter__(self):
        self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


@deprecated("Use AsyncClient instead", category=None)
class ApiClient(AsyncClient):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "ApiClient is deprecated. Use AsyncClient instead.",
            CrypticornDeprecatedSince217,
        )
        super().__init__(*args, **kwargs)


class SyncClient(BaseAsyncClient):
    """
    The official synchronous Python client for interacting with the Crypticorn API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        jwt: Optional[str] = None,
        base_url: BaseUrl = BaseUrl.PROD,
        *,
        http_client: Optional[ClientSession] = None,
    ):
        """
        :param http_client: Optional aiohttp ClientSession to use for HTTP requests.
                          Note: For sync client, session management is handled automatically.
        """
        super().__init__(api_key, jwt, base_url, is_sync=True, http_client=http_client)

    def close(self):
        """Close the client and clean up resources."""
        # For sync client, don't maintain persistent sessions
        # Each operation creates its own session within async_to_sync
        self._http_client = None

    def _ensure_session(self) -> None:
        """
        For sync client, don't create persistent sessions.
        Let each async_to_sync call handle its own session.
        """
        # Don't create persistent sessions in sync mode
        # Each API call will handle session creation/cleanup within async_to_sync
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        """Automatic cleanup when the object is garbage collected."""
        try:
            self.close()
        except Exception:
            pass
