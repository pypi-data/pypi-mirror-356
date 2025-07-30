class CopadoError(RuntimeError):
    """Base SDK error."""


class HTTPError(CopadoError):
    """Non‑2xx response."""


class FileUploadError(CopadoError):
    """File upload / download failed."""