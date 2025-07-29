# Copyright (c) Meta Platforms, Inc. and affiliates.
# SPDX-License-Identifier: LGPL-2.1-or-later

import json
import os
from pathlib import Path
import typing
from typing import Any, Dict, Mapping, Optional, Union
import urllib.error
import urllib.parse
import urllib.request

if typing.TYPE_CHECKING:
    import aiohttp


_CACHE = Optional[Union[str, bytes, Path]]


# Hacky base class because we want the GitHub API from async and non-async
# code.
#
# This provides a slapdash interface for caching a response in a file so that
# we can do conditional requests
# (https://docs.github.com/en/rest/overview/resources-in-the-rest-api#conditional-requests).
# A more complete implementation would be something like a SQLite database
# indexed by endpoint, but this is simpler and good enough for now.
class _GitHubApiBase:
    _HOST = "https://api.github.com"

    def __init__(self, token: Optional[str]) -> None:
        self._headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "osandov/drgn vmtest",
        }
        if token is not None:
            self._headers["Authorization"] = "token " + token

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
    ) -> Any:
        raise NotImplementedError()

    def _cached_get_json(self, endpoint: str, cache: _CACHE) -> Any:
        raise NotImplementedError()

    def _read_cache(self, cache: _CACHE) -> Optional[Mapping[str, Any]]:
        if not cache:
            return None
        try:
            with open(cache, "r") as f:
                return json.load(f)  # type: ignore[no-any-return]
        except FileNotFoundError:
            return None

    def _cached_get_headers(
        self, cached: Optional[Mapping[str, Any]]
    ) -> Dict[str, str]:
        if cached is not None:
            if "etag" in cached:
                return {**self._headers, "If-None-Match": cached["etag"]}
            elif "last_modified" in cached:
                return {**self._headers, "If-Modified-Since": cached["last_modified"]}
        return self._headers

    @staticmethod
    def _trust_cache(cached: Any) -> bool:
        # If the request was cached and the VMTEST_TRUST_CACHE environment
        # variable is non-zero, assume the cache is still valid.
        try:
            return cached is not None and int(os.getenv("VMTEST_TRUST_CACHE", "0")) != 0
        except ValueError:
            return False

    def _write_cache(
        self, cache: _CACHE, body: Any, headers: Mapping[str, str]
    ) -> None:
        if cache is not None and ("ETag" in headers or "Last-Modified" in headers):
            to_cache = {"body": body}
            if "ETag" in headers:
                to_cache["etag"] = headers["ETag"]
            if "Last-Modified" in headers:
                to_cache["last_modified"] = headers["Last-Modified"]
            with open(cache, "w") as f:
                json.dump(to_cache, f)

    def get_release_by_tag(
        self, owner: str, repo: str, tag: str, *, cache: _CACHE = None
    ) -> Any:
        return self._cached_get_json(f"repos/{owner}/{repo}/releases/tags/{tag}", cache)

    def download(self, url: str) -> Any:
        return self._request(
            "GET", url, headers={**self._headers, "Accept": "application/octet-stream"}
        )

    def upload(self, url: str, data: Any, content_type: str) -> Any:
        return self._request(
            "POST",
            url,
            headers={**self._headers, "Content-Type": content_type},
            data=data,
        )


class GitHubApi(_GitHubApiBase):
    def _request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
    ) -> Any:
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(
            url,
            data=data,
            headers={} if headers is None else headers,
            method=method,
        )
        # Work around python/cpython#77842.
        if req.has_header("Authorization"):
            authorization = req.get_header("Authorization")
            req.remove_header("Authorization")
            req.add_unredirected_header("Authorization", authorization)
        return urllib.request.urlopen(req)

    def _cached_get_json(self, endpoint: str, cache: _CACHE) -> Any:
        cached = self._read_cache(cache)
        if self._trust_cache(cached):
            return cached["body"]
        req = urllib.request.Request(
            self._HOST + "/" + endpoint,
            headers=self._cached_get_headers(cached),
        )
        # Work around python/cpython#77842.
        if req.has_header("Authorization"):
            authorization = req.get_header("Authorization")
            req.remove_header("Authorization")
            req.add_unredirected_header("Authorization", authorization)
        try:
            with urllib.request.urlopen(req) as resp:
                body = json.load(resp)
                self._write_cache(cache, body, resp.headers)
                return body
        except urllib.error.HTTPError as e:
            if e.code == 304 and cached is not None:
                return cached["body"]
            else:
                raise


class AioGitHubApi(_GitHubApiBase):
    def __init__(self, session: "aiohttp.ClientSession", token: Optional[str]) -> None:
        super().__init__(token)
        self._session = session

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
    ) -> Any:
        return self._session.request(
            method,
            url,
            params=params,
            headers=headers,
            data=data,
            raise_for_status=True,
        )

    async def _cached_get_json(self, endpoint: str, cache: _CACHE) -> Any:
        cached = self._read_cache(cache)
        if self._trust_cache(cached):
            return cached["body"]
        async with self._session.get(
            self._HOST + "/" + endpoint,
            headers=self._cached_get_headers(cached),
            raise_for_status=True,
        ) as resp:
            if resp.status == 304:
                if cached is None:
                    raise Exception("got HTTP 304 but response was not cached")
                return cached["body"]
            else:
                body = await resp.json()
                self._write_cache(cache, body, resp.headers)
                return body
