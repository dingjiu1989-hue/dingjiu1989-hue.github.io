# SourceHub 数据中心

## Google Search Console 数据导出

每周一次，导出后放到这个目录，自动化系统会自动分析。

**导出步骤：**
1. 打开 [Google Search Console](https://search.google.com/search-console)
2. 左侧菜单 → "效果"
3. 右上角点击"导出"按钮
4. 选择 CSV 格式
5. 命名规范：
   - `gsc-queries-YYYY-MM-DD.csv` → 搜索查询报告
   - `gsc-pages-YYYY-MM-DD.csv` → 页面报告
6. 把 CSV 文件放到这个目录即可

**不需要手动操作：**
- 导出最近 28 天
- 包含所有维度

系统会在下次周度审计时自动读取和分析。
