# 学习通\智慧职教刷课脚本
采用中间人攻击，实现一秒看一个视频的效果

##安装依赖
```bash: pip install requirements.txt```

##导入mitproxy的证书，然后浏览器设置代理端口为8080

## 运行学习通脚本：
```bash: mitmdump -s xuexitong_proxy_modifier.py -p 8080```
## 运行智慧职教脚本
```bash: mitmdump -s zhijiao_proxyer.py -p 8080```
