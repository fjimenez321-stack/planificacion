---
description: Analiza resultados de una evaluación y calcula el logro por OA o indicador
argument-hint: <curso> <archivo.csv o datos pegados>
---
Analiza esta evaluación: $ARGUMENTS

1. Si los datos vienen pegados o en Excel, conviértelos al formato de `cursos/<curso>/evaluaciones/_plantilla.csv`. Reemplaza los nombres por códigos (Regla 3) y guarda el archivo como `cursos/<curso>/evaluaciones/<AAAA-MM-DD>-<nombre>.csv`.
2. Si la tabla de especificaciones (qué pregunta mide qué OA o indicador) no viene, pídela. Sin ella, solo puedes informar el logro global.
3. Calcula con código (Python), no a ojo:
   - el logro por pregunta, por indicador y por OA (% de puntaje obtenido sobre el puntaje máximo),
   - la distribución de logro por alumno (cuántos quedan bajo el 60 %),
   - las preguntas con peor rendimiento y, si hay datos de alternativas, los distractores más elegidos.
4. Clasifica cada OA o indicador según los umbrales de `CLAUDE.md` (≥80 / 60–79 / <60).
5. Escribe `cursos/<curso>/evaluaciones/<mismo-nombre>.md` con el informe: tabla de logro, hallazgos y la hipótesis didáctica de cada caso bajo el umbral.
6. Muestra a Felipe un resumen breve y propón el ajuste concreto. Si algo cae bajo el 60 %, sugiere `/reestructurar`.
7. Haz commit con el csv y el informe: `evaluación: <curso> <nombre> (logro global X %)`.
