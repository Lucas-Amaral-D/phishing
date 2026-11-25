"""Atributos lexicais calculados localmente, sem tráfego de rede."""
import ipaddress
import re
from urllib.parse import urlsplit

import tldextract

psl = tldextract.TLDExtract(suffix_list_urls=(), cache_dir=None, include_psl_private_domains=True)
FEATURES = [
    "comprimento", "host_chars", "digitos", "letras", "especiais", "pontos", "hifens",
    "subdominios", "https", "ip", "parametros", "profundidade", "porta", "fragmento", "sufixo",
]


def parse_url(url):
    if not isinstance(url, str) or not url or len(url) > 16384:
        raise ValueError("Informe um endereço HTTP ou HTTPS de até 16.384 caracteres.")
    if re.search(r"\s|[\x00-\x1f\x7f\\]", url):
        raise ValueError("O endereço contém caracteres inválidos.")
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username is not None:
        raise ValueError("Informe um endereço HTTP ou HTTPS com domínio e sem credenciais.")
    _ = parts.port
    host = parts.hostname.rstrip(".").encode("idna").decode("ascii").lower()
    try:
        return parts, str(ipaddress.ip_address(host)), True
    except ValueError:
        labels = host.split(".")
        if len(host) > 253 or not all(
            re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in labels
        ):
            raise ValueError("O domínio contém caracteres inválidos.")
    return parts, host, False


def domain_group(url):
    _, host, is_ip = parse_url(url)
    if is_ip:
        return host
    return psl(host).top_domain_under_public_suffix or host


def extract_url(url):
    parts, host, is_ip = parse_url(url)
    domain = psl(host) if not is_ip else None
    return dict(zip(FEATURES, [
        len(url), len(host), sum(map(str.isdigit, url)), sum(map(str.isalpha, url)),
        sum(not char.isalnum() for char in url), host.count("."), url.count("-"),
        len(domain.subdomain.split(".")) if domain and domain.subdomain else 0,
        int(parts.scheme == "https"), int(is_ip),
        sum(bool(field) for field in parts.query.split("&")),
        sum(bool(segment) for segment in parts.path.split("/")),
        int(parts.port is not None), int(bool(parts.fragment)), domain.suffix if domain else "",
    ], strict=True))
