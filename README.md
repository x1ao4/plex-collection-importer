# plex-collection-importer
使用 plex-collection-importer 可以将豆瓣、IMDb 和 Trakt 上的片单或其他本地片单导入您的 Plex 媒体库。脚本会通过网络片单或本地片单获取影片数据，然后与选定的库中的影片进行匹配，并将匹配成功的影片添加至与片单同名的合集中，从而实现导入片单的功能。

## 运行条件
- 安装了 Python 3.6 或更高版本。
- 安装了必要的第三方库：plexapi、BeautifulSoup。（可以通过 `pip3 install plexapi beautifulsoup4` 安装）
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
当 `collections` 文件夹为空文件夹时，脚本会自动启用导入网络片单模式，请运行 `plex-collection-importer.py` 脚本，根据提示进行操作，示例如下：
```
以下是您的Plex服务器上的所有影视库：

1. 电影
2. 动漫
3. 电视剧
4. 综艺

请输入您想选择的库的编号（多个编号请用空格隔开）：1

请输入片单的ID：39639105
请输入片单的类型（movie或tv）：movie

正在获取片单：小成本大创意

1 定时拍摄 (2014) {tmdb-273271}
2 爱的就是你 (2014) {tmdb-242090}
3 双重人格 (2013) {tmdb-146015}
4 追随 (1998) {tmdb-11660}
5 彗星来的那一夜 (2013) {tmdb-220289}
6 初始者 (2004) {tmdb-14337}
7 狗镇 (2003) {tmdb-553}
8 记忆碎片 (2000) {tmdb-77}
9 K星异客 (2001) {tmdb-167}
10 机械姬 (2014) {tmdb-264660}
11 摄影机不要停！ (2017) {tmdb-513434}

正在匹配库：电影

"双重人格 (2014)" 已被添加到 "小成本大创意" 合集中
"彗星来的那一夜 (2014)" 已被添加到 "小成本大创意" 合集中
"时光穿梭 (2015)" 已被添加到 "小成本大创意" 合集中
"机械姬 (2015)" 已被添加到 "小成本大创意" 合集中
"狗镇 (2003)" 已被添加到 "小成本大创意" 合集中
```
脚本目前支持导入豆瓣、IMDb 和 Trakt 上的片单，请从以上平台的片单地址中获取片单 ID，示例如下：
```
豆瓣片单的 ID 为纯数字，如下方地址的 ID 为 39639105
https://www.douban.com/doulist/39639105/

IMDb 片单的 ID 以 ls 开头，如下方地址的 ID 为 ls527593715
https://www.imdb.com/list/ls527593715/

Trakt 片单的 ID 包含用户名和 ID 两部分，请用空格隔开，如下方地址的 ID 为 callingjupiter best-movies-of-2023
https://trakt.tv/users/callingjupiter/lists/best-movies-of-2023?sort=added,desc
```

## 导入本地片单
当 `collections` 文件夹内包含 `.txt` 格式的片单时，脚本会自动启用导入本地片单模式，请运行 `plex-collection-importer.py` 脚本，根据提示进行操作，示例如下：
```
以下是您的Plex服务器上的所有影视库：

1. 电影
2. 动漫
3. 电视剧
4. 综艺

请输入您想选择的库的编号（多个编号请用空格隔开）：1

正在读取片单...

豆瓣电影 Top 250

正在匹配库：电影

"疯狂动物城 (2016)" 已被添加到 "豆瓣电影 Top 250" 合集中
"海上钢琴师 (1998)" 已被添加到 "豆瓣电影 Top 250" 合集中
"美丽人生 (1997)" 已被添加到 "豆瓣电影 Top 250" 合集中
"泰坦尼克号 (1997)" 已被添加到 "豆瓣电影 Top 250" 合集中
"肖申克的救赎 (1994)" 已被添加到 "豆瓣电影 Top 250" 合集中
```
若 `collections` 文件夹内包含多个片单文件，脚本会依次处理每个片单，片单需要按照 `序号 片名 (年份)` 的格式列出影片，也可增加 TMDB、IMDb 或 TVDB 的 ID，并按照 ` {平台-ID}` 的格式添加在行末（当使用片名与年份无法匹配影片时，若存在平台 ID，脚本会使用平台 ID 进行二次匹配，以此解决片单语言与库语言不一致或译名不同产生的匹配问题），示例如下：
```
1 肖申克的救赎 (1994) {tmdb-278}
2 霸王别姬 (1993) {tmdb-10997}
3 阿甘正传 (1994) {imdb-tt0109830}
4 泰坦尼克号 (1997)
5 这个杀手不太冷 (1994) {tvdb-234}
```
片单需要保存为 `.txt` 格式，文件名即为生成合集的名称。

## 工具
除了主脚本，我还为大家准备了一些小工具，用于单独获取、转换和编辑片单。
- get-douban-list

  此脚本是用来获取豆瓣片单的，运行脚本后提供片单 ID（并选择片单类型）即可将片单按指定的格式保存为同名的 `.txt` 片单，片单语言为中文。（在脚本内填写 `tmdb_api_key` 可为片单增加 TMDB ID 信息）
- get-imdb-list
  
  此脚本是用来获取 IMDb 片单的，运行脚本后提供片单 ID 即可将片单按指定的格式保存为同名的 `.txt` 片单，片单语言为英文。（包含 IMDb ID 信息）
- get-trakt-list
  
  此脚本是用来获取 Trakt 片单的，运行脚本后提供片单用户名和片单 ID（并选择片单类型）即可将片单按指定的格式保存为同名的 `.txt` 片单，片单语言为英文。（在脚本内填写 `tmdb_api_key` 可为片单增加 TMDB ID 信息）
- top-lists
  - douban-top-250
  
    此脚本是用来获取/更新「[豆瓣电影 Top 250](https://movie.douban.com/top250)」片单的，直接运行即可。（在脚本内填写 `tmdb_api_key` 可为片单增加 TMDB ID 信息）
  - imdb-top-250-movies
  
    此脚本是用来获取/更新「[IMDb Top 250 Movies](https://www.imdb.com/chart/top/)」片单的，直接运行即可。（包含 IMDb ID 信息）
  - imdb-top-250-tv-shows
  
    此脚本是用来获取/更新「[IMDb Top 250 TV Shows](https://www.imdb.com/chart/toptv/)」片单的，直接运行即可。（包含 IMDb ID 信息）
  - tspdt-1000-greatest-films
  
    此脚本是用来获取/更新「[TSPDT 1,000 Greatest Films](https://www.theyshootpictures.com/gf1000_all1000films_table.php)」片单的，直接运行即可。（在脚本内填写 `tmdb_api_key` 可为片单增加 TMDB ID 信息）
- add-tmdb-id

  此脚本是用来为没有平台 ID 信息的片单补充 TMDB ID 的，需要在脚本内填写您的 TMDB API 密钥（`tmdb_api_key`），并设置片单的类型（`media_type`）、匹配模式（`match_mode`）和语言（`language`）。请将需要处理的片单放在脚本所在文件夹内，运行脚本后新的片单会保存在文件夹内。
  - 片单的类型
    - movie：电影
    - tv：电视
  - 匹配模式
    - exact：精确匹配，只有当片名与年份完全一致时才算匹配成功，有可能导致匹配不到结果。
    - fuzzy：模糊匹配，将返回结果中排在第一位（相关度最高）的项目作为匹配结果，有可能匹配到错误的结果。
  - 片单的语言
    - language：请根据「[IETF 语言标签](https://www.venea.net/web/culture_code)」填写片单的语言代码，例如 'zh-CN' 或 'en-US'。
- translate-title

  此脚本是用来转换片单语言的，脚本会在 TMDB 上匹配片单内的影片，并将片名替换为 TMDB 上指定语言的译名，需要在脚本内填写您的 TMDB API 密钥（`tmdb_api_key`），并设置片单的类型（`media_type`）、匹配模式（`match_mode`）、原始语言（`input_language`）和输出语言（`output_language`）。请将需要处理的片单放在脚本所在文件夹内，运行脚本后新的片单会保存在文件夹内。
  - 片单的类型
    - movie：电影
    - tv：电视
  - 匹配模式
    - exact：精确匹配，只有当片名与年份完全一致时才算匹配成功，有可能导致匹配不到结果。
    - fuzzy：模糊匹配，将返回结果中排在第一位（相关度最高）的项目作为匹配结果，有可能匹配到错误的结果。
  - 原始片单的语言
    - input_language：请根据「IETF 语言标签」填写原始片单的语言代码，例如 'zh-CN' 或 'en-US'。
  - 输出片单的语言
    - output_language：请根据「IETF 语言标签」填写输出片单的语言代码，例如 'zh-CN' 或 'en-US'。

## 注意事项
- 请确保您提供了正确的 Plex 服务器地址和 X-Plex-Token。
- 请确保运行脚本的设备可以连接到您的服务器。
- 由于 TMDB API 有速率限制，建议在脚本运行过程中不要进行其他与 TMDB API 相关的操作，以免触发速率限制。
- 部分地区可能会由于网络原因造成 TMDB API 调用失败，无法运行脚本，请确保您的网络环境可以正常调用 TMDB API。
- `collections` 文件夹内包含 4 个预置片单，直接运行脚本将直接导入这 4 个片单，若不需要请删除文件或将它们移走。
- 请不要删除 `collections` 和 `downloads` 文件夹。

## 已知问题
- 没有提供匹配模式选择功能的脚本均采用了模糊匹配的方式在 TMDB 进行匹配，若您使用了 TMDB 匹配的相关功能，在某些情况下可能会出现匹配错误的问题。
- 主脚本会优先使用片单中的片名和年份与库中影片进行匹配，若片单语言与库的语言不一致，片单中又不包含平台 ID 信息，将无法匹配任何影片。
- 只有当使用片单中的片名和年份与库中影片匹配失败时，脚本才会使用平台 ID （若存在）进行二次匹配。
- 若网络片单名称中包含 `:*?"<>|/` 等符号，这些符号将在合集或片单文件名中被删除。
- 若您的库中存在大量挂载的网盘文件，有可能导致脚本运行速度变慢或连接超时，请推出挂载再运行脚本，之后再重新挂载网盘即可。
<br>

# plex-collection-importer
The plex-collection-importer is a tool that allows you to import movie or TV show lists from Douban, IMDb, Trakt, or local lists into your Plex media library. The script fetches movie (TV show) data from the specified platforms or local files, matches them with the selected Plex library, and adds the successfully matched movies (TV shows) to a collection with the same name as the list.

## Requirements
- Installed Python 3.6 or higher.
- Installed required third-party libraries: plexapi, BeautifulSoup. (Install with `pip3 install plexapi beautifulsoup4`)
- Have an available TMDb API (TMDb API can be applied for free in TMDb account settings, optional).

## Config
Before running the script, open the `config.ini` file, and fill in your Plex server address (`address`) and [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) (`token`). If you want to add TMDB ID information during list retrieval (useful for resolving language or translation differences), provide your TMDB API key (`tmdb_api_key`); leave it blank if not needed.
```
[server]
address = http://127.0.0.1:32400
token = 
tmdb_api_key = 
```

## Importing from Online Lists
When the `collections` folder is empty, the script will automatically enable online list import mode. Run the `plex-collection-importer.py` script and follow the prompts. Here's an example:
```
Here are all the MOVIE and TV libraries on your Plex server: 

1. Movies
2. Anime
3. TV Shows
4. Variety Shows

Please enter the number of the library you want to select (separate multiple numbers with spaces): 1

Please enter the ID of the list: x1ao4 low-budget-big-ideas
Please enter the type of the list (movie or tv): movie

Fetching list: Low Budget, Big Ideas

1 Time Lapse (2014) {tmdb-273271}
2 The One I Love (2014) {tmdb-242090}
3 The Double (2014) {tmdb-146015}
4 Following (1999) {tmdb-11660}
5 Coherence (2014) {tmdb-220289}
6 Primer (2004) {tmdb-14337}
7 Dogville (2003) {tmdb-553}
8 Memento (2001) {tmdb-77}
9 K-PAX (2001) {tmdb-167}
10 Ex Machina (2015) {tmdb-264660}
11 One Cut of the Dead (2017) {tmdb-513434}

Matching library: Movies

"Coherence (2014)" has been added to the "Low Budget, Big Ideas" collection
"Dogville (2003)" has been added to the "Low Budget, Big Ideas" collection
"Following (1999)" has been added to the "Low Budget, Big Ideas" collection
"Memento (2000)" has been added to the "Low Budget, Big Ideas" collection
"The One I Love (2014)" has been added to the "Low Budget, Big Ideas" collection
```
The script supports importing lists from Douban, IMDb, and Trakt. Obtain the list ID from the respective platforms as shown below:
```
Douban list ID is a pure number, for example, the ID in the following URL is 39639105
https://www.douban.com/doulist/39639105/

IMDb list ID starts with ls, for example, the ID in the following URL is ls527593715
https://www.imdb.com/list/ls527593715/

Trakt list ID contains both username and ID, separated by a space. For example, the ID in the following URL is callingjupiter best-movies-of-2023
https://trakt.tv/users/callingjupiter/lists/best-movies-of-2023?sort=added,desc
```

## Importing from Local Lists
When the `collections` folder contains `.txt` format lists, the script will automatically enable local list import mode. Run the `plex-collection-importer.py` script and follow the prompts. Here's an example:
```
Here are all the MOVIE and TV libraries on your Plex server: 

1. Movies
2. Anime
3. TV Shows
4. Variety Shows

Please enter the number of the library you want to select (separate multiple numbers with spaces): 1

Reading the list...

DOUBAN Top 250 Movies

Matching library: Movies

"The Shawshank Redemption (1994)" has been added to the "DOUBAN Top 250 Movies" collection
"Spider-Man: Into the Spider-Verse (2018)" has been added to the "DOUBAN Top 250 Movies" collection
"Titanic (1997)" has been added to the "DOUBAN Top 250 Movies" collection
"The Truman Show (1998)" has been added to the "DOUBAN Top 250 Movies" collection
"Zootopia (2016)" has been added to the "DOUBAN Top 250 Movies" collection
```
If the `collections` folder contains multiple list files, the script will process each list sequentially. Lists should follow the format `Number Title (Year) {platform-ID}`, where the platform ID is optional but useful for resolving language or translation differences. Here's an example:
```
1 The Shawshank Redemption (1994) {tmdb-278}
2 Farewell My Concubine (1993) {tmdb-10997}
3 Forrest Gump (1994) {imdb-tt0109830}
4 Titanic (1997)
5 Léon: The Professional (1994) {tvdb-234}
```
Save lists in `.txt` format, and the filename becomes the collection name.

## Tools
In addition to the main script, some auxiliary tools are available for specific tasks:
- get-douban-list

  Fetches Douban lists and saves them as `.txt` files in the specified format. Run the script, provide the list ID (and type), and it will generate a list file. (Adding TMDB ID is optional; include `tmdb_api_key` in the script)
- get-imdb-list
  
  Fetches IMDb lists and saves them as `.txt` files in the specified format. Run the script, provide the list ID, and it will generate a list file. (Includes IMDb ID)
- get-trakt-list
  
  Fetches Trakt lists and saves them as `.txt` files in the specified format. Run the script, provide the username and list ID (and type), and it will generate a list file. (Adding TMDB ID is optional; include `tmdb_api_key` in the script)
- top-lists
  - douban-top-250
  
    Fetches or updates the "[DOUBAN Top 250 Movies](https://movie.douban.com/top250)" list. Run the script to update. (Adding TMDB ID is optional; include `tmdb_api_key` in the script)
  - imdb-top-250-movies
  
    Fetches or updates the "[IMDb Top 250 Movies](https://www.imdb.com/chart/top/)" list. Run the script to update. (Includes IMDb ID)
  - imdb-top-250-tv-shows
  
    Fetches or updates the "[IMDb Top 250 TV Shows](https://www.imdb.com/chart/toptv/)" list. Run the script to update. (Includes IMDb ID)
  - tspdt-1000-greatest-films
  
    Fetches or updates the "[TSPDT 1,000 Greatest Films](https://www.theyshootpictures.com/gf1000_all1000films_table.php)" list. Run the script to update. (Adding TMDB ID is optional; include `tmdb_api_key` in the script)
- add-tmdb-id

  Adds TMDB ID to lists without platform ID information. Configure the script with your TMDB API key (`tmdb_api_key`), list type (`media_type`), matching mode (`match_mode`), and language (`language`). Place lists in the script folder, run it, and the new list will be saved in the same folder.
  - List type
    - movie: Movies
    - tv: TV Shows
  - Matching mode
    - exact: Exact matching, only considered a successful match when both the title and the year are identical, which may result in no matches if there is any deviation.
    - fuzzy: Fuzzy matching, returns the top-ranked item in the results (highest relevance) as the match, which may lead to incorrect matches.
  - List language
    - language: Use the "[IETF Language Tags](https://www.venea.net/web/culture_code)" code, such as 'zh-CN' or 'en-US'.
- translate-title

  Translates list language. The script matches movie names on TMDB and replaces them with the translated title in the specified language. Configure the script with your TMDB API key (`tmdb_api_key`), list type (`media_type`), matching mode (`match_mode`), original language (`input_language`), and output language (`output_language`). Place lists in the script folder, run it, and the new list will be saved in the same folder.
  - List type
    - movie: Movies
    - tv: TV Shows
  - Matching mode
    - exact: Exact matching, only considered a successful match when both the title and the year are identical, which may result in no matches if there is any deviation.
    - fuzzy: Fuzzy matching, returns the top-ranked item in the results (highest relevance) as the match, which may lead to incorrect matches.
  - Original list language
    - input_language: Use the "IETF Language Tags" code, such as 'zh-CN' or 'en-US'.
  - Output list language
    - output_language: Use the "IETF Language Tags" code, such as 'zh-CN' or 'en-US'.

## Notes
- Make sure you've provided the correct Plex server address and X-Plex-Token.
- Make sure the device running the script is connected to your Plex server.
- Due to rate limits on the TMDB API, it is recommended not to perform other TMDB API-related operations during the script execution to avoid rate limit triggers.
- Some regions may experience TMDB API call failures due to network reasons. Ensure that your network environment can make TMDB API calls.
- The `collections` folder contains 4 pre-set lists; running the script will import these lists. Remove or move them if not needed.
- Do not delete the `collections` and `downloads` folders.

## Known Issues
- Scripts without a matching mode selection option use fuzzy matching on TMDB, which may result in incorrect matches in some cases.
- The main script prioritizes matching with the title and year in the list. If the list language differs from the library language and the list doesn't include a platform ID, no matches will occur.
- Platform ID is only used for a secondary match when the primary match with the title and year fails.
- If the online list name contains `:*?"<>|/` symbols, these symbols will be removed in the collection or list file name.
- If your library contains a large number of mounted cloud files, it might slow down the script or cause connection timeouts. Quit mounting, run the script, and then remount the cloud to resolve.
