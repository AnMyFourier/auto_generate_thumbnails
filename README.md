# auto_generate_thumbnails

A script which can auto generate one or more thumbnails using the setting you like. Also generate log file can distinct sucess, fail, duplicate...

批量自动生成缩略图脚本

Features: 

- 批量处理文件夹内所有视频文件
- 自定义排列模式与缩略图尺寸
- 根据排列模式自动检测, 等间隔取帧合成缩略图
- 支持显示进度条(tqdm), 打印生成错误文件信息
- 自动生成处理日志文件(错误日志记录会提到行首), 包括成功, 失败, 文件md5重复
- 根据MD5检测文件夹内的重复文件
- 文件夹文件拓展名groupby

## Background 背景

暂无好的现成服务能自动批量生成缩略图(potplayer能针对单文件自动生成缩略图,但无批量功能)

## Dependency 依赖

- FFmpeg, **请先自行安装**

  > windows: 请到 [FFmpeg官网](https://ffmpeg.org/download.html) 下载安装包, 自行安装
  >
  > MacOS: 使用homebrew 安装 `brew install ffmpeg`
  >
- pyhton 依赖
  `pip install -r ./requirements.txt`

## Run 运行

`python auto_generate_thumbnail.py `

## Params Setting 参数设置

![](https://anmy-md.oss-cn-guangzhou.aliyuncs.com/imgs/2024%2F20240131-d9b20ecb8ac60fe6b90e2959f872fa3f.webp)

参数设置如上, 仅供参考.  排列模式 `tile = 'nxm'` 请务必用x连接, 自动拆分使用 `split('x')`

## Log Example 日志示例

![](https://anmy-md.oss-cn-guangzhou.aliyuncs.com/imgs/2024%2F20240131-5ccfe66a0a7cbbd2e7a147067e83ca05.webp)

## TODO

* [ ] 手动删除缩略图, 自动检测删除对应源文件
* [ ] 不等间隔, 支持按权重取帧数(某段取更多帧)
* [ ] 成功, 失败, 重复, 未处理文件 --> 计数
* [ ] 更多文件类型支持
* [ ] 编写GUI
* [ ] 添加水印, 取帧加时间进度条

## Related Efforts 相关项目

* [FFmpeg](https://github.com/FFmpeg/FFmpeg) - FFmpeg is a collection of libraries and tools to process multimedia content such as audio, video, subtitles and related metadata.

## Maintainers 维护者

[@AnMy](https://github.com/AnMyFourier).
