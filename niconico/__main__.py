# niconico.py - Main

from sys import stdout, stderr, argv
import logging

from json import dump

try:
    from niconico import NicoNico, Cookies
except ImportError:
    from sys import path as spath
    spath.insert(0, __file__[:-20])
    from niconico import NicoNico, Cookies


def set_stdout_logger(name=None):
    "標準出力をするように指定された名前のLoggerを設定する。"
    # FROM: https://techblog.sasashima.works/archives/229
    stdout_handler = logging.StreamHandler(stream=stdout)
    stdout_handler.setFormatter(fmt:=logging.Formatter("[%(levelname)s] %(message)s"))
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    stderr_handler = logging.StreamHandler(stream=stderr)
    stderr_handler.setFormatter(fmt)
    stderr_handler.setLevel(logging.WARNING)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)


if __name__ == "__main__":
    HELP = """# ニコニコスクレイピングツール
ニコニコから様々なデータを取り出すためのツールです。
ニコニコ動画から動画をダウンロードしたりすることができます。

## 使用方法
コマンドの使用方法です。
もし自分で用意したニコニコ動画等でのクッキーがある場合は`--cookies クッキーのファイル`のようにしてください。
クッキーのファイルはNetscapeのフォーマットに準拠している必要があります。
また、ログ出力をして欲しい場合は

### `niconico help`
このメッセージを表示します。

### `niconico video <URL> download/json`
渡されたニコニコ動画のURLの動画をダウンロードまたは情報をJSON形式で出力します。

* `download` - mp4形式で動画をダウンロードします。`動画ID.mp4`のように保存されます。
* `json` - `動画ID.json`という名前のファイルを作り、そこにJSON形式で動画情報を出力します。

## このツールについて
Pythonのニコニコの非公式スクレイピング用のライブラリである`niconico.py`に付属しているツールです。
このツールを使用して何か損害等が起きても開発者は一切責任を負いません。
このツールを使用してから起きること全てを受け入れてください。"""
    args = argv[2:] if argv[0].startswith("py") else argv[1:]
    text, logger = " ".join(args), logging.getLogger("niconico.py")
    set_stdout_logger("niconico.py")

    cookies = None
    for i, arg in enumerate(args):
        if arg == "--cookies":
            # クッキーが指定されていればパスを取り出す。
            cookies = Cookies.from_file(args[i+1])
            del args[i], args[i+1]

    if (length := len(args)) >= 1 and args[0] != "help":
        client = NicoNico(cookies)
        del cookies
        if args[0] == "video" and length == 3:
            video = client.video.get_video(args[1])

            if "download" in args[2]:
                video._download_log = lambda x: print(f"[INFO] {x}\r", end="")
                with video as video:
                    video.download(f"{video.video.id}.mp4")
            else:
                logger.info("Writing json...")
                with open(f"{video.video.id}.json", "w") as f:
                    dump(video.data, f, ensure_ascii=False, indent=2)
                logger.info("Done")

            exit()
    else:
        print(HELP)
        exit()

    print("使用方法が違います。\n`niconico help`で使用方法を確認することができます。")