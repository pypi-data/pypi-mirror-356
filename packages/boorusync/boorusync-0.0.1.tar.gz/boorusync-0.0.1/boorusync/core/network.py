from aiohttp import ClientSession, ClientTimeout, TCPConnector
from typing import (
    Dict,
    Callable,
    Coroutine,
    Literal,
    TypedDict,
    Optional,
    Union,
    Any,
    List,
    Tuple,
    AsyncGenerator,
)
from asyncio import sleep, iscoroutinefunction
from time import time
from os import path, makedirs
from pathlib import Path
import logging
import json
import asyncio
from collections import deque
from aiofiles import open as aopen
from .config import Config

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class Response:
    """Wrapper for HTTP responses"""

    def __init__(
        self,
        status: int = None,
        headers: Dict = None,
        text: str = None,
        json: Any = None,
    ):
        self.status = status
        self.headers = headers or {}
        self._text = text
        self._json = json
        self.url = None
        self.method = None
        self.request_info = None

    def __repr__(self) -> str:
        return f"<Response [status={self.status}, size={len(self._text) if self._text else 0}]>"

    def __str__(self) -> str:
        return self._text if self._json is None else str(self._json)

    async def text(self) -> str:
        """Return response body as text"""
        return self._text or ""

    async def json(self) -> Any:
        """Try to return response body as JSON"""
        if self._json is not None:
            return self._json
        if not self._text:
            return None
        try:
            return json.loads(self._text)
        except Exception:
            return None

    def raise_for_status(self):
        """Raise an exception if the status is 4xx or 5xx."""
        if 400 <= self.status < 600:
            raise Exception(f"HTTP Error {self.status}: {self._text}")

    @classmethod
    def ensure_response(cls, obj):
        """Ensure the object is a Response instance."""
        if isinstance(obj, cls):
            return obj
        elif isinstance(obj, dict):
            return cls(json=obj)
        elif isinstance(obj, str):
            return cls(text=obj)
        return cls(text=str(obj))


class DownloadStatus:
    """Class to track download status."""

    def __init__(self):
        self.downloaded_size = 0
        self.total_size = 0
        self.start_at = 0
        self.time_passed = 0
        self.file_path = ""
        self.filename = ""
        self.download_speed = 0
        self.eta = 0
        self.completed = False


class DownloadOptions(TypedDict, total=False):
    """Type definition for download options."""

    url: str
    folder_path: str
    filename: Optional[str]
    status_callback: Optional[Union[Callable, Coroutine]]
    done_callback: Optional[Union[Callable, Coroutine]]
    status_parent: Optional[Union[Dict, DownloadStatus]]
    headers: Optional[Dict[str, str]]
    timeout: Optional[int]
    callback_rate: Optional[float]
    proxy: Optional[str]
    max_speed: Optional[int]
    close: Optional[bool]
    retry_count: Optional[int]


class HttpClient:
    """HTTP client for making requests and downloading files."""

    def __init__(
        self,
        base_url: str = None,
        headers: Dict[str, str] = None,
        timeout: int = None,
        proxy: str = None,
        verify_ssl: bool = True,
        session: ClientSession = None,
        debug: bool = False,
        config: Config = None,
    ):
        """Initialize the HTTP client with configurable options."""
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout or config.get_as_number("default_timeout", section="network")
        self.debug = debug
        self.proxy = proxy
        self.verify_ssl = verify_ssl
        self.session = session
        self.config = config or Config()
        self.max_concurrent_requests = config.get_as_number("max_concurrent_requests", section="network")
        proxy_detection_enabled = self.config.get("enable_proxy_detection", True, section="network")
        if not proxy and proxy_detection_enabled:
            self.proxy = self.config.get_effective_proxy(base_url)
        else:
            self.proxy = proxy

        # Set logger level based on debug flag
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

    async def _ensure_session(self, headers: Optional[Dict[str, str]] = None) -> ClientSession:
        """Ensure there's an active session or create a new one."""
        session = self.session
        session_headers = headers if headers is not None else self.headers
        if not session or session.closed:
            # Create new session with merged headers only when needed
            connector = TCPConnector(ssl=self.verify_ssl)
            self.session = ClientSession(headers=session_headers, connector=connector)
        elif headers:
            self.session.headers.update(session_headers)
        return self.session

    async def request(
        self,
        url: str,
        method: Literal["get", "post"] = "get",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        proxy: Optional[str] = None,
        retries: int = 0,
        max_retries: int = 3,
        close: bool = True,
        **kwargs: Any,
    ) -> Response:
        """Make an HTTP request with support for retries."""
        if retries > max_retries:
            raise Exception(f"Maximum retry count ({max_retries}) exceeded")

        full_url = url if url.startswith("http") else f"{self.base_url or ''}{url}"
        request_timeout = ClientTimeout(total=timeout or self.timeout)
        request_headers = headers or self.headers
        # Use config's proxy auto-detection logic
        request_proxy = self.config.get_effective_proxy(full_url, proxy)

        logger.debug(f"Request: {method.upper()} {full_url}, retries: {retries}/{max_retries}")
        response_obj = Response()
        response_obj.method = method.upper()
        response_obj.url = full_url

        try:
            session = await self._ensure_session(request_headers)
            session_method = session.get if method == "get" else session.post
            session_kwargs = {
                "timeout": request_timeout,
                "ssl": self.verify_ssl,
                "proxy": request_proxy,
                **kwargs,
            }
            if method == "get":
                session_kwargs["params"] = params
            else:
                session_kwargs["json"] = data or kwargs.pop("json", None)

            async with session_method(full_url, **session_kwargs) as response:
                response_obj.status = response.status
                response_obj.headers = dict(response.headers)
                response_obj._text = await response.text()
                try:
                    response_obj._json = await response.json()
                except json.JSONDecodeError:
                    response_obj._json = None

                if response.status == 429:
                    retry_delay = float(response.headers.get("Retry-After", 1.0))
                    logger.debug(f"Rate limited, retrying after {retry_delay}s")
                    await sleep(retry_delay)
                    return await self.request(
                        url,
                        method,
                        params,
                        data,
                        headers,
                        timeout,
                        proxy,
                        retries + 1,
                        max_retries,
                        close,
                        **kwargs,
                    )
                if response.status >= 400:
                    response_obj.raise_for_status()

        except Exception as e:
            logger.debug(f"Request error: {str(e)}")
            if retries < max_retries:
                await sleep(1.0)
                return await self.request(
                    url,
                    method,
                    params,
                    data,
                    headers,
                    timeout,
                    proxy,
                    retries + 1,
                    max_retries,
                    close,
                    **kwargs,
                )
            raise

        finally:
            if close and session and not session.closed:
                await session.close()

        return response_obj

    async def get(
        self,
        url: str,
        params: Dict = None,
        headers: Dict[str, str] = None,
        timeout: int = None,
        **kwargs,
    ) -> Response:
        """Make a GET request and return Response object."""
        return await self.request(url, method="get", params=params, headers=headers, timeout=timeout, **kwargs)

    async def post(
        self,
        url: str,
        data: Dict = None,
        headers: Dict[str, str] = None,
        timeout: int = None,
        **kwargs,
    ) -> Response:
        """Make a POST request and return Response object."""
        return await self.request(url, method="post", data=data, headers=headers, timeout=timeout, **kwargs)

    async def bulk_request_generator(
        self,
        urls: List[Union[str, Dict[str, str]]],
        method: Literal["get", "post"] = "get",
        close: bool = True,
        **kwargs: Any,
    ) -> AsyncGenerator[Response, None]:
        """Make concurrent requests to multiple URLs and yield responses as they come in."""
        if not urls:
            return

        logger.debug(f"Performing bulk {method.upper()} request to {len(urls)} URLs")

        # Store tasks to ensure proper cancellation
        tasks = []

        try:
            # Ensure session exists but don't close it in the request method
            session = await self._ensure_session()

            # Define helper that returns as soon as a successful response is found
            async def safe_request(
                url_data: Union[str, Dict[str, str]],
            ) -> Tuple[bool, Response]:
                try:
                    # Process URL and credentials
                    url = url_data if isinstance(url_data, str) else url_data.get("url")

                    # Check if we should use proxy for this URL
                    request_kwargs = kwargs.copy()
                    if "proxy" not in request_kwargs:
                        request_kwargs["proxy"] = self.proxy

                    # Don't close the session in individual requests
                    response = await self.request(url, method=method, close=False, **request_kwargs)

                    # Consider 2xx and 3xx status codes as successful
                    if response.status < 400:
                        logger.debug(f"Request to {url} succeeded with status {response.status}")
                        return True, response
                    else:
                        logger.debug(f"Request to {url} failed with status {response.status}")
                        return False, response
                except Exception as e:
                    logger.debug(f"Request to {url} failed with error: {str(e)}")
                    # Create an error response
                    return False, Response(status=0, text=f"Error: {str(e)}")

            # Create tasks for all URLs
            tasks = [asyncio.create_task(safe_request(url)) for url in urls]

            # Use as_completed to get results as they finish
            for future in asyncio.as_completed(tasks):
                success, response = await future
                # Yield each response as it becomes available
                yield response

        except Exception as e:
            logger.debug(f"Bulk request error: {str(e)}")
            # Yield a generic error response
            yield Response(status=0, text=f"Bulk request error: {str(e)}")

        finally:
            # Cancel any remaining tasks that might still be running
            for task in tasks:
                if not task.done():
                    task.cancel()

            # Don't close the session here if close=False was specified
            if close:
                if session and not session.closed:
                    logger.debug("Closing session after bulk request")
                    await session.close()

    async def bulk_request(
        self,
        urls: List[Union[str, Dict[str, str]]],
        method: Literal["get", "post"] = "get",
        **kwargs: Any,
    ) -> Response:
        """Make concurrent requests to multiple URLs and return the first successful response."""
        # Get the generator
        generator = self.bulk_request_generator(urls, method, **kwargs)

        first_error = None
        # Return the first response from the generator
        async for response in generator:
            if response.status < 400 and response.status > 0:
                return response
            # Store the first error response to return if all fail
            if first_error is None:
                first_error = response

        # If we got here, no successful responses were found, return the first error
        return first_error or Response(status=0, text="All requests failed")

    async def bulk_get(
        self,
        urls: List[Union[str, Dict[str, str]]],
        params: Dict = None,
        headers: Dict[str, str] = None,
        timeout: int = None,
        **kwargs,
    ) -> Response:
        """Make concurrent GET requests to multiple URLs and return the first successful response."""
        return await self.bulk_request(
            urls,
            method="get",
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    async def bulk_post(
        self,
        urls: List[Union[str, Dict[str, str]]],
        data: Dict = None,
        headers: Dict[str, str] = None,
        timeout: int = None,
        **kwargs,
    ) -> Response:
        """Make concurrent POST requests to multiple URLs and return the first successful response."""
        return await self.bulk_request(urls, method="post", data=data, headers=headers, timeout=timeout, **kwargs)

    async def download_file(
        self,
        url: str,
        folder_path: str,
        filename: Optional[str] = None,
        status_callback: Optional[Union[Callable[..., None], Coroutine[Any, Any, None]]] = None,
        done_callback: Optional[Union[Callable[..., None], Coroutine[Any, Any, None]]] = None,
        status_parent: Optional[Union[Dict[str, Any], DownloadStatus]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 60,
        callback_rate: float = 0.5,
        proxy: Optional[str] = None,
        max_speed: Optional[int] = None,
        close: bool = True,
        retry_count: int = 3,
    ) -> Path:
        """Download a file with progress tracking."""
        if not url:
            raise ValueError("URL is required for downloading files")

        # Generate download ID for tracking
        # download_id = str(uuid.uuid4())

        # Debug logging
        logger.debug(f"Starting download from: {url}")

        if not path.exists(folder_path):
            logger.debug(f"Creating folder: {folder_path}")
            makedirs(folder_path, exist_ok=True)

        # Cache callback options
        request_headers = headers or self.headers
        request_proxy = proxy or self.proxy
        request_timeout = ClientTimeout(total=timeout or self.timeout)

        # Initialize tracking variables
        start_time = time()
        downloaded_size = 0
        download_speed = 0
        last_callback_time = start_time
        last_size = 0
        iteration = 0

        # Prepare session (reuse session for better performance)
        session = await self._ensure_session(request_headers)

        try:
            # Add retry loop for download
            for retry_attempt in range(retry_count + 1):
                if retry_attempt > 0:
                    logger.debug(f"Retry attempt {retry_attempt}/{retry_count} for download: {url}")
                    await sleep(1.0 * retry_attempt)

                try:
                    download_kwargs = {"ssl": self.verify_ssl}
                    if request_proxy:
                        download_kwargs["proxy"] = request_proxy

                    async with session.get(url, timeout=request_timeout, **download_kwargs) as response:
                        if response.status >= 400:
                            error_msg = f"Failed to download file, status code: {response.status}"
                            logger.debug(error_msg)

                            # Only retry on certain error codes
                            if response.status in (429, 500, 502, 503, 504) and retry_attempt < retry_count:
                                continue
                            raise Exception(error_msg)

                        total_size = int(response.headers.get("Content-Length", -1))
                        logger.debug(f"Content-Length: {total_size} bytes")

                        # Determine filename
                        if not filename:
                            content_disposition = response.headers.get("Content-Disposition", "")
                            if 'filename="' in content_disposition:
                                filename = content_disposition.split('filename="')[1].split('"')[0]
                            else:
                                filename = url.split("/")[-1].split("?")[0]

                        file_path = path.join(folder_path, filename)
                        logger.debug(f"Downloading to: {file_path}")

                        # Download the file with buffer handling
                        buffer_size = 1024 * 1024  # 1MB buffer

                        async with aopen(file_path, "wb") as f:
                            logger.debug("Download started")
                            while True:
                                try:
                                    # Use read() with a timeout to prevent hanging
                                    chunk = await asyncio.wait_for(
                                        response.content.read(buffer_size),
                                        timeout=30,  # Timeout for individual chunk reads
                                    )

                                    if not chunk:
                                        logger.debug("End of stream reached")
                                        break

                                    # Write chunk to file
                                    await f.write(chunk)
                                    chunk_size = len(chunk)
                                    downloaded_size += chunk_size

                                    # Update progress if needed
                                    current_time = time()
                                    time_since_callback = current_time - last_callback_time

                                    if time_since_callback >= callback_rate:
                                        # Calculate download stats
                                        if time_since_callback > 0:
                                            download_speed = (downloaded_size - last_size) / time_since_callback
                                        else:
                                            download_speed = 0

                                        eta = (
                                            (total_size - downloaded_size) / download_speed if download_speed > 0 and total_size > 0 else 0
                                        )
                                        time_passed = current_time - start_time

                                        # Debug logging for download progress
                                        percent = (downloaded_size / total_size * 100) if total_size > 0 else 0
                                        logger.debug(
                                            f"Downloaded: {downloaded_size / 1024 / 1024:.2f}MB / "
                                            f"{total_size / 1024 / 1024:.2f}MB ({percent:.1f}%) at "
                                            f"{download_speed / 1024 / 1024:.2f}MB/s, ETA: {eta:.0f}s"
                                        )

                                        # Create progress data
                                        progress_data = {
                                            "downloaded_size": downloaded_size,
                                            "start_at": start_time,
                                            "time_passed": round(time_passed, 2),
                                            "file_path": file_path,
                                            "filename": filename,
                                            "download_speed": download_speed,
                                            "total_size": total_size,
                                            "iteration": iteration,
                                            "eta": round(eta),
                                        }

                                        # Process callbacks and status updates
                                        await self._process_download_callbacks(
                                            status_callback,
                                            status_parent,
                                            progress_data,
                                        )

                                        # Update tracking variables
                                        last_callback_time = current_time
                                        last_size = downloaded_size
                                        iteration += 1

                                    # Limit download speed if requested
                                    if max_speed and download_speed > max_speed:
                                        sleep_time = chunk_size / max_speed
                                        logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                                        await sleep(sleep_time)

                                except asyncio.TimeoutError:
                                    logger.debug(f"Timeout while reading chunk after downloading {downloaded_size / 1024 / 1024:.2f}MB")
                                    # If we've downloaded a significant portion, try to continue
                                    if downloaded_size > buffer_size * 5:
                                        logger.debug("Continuing download despite chunk timeout")
                                        await sleep(0.5)
                                        continue
                                    # Otherwise, retry the whole download
                                    if retry_attempt < retry_count:
                                        break  # Break out of chunk reading loop to retry full download
                                    else:
                                        raise Exception("Download timed out after multiple retries")

                    # If we reached here, the download was successful
                    # Process completion
                    if status_parent or done_callback:
                        completion_time = time()
                        time_passed = round(completion_time - start_time, 2)
                        logger.debug(f"Download completed in {time_passed}s")

                        # Update status parent if provided
                        if status_parent:
                            completed_data = {
                                "downloaded_size": downloaded_size,
                                "total_size": total_size,
                                "completed": True,
                                "time_passed": time_passed,
                            }

                            if isinstance(status_parent, dict):
                                status_parent.update(completed_data)
                            elif hasattr(status_parent, "__dict__"):
                                for key, value in completed_data.items():
                                    setattr(status_parent, key, value)

                        # Call completion callback if provided
                        if done_callback:
                            done_data = {
                                "downloaded_size": downloaded_size,
                                "start_at": start_time,
                                "time_passed": time_passed,
                                "file_path": file_path,
                                "filename": filename,
                                "total_size": path.getsize(file_path),
                            }

                            if iscoroutinefunction(done_callback):
                                await done_callback(**done_data)
                            else:
                                done_callback(**done_data)

                    # If successful, break out of the retry loop
                    break

                except (asyncio.TimeoutError, ConnectionError) as e:
                    # Only retry on timeouts and connection errors
                    if retry_attempt < retry_count:
                        logger.debug(f"Download error (attempt {retry_attempt + 1}/{retry_count + 1}): {str(e)}")
                    else:
                        logger.error(f"Download failed after {retry_count + 1} attempts: {str(e)}")
                        raise

        except Exception as e:
            logger.debug(f"Download error: {str(e)}")
            raise
        finally:
            if close:
                logger.debug("Closing session")
                await session.close()

        return Path(file_path)

    async def _process_download_callbacks(self, status_callback, status_parent, progress_data):
        """Helper method to process download callbacks and status updates."""
        # Call status callback if provided
        if status_callback:
            if iscoroutinefunction(status_callback):
                await status_callback(**progress_data)
            else:
                status_callback(**progress_data)

        # Update status parent if provided
        if status_parent:
            if isinstance(status_parent, dict):
                status_parent.update(progress_data)
            elif hasattr(status_parent, "__dict__"):
                for key, value in progress_data.items():
                    setattr(status_parent, key, value)
            else:
                raise TypeError("status_parent must be a dict or an object with attributes")

    async def bulk_download(
        self,
        urls: List[Union[str, Dict[str, str]]],
        folder_path: str,
        max_concurrent: Optional[int] = None,
        **options: Any,
    ) -> List[Tuple[str, Optional[Path], Optional[Exception]]]:
        """Download multiple files concurrently with a limit on maximum parallel downloads."""
        results = []
        url_queue = deque(urls)
        active_tasks = set()

        async def download_task(url_data: Union[str, Dict[str, str]], options: Dict) -> Tuple[str, Optional[Path], Optional[Exception]]:
            try:
                file_path = await self.download_file(**options)
                return options["url"], file_path, None
            except Exception as e:
                return options["url"], None, e

        while url_queue or active_tasks:
            while len(active_tasks) < max_concurrent and url_queue:
                url_data = url_queue.popleft()
                options["url"] = url_data if isinstance(url_data, str) else url_data["url"]
                options["folder_path"] = folder_path
                task = asyncio.create_task(download_task(url_data, options))
                active_tasks.add(task)
                task.add_done_callback(active_tasks.discard)

            if active_tasks:
                done, _ = await asyncio.wait(active_tasks, timeout=0.1)
                for task in done:
                    results.append(task.result())

        return results

    async def detached_download(
        self,
        url: str,
        folder_path: str,
        filename: Optional[str] = None,
        status_callback: Optional[Union[Callable[..., None], Coroutine[Any, Any, None]]] = None,
        done_callback: Optional[Union[Callable[..., None], Coroutine[Any, Any, None]]] = None,
        status_parent: Optional[Union[Dict[str, Any], DownloadStatus]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 60,
        callback_rate: float = 0.5,
        proxy: Optional[str] = None,
        max_speed: Optional[int] = None,
        close: bool = True,
        retry_count: int = 3,
    ) -> asyncio.Task:
        """
        Start a file download in a detached task that runs in the background.

        Args:
            url: URL to download
            folder_path: Destination folder for the download
            filename: Optional filename for the downloaded file
            status_callback: Optional callback for download progress
            done_callback: Optional callback for download completion
            status_parent: Optional object to update with download status
            headers: Optional request headers
            timeout: Timeout for the download
            callback_rate: Rate at which progress callbacks are invoked
            proxy: Optional proxy for the download
            max_speed: Optional maximum download speed
            close: Whether to close the session after the download
            retry_count: Number of retries for the download

        Returns:
            asyncio.Task: The task handling the download, which can be awaited or monitored
        """
        # Create a task for the download
        download_task = asyncio.create_task(
            self.download_file(
                url=url,
                folder_path=folder_path,
                filename=filename,
                status_callback=status_callback,
                done_callback=done_callback,
                status_parent=status_parent,
                headers=headers,
                timeout=timeout,
                callback_rate=callback_rate,
                proxy=proxy,
                max_speed=max_speed,
                close=close,
                retry_count=retry_count,
            )
        )

        # Add name to the task for better debugging
        task_name = f"DetachedDownload_{filename or url.split('/')[-1][:30]}"
        download_task.set_name(task_name)

        logger.debug(f"Started detached download task: {task_name}")
        return download_task

    async def __aenter__(self):
        """Async context manager entry point."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting context."""
        await self.close()

    def __del__(self):
        """Ensure session is closed when the object is deleted."""
        if self.session and not self.session.closed:
            asyncio.run(self.close())
            logger.debug("Session closed on object deletion")

    async def close(self) -> None:
        """Close the HTTP client session."""
        if self.session and not self.session.closed:
            await self.session.close()
            logger.debug("Session closed explicitly")
