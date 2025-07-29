
import streamlit as st

def main():
    st.title("🚀 MCPStore 测试")
    st.write("如果您能看到这个页面，说明基本功能正常。")
    
    # 侧边栏测试
    with st.sidebar:
        st.header("侧边栏测试")
        if st.button("测试按钮"):
            st.success("按钮点击成功！")
    
    # 主内容测试
    st.header("主内容区域")
    st.info("这是一个最小化的测试页面")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("测试指标1", 100)
    with col2:
        st.metric("测试指标2", 200)

if __name__ == "__main__":
    main()
