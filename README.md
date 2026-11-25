# Planificación — Prof. Felipe Jiménez · Colegio San Agustín

Repo de trabajo para un agente (Claude) que analiza programas, planifica, registra clases y evaluaciones, y reestructura unidades.
Las reglas del agente están en [`CLAUDE.md`](CLAUDE.md) y el formato institucional en [`formato/FORMATO.md`](formato/FORMATO.md).

## Flujo

```
programa (OA) ──► /planificar-unidad ──► U<n>.yaml ──► .docx (formato UTP)
                                             ▲
clase ──► /registrar-clase ──► registros/    │
prueba ──► /analizar-evaluacion ──► logro ───┴── /reestructurar
```

## Uso desde el celular

Abre una sesión de Claude con este repo y pide, por ejemplo:

- `/registrar-clase 2M-fisica hoy vimos impulso, la mitad no entendió Δp, faltó el experimento`
- `/analizar-evaluacion 2M-fisica` (y adjunta el Excel de notas por pregunta)
- `/reestructurar 2M-fisica`

Los .docx se descargan desde `cursos/<curso>/planificaciones/docx/`.

## Generar a mano

```
pip install -r requirements.txt
python scripts/generar_docx.py cursos/2M-fisica/planificaciones/U3-energia-momentum.yaml
```

## Cursos

| Código | Programa | Planificaciones |
|---|---|---|
| `1M-biologia` | ✅ 8 OA · 54 indicadores | — |
| `1M-fisica` | ✅ 8 OA · 59 indicadores | — |
| `2M-biologia` | ✅ 8 OA · 47 indicadores | — |
| `2M-fisica` | ✅ 6 OA · 37 indicadores | U3 (piloto) |
| `5B-ciencias` | ✅ 14 OA · 78 indicadores | — |
| `6B-ciencias` | ✅ 18 OA · 95 indicadores | — |

Programas completos, incluido el eje Química, en `programas/<nivel>/`.
