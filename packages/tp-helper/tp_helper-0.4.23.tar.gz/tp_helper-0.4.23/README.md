# TP Helper

Collection of common practices used in Transpropusk's projects.


## Установка:
`poetry add tp-helper`

## Очистка при обновлении
- `poetry cache clear --all PyPI`
- `poetry update`
- `poetry add tp-helper`


## Публикация:
Собирает и загружает собранный пакет в PyPI.

`poetry publish --build`