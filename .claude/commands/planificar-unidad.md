---
description: Crea una planificación de unidad nueva en el formato institucional
argument-hint: <curso> <unidad> [semanas] [meses]   ej: 2M-fisica "Unidad 4" 8 "Octubre y noviembre"
---
Planifica una unidad nueva: $ARGUMENTS

1. Lee `CLAUDE.md`, `formato/FORMATO.md` y el ejemplo `cursos/2M-fisica/planificaciones/U3-energia-momentum.yaml`.
2. Lee `cursos/<curso>/programa/oa.md`. Si los OA de esta unidad no están, **detente** y pide la fuente oficial (Regla 2).
3. Revisa la unidad anterior del curso, sus registros y sus evaluaciones para detectar:
   - OA o indicadores con logro bajo que convenga retomar como activación,
   - metodologías que funcionaron o no funcionaron, según los registros.
4. Si faltan datos (cantidad de semanas, meses, horas por semana, fechas fijas), pregúntalos en un solo mensaje.
5. Escribe `cursos/<curso>/planificaciones/U<n>-<slug>.yaml` con `estado: borrador` y `version: 1`:
   - OA literales,
   - progresión Bloom por ciclo de OA,
   - una evaluación formativa por semana y al menos una sumativa por OA,
   - `oa:` en cada semana.
6. Corre `python scripts/generar_docx.py <yaml>`. Corrige hasta que valide.
7. Muestra a Felipe un resumen semana a semana (tema + Bloom + evaluación) y avísale de cualquier riesgo, como una carga excesiva o un OA poco cubierto.
8. Haz commit con el yaml y el docx: `planificación: <curso> U<n> (borrador)`.
