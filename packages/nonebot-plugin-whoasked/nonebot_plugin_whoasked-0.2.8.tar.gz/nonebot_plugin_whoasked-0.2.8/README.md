# 谁问你了？

一个用于查询谁@了你或引用了你的消息的NoneBot2插件

插件名：`nonebot-plugin-whoasked`

## 功能

- 记录群聊中的@消息和引用消息，并通过命令查询谁@了你或引用了你的消息

## 安装

使用nb-cli安装：

```bash
nb plugin install nonebot-plugin-whoasked
```

## 配置

在.env文件中添加以下配置（可选）：

```bash
# 最大返回消息数量，默认25，最大值100
WHOASKED_MAX_MESSAGES=25

# 消息存储天数，默认3，最大值30
WHOASKED_STORAGE_DAYS=3

# 自定义触发关键词
# 配置示例：WHOASKED_KEYWORDS=["谁问我了","who"]
WHOASKED_KEYWORDS=["谁问我了"]

# 是否在消息开头加上消息发送者头像, 默认关闭
# 在使用Napcat作为协议端的情况下, 消息中会正常显示消息发送者头像和昵称
# 由于部分协议端暂不支持伪造转发, 所以增加此配置
WHOASKED_SHOW_AVATAR=False

# 消息发送者头像大小, 可用值: 40/160，仅在`WHOASKED_SHOW_AVATAR=True`时生效
WHOASKED_SHOW_AVATAR_SIZE=40

```

## 使用

在群聊中发送以下命令：
> [!WARNING]
> 此处示例中的"/"为 nb 默认的命令开始标志，若您设置了另外的标志，则请使用您设置的标志作为命令的开头

- /谁问我了

## 注意事项
- 该插件代码基本由AI完成，如有更好的改进建议欢迎提交pr
- 目前仅使用了`OnebotV11适配器+Napcat/Lagrange`，在Windows/Linux系统下测试通过，如有兼容性问题欢迎提交issue


## TODO
- [ ] 将数据存储迁移至数据库

## 更新日志

### 0.2.8
优化头像显示模式下的展示效果

### 0.2.7
添加头像显示([PR #3](https://github.com/enKl03B/nonebot-plugin-whoasked/pull/3))

### 0.2.6
尝试利用伪造转发以实现更好的消息展示

### 0.2.5
触发关键词可自定义([Issue #1](https://github.com/enKl03B/nonebot-plugin-whoasked/issues/1#issuecomment-2955470018))

### 0.2.4
新增CQ码过滤，分离日志过滤器

### 0.2.3
优化日志输出和消息记录
> [!IMPORTANT]
> 自该版本起，消息记录完成后将不再展示完成日志，可自行查看`message_records.json`文件以确定是否成功记录。

### 0.2.2
优化引用消息展示形式
> [!IMPORTANT]
> 自该版本起，`WHOASKED_MAX_MESSAGES`的默认值将更改为25

### 0.2.0、0.2.1.1
修复了一些体验问题

### 0.1.3.3
修复已知Bug

### 0.1.3
更新依赖版本，优化导入

### 0.1.2
更改插件以符合规范

### 0.1.1
修改元数据的一处描述错误

### 0.1.0
初次发布


## 鸣谢
- [NoneBot2](https://github.com/nonebot/nonebot2) - 跨平台 Python 异步机器人框架
- [noneBot-plugin-localStore](https://github.com/nonebot/plugin-localstore) - 实现本地数据存储 


以及所有未提及的相关项目❤

## 许可证

MIT
