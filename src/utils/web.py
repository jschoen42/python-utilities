"""
    © Jürgen Schoenemeyer, 07.02.2026 22:49

    src/utils/web.py

    PUBLIC:
     - check_certifikat
"""
from __future__ import annotations

import socket
import ssl

from typing import Any, Dict

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID

from src.utils.trace import Trace

def inspect_certificate(hostname: str, port: int = 443) -> Dict[str, Any] | None:

    def fetch_raw_cert(verify: bool) -> x509.Certificate | None:
        context = ssl.create_default_context() if verify else ssl._create_unverified_context()
        try:
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    der_cert = ssock.getpeercert(binary_form=True)
                    if der_cert:
                        return x509.load_der_x509_certificate(der_cert, default_backend())
                    else:
                        return None
        except (TimeoutError, OSError, ssl.SSLCertVerificationError, ssl.SSLError) as e:
            Trace.error(f"❌ Fehler beim Abrufen des Zertifikats ({'mit' if verify else 'ohne'} Prüfung): {e}")
            return None

    # Stufe 1: mit Prüfung
    cert = fetch_raw_cert(verify=True)
    if cert is None:
        Trace.error("⚠️ Zertifikatsprüfung fehlgeschlagen – versuche ohne Prüfung...")
        cert = fetch_raw_cert(verify=False)
        if cert is None:
            Trace.error("❌ Zertifikat konnte nicht geladen werden.")
            return None

    # Extraktion von CN und SANs
    result: Dict[str, Any] = {}
    try:
        cn_attr = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        result["common_name"] = cn_attr[0].value if cn_attr else None
    except Exception:
        result["common_name"] = None

    try:
        san_ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        result["subject_alt_names"] = san_ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        result["subject_alt_names"] = []

    # Weitere Infos (optional)
    result["issuer"] = cert.issuer.rfc4514_string()
    result["valid_from"] = cert.not_valid_before_utc.isoformat()
    result["valid_until"] = cert.not_valid_after_utc.isoformat()

    Trace.info("Zertifikatsinformationen:")
    for key, value in result.items():
        Trace.info(f"  {key}: {value}")

    return result
