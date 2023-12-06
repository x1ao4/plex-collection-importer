# plex-collection-importer
使用 plex-collection-importer 可以将豆瓣、IMDb 和 Trakt 上的片单或其他本地片单导入您的 Plex 媒体库。脚本会通过网络片单或本地片单获取影片数据，然后与选定的库中的影片进行匹配，并将匹配成功的影片添加至与片单同名的合集中，从而实现导入片单的功能。

## 运行条件
- 安装了 Python 3.6 或更高版本。
- 安装了必要的第三方库：plexapi。
- 有可用的 TMDB API。（TMDB API 可在 TMDB 账号设置中免费申请，此项为可选项）

## 配置文件
在运行脚本前，请先打开配置文件 `config.ini`，填写您的 Plex 服务器地址（`address`）和 [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)（`token`）。若您需要在获取片单时为影片增加 TMDB ID 信息（当使用片名与年份无法匹配影片时，若存在 TMDB ID，脚本会使用 TMDB ID 进行二次匹配，以此解决片单语言与库语言不一致或译名不同产生的匹配问题），请填写您的 TMDB API 密钥（`tmdb_api_key`）；若不需要增加 TMDB ID 信息，将 `tmdb_api_key` 留空即可。
```
[server]
address = http://127.0.0.1:32400
token = 
tmdb_api_key = 
```

## 导入网络片单
当 `collections` 文件夹为空文件夹时，脚本会自动进入**导入网络片单模式**。
