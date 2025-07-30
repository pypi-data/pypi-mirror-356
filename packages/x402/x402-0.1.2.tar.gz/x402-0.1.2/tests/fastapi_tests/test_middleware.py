from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from x402.fastapi.middleware import require_payment


async def test_endpoint():
    return {"message": "success"}


def test_middleware_invalid_payment():
    app_with_middleware = FastAPI()
    app_with_middleware.get("/test")(test_endpoint)
    app_with_middleware.middleware("http")(
        require_payment(
            price="$1.00",
            pay_to_address="0x1111111111111111111111111111111111111111",
            network_id="base-sepolia",
            description="Test payment",
        )
    )

    client = TestClient(app_with_middleware)
    response = client.get("/test", headers={"X-PAYMENT": "invalid_payment"})

    assert response.status_code == 402
    assert "accepts" in response.json()
    assert "Invalid payment header format:" in response.json()["error"]


def test_app_middleware_path_matching():
    app_with_middleware = FastAPI()
    app_with_middleware.get("/test")(test_endpoint)
    app_with_middleware.get("/unprotected")(test_endpoint)

    app_with_middleware.middleware("http")(
        require_payment(
            price="$1.00",
            pay_to_address="0x1111111111111111111111111111111111111111",
            path="/test",
            network_id="base-sepolia",
            description="Test payment",
        )
    )

    client = TestClient(app_with_middleware)

    # Protected endpoint should require payment
    response = client.get("/test")
    assert response.status_code == 402

    # Unprotected endpoint should work without payment
    response = client.get("/unprotected")
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


def test_middleware_path_list_matching():
    app_with_middleware = FastAPI()
    app_with_middleware.get("/test1")(test_endpoint)
    app_with_middleware.get("/test2")(test_endpoint)
    app_with_middleware.get("/unprotected")(test_endpoint)

    app_with_middleware.middleware("http")(
        require_payment(
            price="$1.00",
            pay_to_address="0x1111111111111111111111111111111111111111",
            path=["/test1", "/test2"],
            network_id="base-sepolia",
            description="Test payment",
        )
    )

    client = TestClient(app_with_middleware)

    # Protected endpoints should require payment
    response = client.get("/test1")
    assert response.status_code == 402

    response = client.get("/test2")
    assert response.status_code == 402

    # Unprotected endpoint should work without payment
    response = client.get("/unprotected")
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


def expected_path(given: str, expected: str) -> bool:
    app = FastAPI()

    @app.get("/{path:path}")
    def test(request: Request):
        return {"path": request.url.path}

    client = TestClient(app)
    response = client.get(given)
    p = response.json()
    print(p)
    return p == {"path": expected}


def test_path_matching():
    from x402.fastapi.middleware import _path_is_match

    # Test paths are parsed correctly
    assert expected_path("/", "/")
    assert not expected_path("/test   ", "/test")
    assert expected_path("/test?x=1", "/test")
    assert expected_path("/test/123", "/test/123")
    assert expected_path("/test/123?x=1", "/test/123")
    assert expected_path("/test/123?x=1&y=2", "/test/123")
    assert expected_path("/test/123?x=1&y=2", "/test/123")

    # Test Exact matching
    assert _path_is_match("/test", "/test")
    assert not _path_is_match("/test", "/test/123")
    assert not _path_is_match("/test", "/different")

    # Test glob patterns
    assert _path_is_match("/api/*", "/api/users")
    assert _path_is_match("/api/*", "/api/posts")
    assert _path_is_match("/api/*/profile", "/api/user/profile")
    assert _path_is_match("/api/*/profile", "/api/admin/profile")
    assert not _path_is_match("/api/*/profile", "/api/user/settings")

    # Test regex patterns
    assert _path_is_match("regex:^/api/users/\\d+$", "/api/users/123")
    assert _path_is_match("regex:^/api/users/\\d+$", "/api/users/456")
    assert not _path_is_match("regex:^/api/users/\\d+$", "/api/users/abc")
    assert not _path_is_match("regex:^/api/users/\\d+$", "/api/users/123/posts")

    # Test list matching
    assert _path_is_match(["/test1", "/test2"], "/test1")
    assert _path_is_match(["/test1", "/test2"], "/test2")
    assert not _path_is_match(["/test1", "/test2"], "/test3")

    # Test mixed patterns in list
    assert _path_is_match(["/exact", "/api/*", "regex:^/users/\\d+$"], "/exact")
    assert _path_is_match(["/exact", "/api/*", "regex:^/users/\\d+$"], "/api/posts")
    assert _path_is_match(["/exact", "/api/*", "regex:^/users/\\d+$"], "/users/123")
    assert not _path_is_match(["/exact", "/api/*", "regex:^/users/\\d+$"], "/other")


def test_abusive_url_paths():
    """Test various abusive and edge-case URL paths that could bypass security"""
    from x402.fastapi.middleware import _path_is_match

    # Path traversal attacks
    path_traversal_attempts = [
        "../../../etc/passwd",
        "..%2F..%2F..%2Fetc%2Fpasswd",  # URL encoded
        "..\\..\\..\\windows\\system32",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2ffile",  # Double URL encoded
        "....//....//....//file",
        "..%252f..%252f..%252ffile",  # Double URL encoded
        "..%c0%af..%c0%af..%c0%affile",  # UTF-8 overlong encoding
        "/..;/..;/..;/file",
        "/.%00./..%00./..%00./file",  # Null byte injection
    ]

    # Test that path traversal doesn't match protected paths
    for malicious_path in path_traversal_attempts:
        assert not _path_is_match("/api/protected", f"/api/protected/{malicious_path}")
        assert not _path_is_match("/api/protected", malicious_path)
        # But should match if explicitly allowed
        assert _path_is_match("/api/*", f"/api/{malicious_path}")

    # URL encoding bypass attempts
    encoding_bypasses = [
        "/api%2fprotected",  # Path separator encoding
        "/api%252fprotected",  # Double encoding
        "/api%c0%afprotected",  # UTF-8 overlong
        "/api%2520protected",  # Space encoding variations
        "/api%09protected",  # Tab character
        "/api%0aprotected",  # Line feed
        "/api%0d%0aprotected",  # CRLF injection
        "/api\x00protected",  # Null byte
        "/api/./protected",  # Current directory
        "/api/../api/protected",  # Directory traversal but same result
        "//api//protected",  # Double slashes
        "/api///protected",  # Multiple slashes
        "/API/PROTECTED",  # Case variations
        "/Api/Protected",
        "/aPi/pRoTeCtEd",
    ]

    # Test various encoding attempts
    for encoded_path in encoding_bypasses:
        # These should NOT match exact path
        assert not _path_is_match("/api/protected", encoded_path), (
            f"encoded_path: {encoded_path}"
        )
        # But glob patterns might catch some
        if encoded_path.startswith("/api/") and "//" in encoded_path:
            assert _path_is_match("/api/*", encoded_path), (
                f"encoded_path: {encoded_path}"
            )

    # Fragment and query parameter bypass attempts
    fragment_query_bypasses = [
        "/public#/../protected",
        "/public?../protected",
        "/public/../protected#fragment",
        "/public/../protected?param=value",
        "/public;jsessionid=123/../protected",
        "/public/../protected;jsessionid=456",
    ]

    # These should be handled by the URL parsing (query/fragment stripped)
    for bypass_path in fragment_query_bypasses:
        # The actual path component should be matched
        if "/../protected" in bypass_path:
            assert not _path_is_match("/protected", bypass_path)

    # HTTP method override attempts (path-based)
    method_override_paths = [
        "/api/users?_method=DELETE",
        "/api/users?_method=PUT",
        "/api/users?_method=PATCH",
        "/api/users?X-HTTP-Method-Override=DELETE",
    ]

    for method_path in method_override_paths:
        assert expected_path(method_path, "/api/users")

    # Unicode normalization attacks
    unicode_attacks = [
        "/api/protectedﾉ",  # Full-width characters
        "/api/protected\u200b",  # Zero-width space
        "/api/protected\u2028",  # Line separator
        "/api/protected\u2029",  # Paragraph separator
        "/api/protected\ufeff",  # Byte order mark
        "/api/protected\u202e",  # Right-to-left override
        "/api/protectedⒶ",  # Enclosed characters
        "/api/protectedﬀ",  # Ligatures
    ]

    for unicode_path in unicode_attacks:
        # These should NOT match the original path due to different Unicode
        assert not _path_is_match("/api/protected", unicode_path)
        # But glob should catch them
        assert _path_is_match("/api/*", unicode_path)

    # Long path attacks
    very_long_path = "/api/" + "a" * 1000
    extremely_long_path = "/api/" + "a" * 10000
    assert _path_is_match("/api/*", very_long_path)
    assert _path_is_match("/api/*", extremely_long_path)
    assert not _path_is_match("/api/short", very_long_path)

    # Empty and special characters
    special_paths = [
        "",  # Empty path
        "/",  # Root only
        "//",  # Double slash
        "///",  # Triple slash
        "/api/",  # Trailing slash
        "/api//",  # Double trailing slash
        "/api/./",  # Current directory with trailing slash
        "/api/../",  # Parent directory with trailing slash
        "/api/ ",  # Space
        "/api/\t",  # Tab
        "/api/\n",  # Newline
        "/api/\r",  # Carriage return
        "/api/\r\n",  # CRLF
        "/api/\x00",  # Null byte
        "/api/\x7f",  # DEL character
        "/api/\xff",  # High byte
    ]

    for special_path in special_paths:
        # Test that our matching handles these edge cases
        if special_path.startswith("/api/") and len(special_path) > 5:
            assert _path_is_match("/api/*", special_path)
        elif special_path == "/api/":
            assert _path_is_match("/api/", special_path)

    # Case sensitivity tests
    case_variations = [
        ("/API/USERS", "/api/users", False),  # Should not match due to case
        ("/Api/Users", "/api/users", False),
        ("/api/USERS", "/api/users", False),
        ("/api/users", "/api/users", True),  # Exact match
    ]

    for test_pattern, test_path, should_match in case_variations:
        result = _path_is_match(test_pattern, test_path)
        assert result == should_match, (
            f"Pattern '{test_pattern}' vs path '{test_path}' should {'match' if should_match else 'not match'}"
        )

    # Regex injection attempts
    regex_injection_attempts = [
        "regex:.*",  # Match everything
        "regex:^.*$",  # Match everything anchored
        "regex:^/api/(.*)",  # Capture group attempt
        "regex:^/api/|/admin/",  # OR condition
        "regex:^/api/(?:users|admin)",  # Non-capturing group
        "regex:^/api/users.*(?=admin)",  # Lookahead
        "regex:^/api/users.*(?!public)",  # Negative lookahead
    ]

    # These should work as intended since they're valid regex patterns
    for regex_pattern in regex_injection_attempts:
        if regex_pattern == "regex:.*":
            assert _path_is_match(regex_pattern, "/any/path")
            assert _path_is_match(regex_pattern, "/api/users")
        elif regex_pattern == "regex:^.*$":
            assert _path_is_match(regex_pattern, "/any/path")
        elif regex_pattern == "regex:^/api/(.*)":
            assert _path_is_match(regex_pattern, "/api/users")
            assert not _path_is_match(regex_pattern, "/other/path")
        elif regex_pattern == "regex:^/api/|/admin/":
            assert _path_is_match(regex_pattern, "/api/anything")
            assert _path_is_match(regex_pattern, "/admin/panel")
            assert not _path_is_match(regex_pattern, "/other/path")
