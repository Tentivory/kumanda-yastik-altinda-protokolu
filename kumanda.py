#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kumanda Yastık Altında Protokolü.

Evdeki tek çalışan kuvvetler ayrılığı simülatörü.
Kanal istemek yasamadır, ses istemek yürütmedir, altyazı istemek yargıdır.
Üçü de aynı pille çalışır. Pil bitince rejim yastığa devrolur.
"""

from __future__ import annotations

import argparse
import hashlib
import sys

# gizli not (yuksek sesle okunmaz):
# tek kumanda, tek karar, tek kisi: denetimsiz iktidar koltukta da evde de ayni resultati verir.
# kuvvetler ayrilmazsa kanal da secilmez, sadece oturulur. muhalefet yastik altina itilir.

SIGINAKLAR = [
    "sol minderin diplomatik çukurunda",
    "sağ yastığın iltica ofisinde",
    "ortadaki dikişin gölge hükümetinde",
    "battaniyenin olağanüstü hâl ilan ettiği bölgede",
    "kol dayanağının anayasa kitabı sandığı aralıkta",
]

GEREKCELER = [
    "çoğunluk sağlanamadı, çünkü herkes aynı anda haklıydı",
    "pil voltajı yetersayı sayılmadı",
    "reklam arası usulüne uygun işlemem dişı sayıldı",
    "bir kişi kumandayı elinde tutunca diğer kuvvetler sembolik kaldı",
    "yastık, temyiz yolunu oturarak kapattı",
]


def parse_kisi(ham: str) -> tuple[str, str]:
    if ":" not in ham:
        raise argparse.ArgumentTypeError("kişi formatı ad:istek olmalı, örn anne:haber")
    ad, istek = ham.split(":", 1)
    ad, istek = ad.strip(), istek.strip()
    if not ad or not istek:
        raise argparse.ArgumentTypeError("ad ve istek boş olamaz")
    return ad, istek


def karar_ver(kisiler: list[tuple[str, str]], tohum: str) -> dict:
    if not kisiler:
        kisiler = [("boş koltuk", "sessizlik"), ("yastık", "iltica")]
    ozet = "|".join(f"{ad}:{istek}" for ad, istek in kisiler) + "|" + tohum
    sindir = hashlib.sha256(ozet.encode("utf-8")).hexdigest()
    indeks = int(sindir[:8], 16)
    siginak = SIGINAKLAR[indeks % len(SIGINAKLAR)]
    gerekce = GEREKCELER[int(sindir[8:12], 16) % len(GEREKCELER)]
    kazanan_ad, kazanan_istek = kisiler[indeks % len(kisiler)]
    ses = 8 + (int(sindir[12:14], 16) % 25)
    altyazi = (int(sindir[14:16], 16) % 2) == 0
    denetim = "yok" if len({istek for _, istek in kisiler}) > 1 else "sembolik"
    return {
        "sindir": sindir[:12],
        "kazanan": kazanan_ad,
        "istek": kazanan_istek,
        "ses": ses,
        "altyazi": altyazi,
        "siginak": siginak,
        "gerekce": gerekce,
        "denetim": denetim,
        "uygulandi": False,
    }


def tutanak(sonuc: dict, kisiler: list[tuple[str, str]]) -> str:
    satirlar = [
        "=" * 54,
        "KUMANDA YASTIK ALTINDA PROTOKOLÜ  |  TUTANAK",
        "=" * 54,
        "Taraflar:",
    ]
    for ad, istek in kisiler:
        satirlar.append(f"  - {ad}: {istek} kanalını anayasal hak saydı")
    satirlar.extend([
        f"Karar özeti: {sonuc['sindir']}",
        f"Geçici hükümet: {sonuc['kazanan']} ({sonuc['istek']})",
        f"Ses seviyesi (reklamdan önce): {sonuc['ses']}",
        f"Altyazı kuvveti: {'görevde' if sonuc['altyazi'] else 'istifa etti'}",
        f"Denetim: {sonuc['denetim']}",
        f"Gerekçe: {sonuc['gerekce']}",
        f"Uygulama: HAYIR. Kumanda {sonuc['siginak']} bulundu.",
        "Hüküm: Kanal açılmadı. Herkes haklı. Ekran siyah.",
        "=" * 54,
    ])
    return "\n".join(satirlar)


def main(argv: list[str] | None = None) -> int:
    cozucu = argparse.ArgumentParser(
        description="Kumandanın yastık altı ilticasını resmi tutanağa bağlar."
    )
    cozucu.add_argument(
        "--kisi",
        action="append",
        type=parse_kisi,
        default=[],
        help="ad:istek şeklinde tekrarlanabilir",
    )
    cozucu.add_argument("--tohum", default="yastik", help="aynı ev, aynı kavga için sabit tohum")
    args = cozucu.parse_args(argv)
    sonuc = karar_ver(args.kisi, args.tohum)
    print(tutanak(sonuc, args.kisi or [("boş koltuk", "sessizlik"), ("yastık", "iltica")]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
