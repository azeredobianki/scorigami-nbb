"""Gera o arquivo compacto do site (games.json) a partir dos CSVs brutos da LNB.

Uso: python3 -I scripts/build_data.py dados/brutos/lnb site/games.json

Cada CSV se chama <temporada>_<fase>.csv (fase = reg ou po), tem cabeçalho e as colunas
data,mandante,pts_mandante,pts_visitante,visitante,rodada,etapa,hora,prorrogacoes,quartos,status_quartos,
fonte_prorrogacao,id_lnb,link
"prorrogacoes" é o número de períodos extras (0, 1, 2...; "1+" quando a fonte só diz que houve prorrogação)
ou vazio quando nenhuma fonte informa.
"""
import csv
import json
import sys
from pathlib import Path

# Nome exibido pela LNB (muda com patrocínio) -> franquia.
FRANQUIAS = {
    "123 Minas": "Minas", "KTO Minas": "Minas", "Minas Storm": "Minas", "Minas": "Minas",
    "Araraquara": "Araraquara", "Assis": "Assis",
    "Brasília": "Brasília", "BRB/Brasília": "Brasília", "CAIXA/Brasília Basquete": "Brasília",
    "Basket Osasco": "Osasco",
    "Basq. Cearense": "Basquete Cearense", "Basquete Cearense": "Basquete Cearense",
    "Fortaleza B. C.": "Basquete Cearense", "Fortaleza B. C. / CFO": "Basquete Cearense",
    "Fortaleza Basquete Cearense": "Basquete Cearense",
    "Bauru": "Bauru", "Bauru Basket": "Bauru", "Botafogo": "Botafogo",
    "Campo Mourão": "Campo Mourão", "VipTech CMB": "Campo Mourão",
    "Caxias do Sul": "Caxias do Sul", "Caxias do Sul Basquete": "Caxias do Sul", "KTO/Caxias do Sul": "Caxias do Sul",
    "União Corinthians": "União Corinthians", "Ceisc/União Corinthians": "União Corinthians",
    "Luvix/União Corinthians": "União Corinthians",
    "Cerrado": "Cerrado", "Cerrado Basquete": "Cerrado",
    "Rio Claro": "Rio Claro", "Conta Simples Rio Claro": "Rio Claro",
    "São José": "São José", "São José Basketball": "São José", "Coop/São José Basketball": "São José",
    "Farma Conde/São José Basketball": "São José", "Mr. Moo São José Basketball": "São José",
    "Oscar São José Basketball": "São José",
    "Corinthians": "Corinthians",
    "Cruzeiro": "Cruzeiro", "Itatiaiuçu Cruzeiro Basquete": "Cruzeiro",
    "Mogi": "Mogi", "Mogi Basquete": "Mogi", "Desk Manager Mogi Basquete": "Mogi",
    "Espírito Santo": "Espírito Santo", "Flamengo": "Flamengo",
    "Franca": "Franca", "Sesi Franca": "Franca", "Goiânia": "Goiânia",
    "Joinville": "Joinville", "Joinville / AABJ": "Joinville",
    "L. Sorocabana": "Liga Sorocabana", "Lajeado": "Lajeado", "Limeira": "Limeira", "Londrina": "Londrina",
    "Macaé": "Macaé", "Macaé Basquete": "Macaé", "Palmeiras": "Palmeiras", "Pato Basquete": "Pato",
    "Paulistano": "Paulistano", "Paulistano/CORPe": "Paulistano", "Pinheiros": "Pinheiros",
    "R10 Score Vasco da Gama": "Vasco da Gama", "Vasco da Gama": "Vasco da Gama",
    "Saldanha": "Saldanha da Gama", "Suzano": "Suzano", "São Paulo": "São Paulo", "Tijuca": "Tijuca",
    "UNIFACISA": "Unifacisa", "Uberlândia": "Uberlândia", "Vitória": "Vitória", "Vitória (ES)": "Vitória (ES)",
}


def main(src, dst):
    teams, games = [], []
    idx = {}

    def tid(name):
        f = FRANQUIAS.get(name, name)
        if name not in FRANQUIAS:
            print(f"aviso: time sem franquia mapeada: {name}", file=sys.stderr)
        if f not in idx:
            idx[f] = len(teams)
            teams.append(f)
        return idx[f]

    for path in sorted(Path(src).glob("*.csv")):
        season, phase = path.stem.split("_")
        with open(path, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                dd, mm, yy = row["data"].strip().split("/")
                n = row["prorrogacoes"].strip()
                games.append([f"{yy}-{mm}-{dd}", season, 1 if phase == "po" else 0,
                              tid(row["mandante"].strip()), tid(row["visitante"].strip()),
                              int(row["pts_mandante"]), int(row["pts_visitante"]),
                              None if n == "" else n != "0"])
    games.sort(key=lambda g: g[0])
    out = {"teams": teams, "fields": ["date", "season", "playoff", "home", "away", "hs", "as", "ot"],
           "games": games}
    Path(dst).write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(games)} jogos, {len(teams)} times -> {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
