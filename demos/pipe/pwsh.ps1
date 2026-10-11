Select-String -Path log.txt -Pattern ERROR | Measure-Object | Select-Object -ExpandProperty Count
