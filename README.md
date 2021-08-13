# [Метод анализа иерархий](https://en.wikipedia.org/wiki/Analytic_hierarchy_process)

## Использование

```bash
pip install -r -U requirements.txt
python multicrit.py config.json
```

## Конфигурация

Пример [файла конфигурации](example.json), его структура следующая:

```json
{
  "criteria": {
    "c1": [cw1, [wa1c1, wa2c1, wa3c1]],
    "c2": [cw2, [wa1c2, wa2c2, wa3c2]]
  },
  "alternatives": ["a1", "a2", "a3"]
}
```

- `ci` названия i-го критерия;
- `cwi` важность i-го критерия критерия [1..9];
- `waicj` важность j-го критерия для i-ой альтернативы;
- `ai` название i-ой альтернативы.

## Мотивация

Возможность выбора автомобиля, гостиницы, шавермы и прочего языком математики.
