"""
工具管理页面
"""

import streamlit as st
from typing import Dict, List
import json

from utils.helpers import (
    show_success_message, show_error_message, show_info_message,
    create_dynamic_form, format_tool_result, format_json
)

def show():
    """显示工具管理页面"""
    st.header("🔧 工具管理")
    
    # 创建标签页
    tab1, tab2, tab3 = st.tabs(["📋 工具列表", "🧪 工具测试", "📊 使用统计"])
    
    with tab1:
        show_tool_list()
    
    with tab2:
        show_tool_tester()
    
    with tab3:
        show_tool_statistics()

def show_tool_list():
    """显示工具列表"""
    st.subheader("📋 可用工具")
    
    # 操作按钮
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 刷新工具", key="tool_refresh_list"):
            st.rerun()
    
    with col2:
        show_all = st.checkbox("显示所有服务工具", value=True)
    
    # 获取工具列表
    api_client = st.session_state.api_client
    response = api_client.list_tools()
    
    if not response:
        show_error_message("无法获取工具列表")
        return
    
    tools = response.get('data', [])
    
    if not tools:
        st.info("暂无可用工具")
        return
    
    # 工具统计
    st.metric("工具总数", len(tools))
    
    # 按服务分组显示
    tools_by_service = {}
    for tool in tools:
        service_name = tool.get('service_name', 'Unknown')
        if service_name not in tools_by_service:
            tools_by_service[service_name] = []
        tools_by_service[service_name].append(tool)
    
    # 搜索和过滤
    search_term = st.text_input("🔍 搜索工具", placeholder="输入工具名称或描述关键词")
    
    for service_name, service_tools in tools_by_service.items():
        with st.expander(f"🛠️ {service_name} ({len(service_tools)} 个工具)", expanded=True):
            
            # 过滤工具
            filtered_tools = service_tools
            if search_term:
                filtered_tools = [
                    tool for tool in service_tools
                    if search_term.lower() in tool.get('name', '').lower() or
                       search_term.lower() in tool.get('description', '').lower()
                ]
            
            if not filtered_tools:
                st.info("没有匹配的工具")
                continue
            
            for tool in filtered_tools:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**🔧 {tool.get('name', 'Unknown')}**")
                        st.caption(tool.get('description', 'No description'))
                    
                    with col2:
                        # 显示参数数量
                        schema = tool.get('inputSchema', {})
                        param_count = len(schema.get('properties', {}))
                        st.metric("参数", param_count)
                    
                    with col3:
                        if st.button("🧪 测试", key=f"test_{tool.get('name')}"):
                            st.session_state.selected_tool = tool
                            st.rerun()
                    
                    st.markdown("---")

def show_tool_tester():
    """显示工具测试页面"""
    st.subheader("🧪 工具测试")
    
    # 工具选择
    api_client = st.session_state.api_client
    response = api_client.list_tools()
    
    if not response:
        show_error_message("无法获取工具列表")
        return
    
    tools = response.get('data', [])
    
    if not tools:
        st.info("暂无可用工具")
        return
    
    # 选择工具
    selected_tool = st.session_state.get('selected_tool')
    
    if not selected_tool:
        # 工具选择器
        tool_options = {f"{tool.get('name')} ({tool.get('service_name')})": tool for tool in tools}
        selected_option = st.selectbox(
            "选择要测试的工具",
            options=list(tool_options.keys()),
            index=0 if tool_options else None
        )
        
        if selected_option:
            selected_tool = tool_options[selected_option]
            st.session_state.selected_tool = selected_tool
    
    if selected_tool:
        st.markdown(f"### 🔧 {selected_tool.get('name')}")
        st.markdown(f"**服务**: {selected_tool.get('service_name')}")
        st.markdown(f"**描述**: {selected_tool.get('description', 'No description')}")
        
        # 显示工具schema
        schema = selected_tool.get('inputSchema', {})
        
        if schema:
            with st.expander("📋 参数结构"):
                st.code(format_json(schema), language='json')
        
        # 动态表单
        form_data = create_dynamic_form(selected_tool.get('name'), schema)
        
        if form_data is not None:
            # 执行工具
            with st.spinner("执行工具中..."):
                result = execute_tool(selected_tool.get('name'), form_data)
                
                if result:
                    st.success("✅ 工具执行成功！")
                    
                    # 显示结果
                    st.markdown("#### 📊 执行结果")
                    
                    if isinstance(result, dict) and 'data' in result:
                        tool_result = result['data']
                        formatted_result = format_tool_result(tool_result)
                        
                        # 结果展示选项
                        result_format = st.radio(
                            "结果格式",
                            ["格式化", "原始JSON"],
                            horizontal=True
                        )
                        
                        if result_format == "格式化":
                            if isinstance(tool_result, (dict, list)):
                                st.json(tool_result)
                            else:
                                st.text(str(tool_result))
                        else:
                            st.code(formatted_result, language='json')
                    else:
                        st.text(str(result))
                    
                    # 保存到历史
                    save_to_history(selected_tool.get('name'), form_data, result)
        
        # 清除选择按钮
        if st.button("🔄 选择其他工具", key="tool_select_other"):
            if 'selected_tool' in st.session_state:
                del st.session_state.selected_tool
            st.rerun()

def show_tool_statistics():
    """显示工具使用统计"""
    st.subheader("📊 工具使用统计")
    
    # 获取历史记录
    history = st.session_state.get('tool_history', [])
    
    if not history:
        st.info("暂无工具使用记录")
        return
    
    # 统计信息
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总执行次数", len(history))
    
    with col2:
        unique_tools = len(set(record['tool_name'] for record in history))
        st.metric("使用过的工具", unique_tools)
    
    with col3:
        success_count = sum(1 for record in history if record.get('success', False))
        success_rate = (success_count / len(history)) * 100 if history else 0
        st.metric("成功率", f"{success_rate:.1f}%")
    
    # 使用频率图表
    st.markdown("#### 📈 工具使用频率")
    
    tool_counts = {}
    for record in history:
        tool_name = record['tool_name']
        tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
    
    if tool_counts:
        st.bar_chart(tool_counts)
    
    # 最近使用记录
    st.markdown("#### 🕒 最近使用记录")
    
    recent_history = sorted(history, key=lambda x: x.get('timestamp', ''), reverse=True)[:10]
    
    for record in recent_history:
        with st.expander(f"🔧 {record['tool_name']} - {record.get('timestamp', 'Unknown time')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**输入参数**:")
                st.code(format_json(record.get('args', {})), language='json')
            
            with col2:
                st.markdown("**执行结果**:")
                success = record.get('success', False)
                status_icon = "✅" if success else "❌"
                st.markdown(f"{status_icon} {'成功' if success else '失败'}")
                
                if success and 'result' in record:
                    st.code(format_tool_result(record['result'])[:200] + "...", language='json')

def execute_tool(tool_name: str, args: Dict) -> Dict:
    """执行工具"""
    api_client = st.session_state.api_client
    
    try:
        response = api_client.use_tool(tool_name, args)
        return response
    except Exception as e:
        show_error_message(f"工具执行失败: {e}")
        return None

def save_to_history(tool_name: str, args: Dict, result: Dict):
    """保存执行历史"""
    from datetime import datetime
    
    if 'tool_history' not in st.session_state:
        st.session_state.tool_history = []
    
    history_record = {
        'tool_name': tool_name,
        'args': args,
        'result': result,
        'success': result is not None and result.get('success', False),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    st.session_state.tool_history.append(history_record)
    
    # 限制历史记录数量
    if len(st.session_state.tool_history) > 100:
        st.session_state.tool_history = st.session_state.tool_history[-100:]
