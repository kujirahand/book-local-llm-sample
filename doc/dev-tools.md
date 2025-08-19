# 本書サンプルを動かすために

本書では、ローカル環境でLLMを動かすための開発環境を構築する方法を紹介します。
以下の手順に従って、必要なツールをインストールしていきましょう。

## Ollamaのインストール

Ollamaは、ローカルでLLMを動かすためのツールです。公式サイトからインストーラーをダウンロードしてインストールします。

```
Ollama
[URL] https://ollama.com/
```

## WSLをインストールしよう

WindowsにWSLをインストールすることで、Linux環境を手軽に利用できます。PowerShellを管理者権限で起動して、下記のコマンドを実行しましょう。WSLをインストールしたら、Microsoft StoreからUbuntu 24をインストールします。

```sh
# WSLをインストールする
$ wsl --install
# WSLのバージョンを確認しよう
$ wsl --list --verbose
```

## Pythonのインストール / pyenv / venv

本書では、Pythonを利用したプログラムを多く紹介しています。Pythonは、公式サイトからインストーラーをダウンロードしてインストールできますが、本書の場合、Pythonのバージョンを細かく指定して実行する必要があるため、手軽にPythonのバージョンを切り替えられる「pyenv」を利用することを推奨しています。pyenvについては、以下のURLでインストール方法が案内されています。

```
GitHub > pyenv
[URL] https://github.com/pyenv/pyenv
```

## Dockerのインストール

本書の一部で、Dockerを利用したプログラムを紹介しています。Dockerはコンテナ仮想化を用いてアプリを実行するためのプラットフォームです。次のURLからインストーラーを利用して、インストールできます。

```
Docker
[URL] https://www.docker.com/ja-jp/
```

## Visual Studio Codeのインストール

Visual Studio Codeは、Microsoftが提供する無料のコードエディタです。多くのプログラミング言語に対応しており、拡張機能を追加することで機能を拡張できます。次のURLからインストーラーをダウンロードしてインストールしましょう。Windows/macOS/Linuxのいずれでも利用できます。

```
Visual Studio Code
[URL] https://code.visualstudio.com/
```
