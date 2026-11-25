---
description: Reestructura las próximas semanas según los registros y las evaluaciones
argument-hint: <curso> [motivo]
---
Reestructura la planificación vigente de: $ARGUMENTS

1. Carga el `.yaml` vigente del curso, `programa/oa.md`, los registros desde el último cambio, los informes de evaluación y `cambios.md`.
2. Arma el diagnóstico con evidencia citada (Regla 4):
   - lo planificado vs. lo realizado (semanas atrasadas o actividades sin hacer),
   - el logro por OA o indicador y su umbral,
   - las fechas fijas que no se pueden mover.
3. Propón **una** reestructuración (y, como mucho, una alternativa) que:
   - solo modifique semanas futuras, porque las pasadas quedan como historia,
   - mantenga cubiertos todos los OA de la unidad; si algo no cabe, dilo explícitamente,
   - conserve la progresión Bloom,
   - use actividades distintas a las que fallaron.
4. **Muestra la propuesta antes de aplicarla**: una tabla de antes y después de las semanas afectadas, más el porqué. Espera el visto bueno de Felipe.
5. Cuando la apruebe:
   - edita el `.yaml` y sube `version`,
   - regenera el docx con `scripts/generar_docx.py`,
   - agrega una entrada en `cursos/<curso>/cambios.md` (fecha, versión, evidencia y cambio),
   - haz commit: `reestructura: <curso> U<n> v<k> — <motivo corto>`.
