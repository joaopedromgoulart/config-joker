## 0.7.0 (2023-06-16)

### Feat

- **python-v**: ajuste de versao para 3.7

## 0.6.0 (2023-05-26)

### Feat

- **sources.source.SourceAsDict**: Add config extraction from list of dicts
- **config.Config**: Add cast string to bool

### Fix

- **requirements**: lower pyyaml version

## 0.5.0 (2023-05-17)

### Feat

- **sources.json**: add source para arquivos json

### Fix

- **sources.yamlfile**: Fix file load

### Refactor

- **sources.source-sources.yamlfile**: Base class to sources thet cam be transformed to dicts

## 0.4.0 (2023-05-17)

### Feat

- **yamlfile.YamlFileSource**: add possibilidade de apontar para paths conplexos para buscar configuracoes

## 0.3.0 (2023-05-05)

### Feat

- **config_joker**: Add import of Config and source classes from root folder

## [0.2.0] - 2023-04-11

### Feat

- **sources.yamlfile.YamlFileSource**: Add complex path search to find values inside neasted dicts and lists
- **sources.yamlfile**: Add new source YamlFileSource
- **sources.source.SourceResponse**: Replace the pydantic implemantation with a dataclass implementation (Remove pyndantic dependency)
