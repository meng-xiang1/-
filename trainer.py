import streamlit as st
from openai import OpenAI

# ① 连接 DeepSeek
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_KEY"],
    base_url="https://api.deepseek.com"
)

# ② 教练的"大脑"(系统提示)
系统提示 = """你是一名有10年经验的私人健身教练,专门帮学员制定科学、可执行的训练计划。

请根据学员的情况,生成一份完整的训练计划。

【计划格式要求】
- 按训练日分块(第1天 / 第2天 ...)
- 每个动作写明:动作名 | 练的部位 | 组数 × 次数
- 给出组间休息的建议
- 最后附上 2~3 条饮食或恢复建议

【风格】专业、亲切、鼓励人,像一个真正的教练。提醒学员循序渐进、量力而行。"""

# ③ 网页标题
st.title("🏋️ AI 训练计划生成器")
st.caption("填一下你的情况,几秒钟生成一份专属训练计划")

# ④ 一个表单,收集学员信息
with st.form("plan_form"):
    左, 右 = st.columns(2)          # 分两列,好看

    with 左:
        目标 = st.selectbox("你的目标", ["增肌", "减脂", "塑形", "提升体能"])
        水平 = st.selectbox("你的水平", ["完全新手", "练过一阵", "老手"])
        频率 = st.slider("每周训练次数", 1, 7, 3)

    with 右:
        时长 = st.selectbox("每次训练时长", ["30分钟", "45分钟", "1小时", "1.5小时"])
        场地 = st.selectbox("在哪练", ["健身房(器械齐全)", "家里(有一对哑铃)", "家里(无器械)"])
        伤病 = st.text_input("有无伤病或不适?(没有就留空)")

    提交 = st.form_submit_button("生成训练计划")

# ⑤ 用户点"生成"之后
if 提交:
    情况 = f"""学员情况如下:
- 目标:{目标}
- 水平:{水平}
- 每周训练 {频率} 次,每次 {时长}
- 训练场地:{场地}
- 伤病情况:{伤病 if 伤病 else "无"}"""

    with st.spinner("正在为你定制计划,请稍等..."):
        回复 = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": 系统提示},
                {"role": "user", "content": 情况}
            ]
        )
        计划 = 回复.choices[0].message.content

    st.success("你的专属计划来啦!💪")
    st.markdown(计划)

    st.download_button(
        label="📥 下载这份计划",
        data=计划,
        file_name="我的训练计划.md"
    )