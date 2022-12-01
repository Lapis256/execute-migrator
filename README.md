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
execute_migrator text 'execute @e[name=\"test entity\"] ~~~ detect ~~-1~ stone 0 say Hello world!!'

// 結果
// execute as @e[name="test entity"] at @s positioned ~ ~ ~ if block ~ ~-1 ~ stone 0 run say Hello world!!
```

## function
指定した .mcfunction ファイル内の execute コマンドを新しい物に置き換えます。
```
execute_migrator function <file path>
```
`--output`、`-o`オプションで、出力先ファイルを指定できます。
指定しない場合は、上書きします。
```
execute_migrator function -o <file path> <file path>
```

## functions
指定したディレクトリ内にある .mcfunction ファイル内の execute コマンドを新しい物に置き換えます。
```
execute_migrator functions <directory path>
```
`--output`、`-o`オプションで、出力先ディレクトリを指定できます。
指定しない場合は、上書きします。
```
execute_migrator function -o <directory path> <directory path>
```
