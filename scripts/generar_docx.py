#!/usr/bin/env python3
"""Genera una planificación .docx con el formato institucional exacto.

Usa formato/plantilla_planificacion.docx como molde: copia sus tablas,
estilos, márgenes y orientación, y solo reemplaza el contenido.

Uso:
    python scripts/generar_docx.py cursos/2M-fisica/planificaciones/U3-energia-momentum.yaml
    python scripts/generar_docx.py --check <archivo.yaml>   # solo valida
"""
import copy
import re
import sys
from pathlib import Path

import docx
import yaml

RAIZ = Path(__file__).resolve().parent.parent
PLANTILLA = RAIZ / "formato" / "plantilla_planificacion.docx"

CAMPOS_ENCABEZADO = ["unidad", "profesor", "curso", "asignatura", "mes"]
CAMPOS_SEMANA = ["semana", "tema", "actividades", "objetivos_especificos",
                 "bloom", "evaluacion_formativa"]
BLOOM_VALIDOS = {"Recordar", "Comprender", "Aplicar", "Analizar", "Evaluar", "Crear"}


# ---------------------------------------------------------------- validación
def validar(plan, ruta_yaml):
    errores = []
    enc = plan.get("encabezado") or {}
    for c in CAMPOS_ENCABEZADO:
        if not str(enc.get(c, "")).strip():
            errores.append(f"encabezado.{c} vacío")
    if not re.fullmatch(r"20\d\d", str(plan.get("anio", ""))):
        errores.append("anio falta o no es un año (ej: 2027)")
    for c in ["proposito", "duracion"]:
        if not str(plan.get(c, "")).strip():
            errores.append(f"{c} vacío")
    oas = plan.get("objetivos") or []
    if not oas:
        errores.append("objetivos: debe haber al menos un OA")
    codigos = {o.get("oa") for o in oas}
    semanas = plan.get("semanas") or []
    if not semanas:
        errores.append("semanas: lista vacía")
    for i, s in enumerate(semanas, 1):
        for c in CAMPOS_SEMANA:
            if not str(s.get(c, "")).strip():
                errores.append(f"semana {i}: campo '{c}' vacío")
        for nivel in re.split(r"\s*/\s*", str(s.get("bloom", ""))):
            if nivel and nivel not in BLOOM_VALIDOS:
                errores.append(f"semana {i}: nivel Bloom desconocido '{nivel}'")
        for oa in s.get("oa", []) or []:
            if oa not in codigos:
                errores.append(f"semana {i}: {oa} no está en 'objetivos' de la unidad")
    # cobertura: todo OA de la unidad debe aparecer en alguna semana
    usados = {oa for s in semanas for oa in (s.get("oa") or [])}
    for oa in codigos - usados:
        errores.append(f"{oa} no está asignado a ninguna semana")
    # el OA debe existir en el programa del curso
    curso = next((d for d in Path(ruta_yaml).resolve().parents if d.parent.name == "cursos"), None)
    prog = curso / "programa" / "oa.md" if curso else None
    if prog is None or not prog.exists():
        errores.append("no se encontró cursos/<curso>/programa/oa.md")
    else:
        texto = prog.read_text(encoding="utf-8")
        for oa in codigos:
            if not re.search(rf"\b{re.escape(oa)}\b", texto):
                errores.append(f"{oa} no figura en {prog.relative_to(RAIZ)}")
    return errores


# ------------------------------------------------------------ helpers docx
def _poner_texto(parrafo, texto):
    """Reemplaza el texto del párrafo conservando el formato del primer run."""
    runs = parrafo.runs
    if not runs:
        parrafo.add_run(texto)
        return
    runs[0].text = texto
    for r in runs[1:]:
        r._element.getparent().remove(r._element)


def llenar_celda(celda, lineas):
    """Escribe una lista de líneas, un párrafo por línea, con el formato
    del primer párrafo con texto de la celda."""
    if isinstance(lineas, str):
        lineas = [lineas]
    parrafos = celda.paragraphs
    molde = next((p for p in parrafos if p.text.strip()), parrafos[0])
    molde_xml = copy.deepcopy(molde._element)
    for p in parrafos:
        p._element.getparent().remove(p._element)
    for linea in lineas:
        nuevo = copy.deepcopy(molde_xml)
        celda._element.append(nuevo)
        _poner_texto(docx.text.paragraph.Paragraph(nuevo, celda), str(linea))


def generar(plan, salida):
    d = docx.Document(PLANTILLA)
    # año en el título institucional ("UNIDAD TECNICO PEDAGOGICA 2026")
    anio = str(plan.get("anio", 2026))
    for r in d.paragraphs[1].runs:
        r.text = re.sub(r"\b20\d\d\b", anio, r.text)
    t_enc, t_prop, t_sem = d.tables[0], d.tables[1], d.tables[2]
    enc = plan["encabezado"]

    llenar_celda(t_enc.cell(0, 0), [enc["unidad"],
                                    f"Profesor (a): {enc['profesor']}",
                                    f"Curso: {enc['curso']}"])
    llenar_celda(t_enc.cell(0, 1), [f"Asignatura: {enc['asignatura']}",
                                    f"Mes: {enc['mes']}"])

    llenar_celda(t_prop.cell(1, 0), plan["proposito"].strip())
    oas = []
    for i, o in enumerate(plan["objetivos"]):
        if i:
            oas.append("")  # línea en blanco entre OA, como en el original
        oas.append(f"{o['oa']}: {o['texto'].strip()}")
    llenar_celda(t_prop.cell(1, 1), oas)
    llenar_celda(t_prop.cell(1, 2), str(plan["duracion"]))

    # tabla semanal: se clona la fila 1 como molde para cada semana
    filas = t_sem.rows
    molde_fila = copy.deepcopy(filas[1]._tr)
    for f in list(filas)[1:]:
        t_sem._tbl.remove(f._tr)
    for s in plan["semanas"]:
        tr = copy.deepcopy(molde_fila)
        t_sem._tbl.append(tr)
        fila = t_sem.rows[-1]
        valores = [str(s["semana"]), s["tema"], s["actividades"],
                   s["objetivos_especificos"], s["bloom"], s["evaluacion_formativa"]]
        for celda, v in zip(fila.cells, valores):
            llenar_celda(celda, " ".join(str(v).split()))

    # nota final (título en negrita + texto en cursiva)
    p_nota = d.paragraphs[4]
    nota = plan.get("nota")
    runs = p_nota.runs
    if nota:
        runs[0].text = nota["titulo"].rstrip(":") + ": "
        runs[1].text = " ".join(nota["texto"].split())
        for r in runs[2:]:
            r._element.getparent().remove(r._element)
    else:
        p_nota._element.getparent().remove(p_nota._element)

    Path(salida).parent.mkdir(parents=True, exist_ok=True)
    d.save(salida)


def main(args):
    solo_check = "--check" in args
    args = [a for a in args if a != "--check"]
    if not args:
        print(__doc__)
        return 1
    codigo = 0
    for ruta in args:
        plan = yaml.safe_load(Path(ruta).read_text(encoding="utf-8"))
        errores = validar(plan, ruta)
        if errores:
            codigo = 1
            print(f"✗ {ruta}")
            for e in errores:
                print(f"   - {e}")
            continue
        if solo_check:
            print(f"✓ {ruta} válido")
            continue
        salida = Path(ruta).parent / "docx" / (Path(ruta).stem + ".docx")
        generar(plan, salida)
        print(f"✓ {salida}")
    return codigo


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
