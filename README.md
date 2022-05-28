# execute-migrator
execute コマンドを新しい記法へと移行するツールです。

# 導入
## 依存関係
Python 3.8 以上

## インストール
```
pip install git+https://github.com/Lapis256/execute-migrator.git
```

# 使い方
## text
```
execute_migrator text <コマンド>
```
サンプル
```
execute_migrator text 'execute @e[name=\"test entity\"] ~~~ say Hello world!!'

// 結果
// execute as @e[name="test entity"] at @s positioned ~ ~ ~ run say Hello world!!
```

## mcfunction[WIP]
```
execute_migrator mcfunction <file path>
```
