#!/usr/bin/env python3
"""Verifica se todas as imagens do README ainda respondem.

Uso:
    python scripts/check-readme-links.py

Sai com codigo 1 se alguma imagem estiver fora do ar. Servicos gratuitos de
cartoes de estatisticas caem sem aviso, e o README quebra em silencio quando
isso acontece -- este check existe para nao descobrir pelo print de outra pessoa.

Detecta tres formas de quebra:
  * resposta HTTP diferente de 200
  * SVG de erro devolvido com status 200 (o padrao do github-readme-stats
    quando falta o token: "Something went wrong" / "Maximum retries exceeded")
  * caminho local referenciado no README que nao existe no repositorio
"""

from __future__ import annotations

import io
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
TIMEOUT = 45
RETRIES = 3  # instancias compartilhadas devolvem 503 esporadico sob carga

ERROR_MARKERS = (
    "something went wrong",
    "maximum retries exceeded",
    "user not found",
    "deployment_paused",
    "could not fetch",
)


def sources(text: str) -> list[str]:
    found = re.findall(r'(?:src|srcset)="([^"]+)"', text)
    seen: dict[str, None] = {}
    for url in found:
        seen.setdefault(url, None)
    return list(seen)


def check_remote(url: str) -> str | None:
    """Retorna None se ok, ou uma descricao do problema."""
    last = "sem resposta"
    for attempt in range(RETRIES):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "readme-link-check"})
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                body = response.read(20000).decode("utf-8", "replace").lower()
                for marker in ERROR_MARKERS:
                    if marker in body:
                        return f"status 200 mas o SVG diz: {marker!r}"
                return None
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}"
        except Exception as exc:  # timeout, DNS, TLS
            last = f"{type(exc).__name__}: {exc}"
    return f"{last} (apos {RETRIES} tentativas)"


def main() -> int:
    text = io.open(README, encoding="utf-8").read()
    urls = sources(text)
    if not urls:
        print("nenhuma imagem encontrada no README")
        return 1

    failures: list[tuple[str, str]] = []
    print(f"verificando {len(urls)} imagens do README\n")

    for url in urls:
        if url.startswith("http"):
            problem = check_remote(url)
        else:
            local = ROOT / url
            problem = None if local.exists() else "arquivo local nao encontrado"

        label = url if len(url) <= 88 else url[:85] + "..."
        if problem:
            failures.append((url, problem))
            print(f"  FALHA  {label}\n         -> {problem}")
        else:
            print(f"  ok     {label}")

    print()
    if failures:
        print(f"{len(failures)} de {len(urls)} imagens quebradas.")
        print("Para hospedar seus proprios cartoes: docs/self-host-stats.md")
        return 1

    print(f"todas as {len(urls)} imagens responderam.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
