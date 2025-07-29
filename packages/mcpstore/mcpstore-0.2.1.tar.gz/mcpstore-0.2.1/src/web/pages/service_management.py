"""
服务管理页面
"""

import streamlit as st
from typing import Dict, List
import json

from utils.helpers import (
    show_success_message, show_error_message, show_warning_message,
    validate_url, validate_service_name, create_service_card,
    get_status_color, get_status_text, get_preset_services,
    format_json
)

def show():
    """显示服务管理页面"""
    st.header("🛠️ 服务管理")
    
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📋 服务列表", "➕ 添加服务", "📦 批量操作", "🔧 服务详情"])
    
    with tab1:
        show_service_list()
    
    with tab2:
        show_add_service()
    
    with tab3:
        show_batch_operations()
    
    with tab4:
        show_service_details()

def show_service_list():
    """显示服务列表"""
    st.subheader("📋 已注册服务")
    
    # 操作按钮
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 刷新列表", key="service_refresh_list"):
            st.rerun()

    with col2:
        if st.button("🔍 检查健康", key="service_check_health"):
            check_all_services_health()
    
    # 获取服务列表
    api_client = st.session_state.api_client
    response = api_client.list_services()
    
    if not response:
        show_error_message("无法获取服务列表")
        return
    
    services = response.get('data', [])
    
    if not services:
        st.info("暂无已注册的服务")
        return
    
    # 显示服务统计
    healthy_count = sum(1 for s in services if s.get('status') == 'healthy')
    st.metric("服务统计", f"{len(services)} 个服务", f"{healthy_count} 个健康")
    
    # 服务列表
    for service in services:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
            
            with col1:
                status_icon = get_status_color(service.get('status', 'unknown'))
                st.markdown(f"**{status_icon} {service.get('name', 'Unknown')}**")
                st.caption(service.get('url', 'No URL'))
            
            with col2:
                tool_count = service.get('tool_count', 0)
                st.metric("工具", tool_count)
            
            with col3:
                status_text = get_status_text(service.get('status', 'unknown'))
                st.write(status_text)
            
            with col4:
                if st.button("📊 详情", key=f"detail_{service.get('name')}"):
                    st.session_state.selected_service = service.get('name')
                    st.rerun()
            
            with col5:
                # 操作按钮
                col5_1, col5_2, col5_3 = st.columns(3)
                
                with col5_1:
                    if st.button("🔄", key=f"restart_{service.get('name')}", help="重启服务"):
                        restart_service(service.get('name'))
                
                with col5_2:
                    if st.button("✏️", key=f"edit_{service.get('name')}", help="编辑服务"):
                        st.session_state.edit_service = service.get('name')
                        st.rerun()
                
                with col5_3:
                    if st.button("🗑️", key=f"delete_{service.get('name')}", help="删除服务"):
                        delete_service(service.get('name'))
            
            st.markdown("---")

def show_add_service():
    """显示添加服务页面"""
    st.subheader("➕ 添加新服务")
    
    # 预设服务
    st.markdown("#### 🎯 快速添加预设服务")
    preset_services = get_preset_services()
    
    col1, col2 = st.columns(2)
    for i, preset in enumerate(preset_services):
        with col1 if i % 2 == 0 else col2:
            with st.container():
                st.markdown(f"**{preset['name']}**")
                st.caption(preset['description'])
                if st.button(f"添加 {preset['name']}", key=f"preset_{i}"):
                    add_preset_service(preset)
    
    st.markdown("---")
    
    # 自定义服务
    st.markdown("#### 🔧 自定义服务配置")
    
    with st.form("add_service_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            service_name = st.text_input(
                "服务名称 *",
                help="服务的唯一标识符"
            )
            
            service_url = st.text_input(
                "服务URL *", 
                placeholder="http://example.com/mcp",
                help="MCP服务的完整URL地址"
            )
        
        with col2:
            transport_type = st.selectbox(
                "传输类型",
                ["auto", "sse", "streamable-http"],
                help="选择auto将自动推断传输类型"
            )
            
            keep_alive = st.checkbox(
                "保持连接",
                value=False,
                help="是否保持长连接"
            )
        
        # 高级选项
        with st.expander("🔧 高级选项"):
            headers_text = st.text_area(
                "请求头 (JSON格式)",
                placeholder='{"Authorization": "Bearer token"}',
                help="自定义HTTP请求头"
            )
            
            env_text = st.text_area(
                "环境变量 (JSON格式)",
                placeholder='{"API_KEY": "your_key"}',
                help="服务运行时的环境变量"
            )
        
        submitted = st.form_submit_button("🚀 添加服务")
        
        if submitted:
            add_custom_service(service_name, service_url, transport_type, keep_alive, headers_text, env_text)

def show_batch_operations():
    """显示批量操作页面"""
    st.subheader("📦 批量操作")
    
    # 批量添加
    st.markdown("#### ➕ 批量添加服务")
    
    # 方式1: JSON配置
    with st.expander("📝 JSON配置方式"):
        json_config = st.text_area(
            "服务配置 (JSON数组格式)",
            placeholder='''[
  {
    "name": "service1",
    "url": "http://example1.com/mcp"
  },
  {
    "name": "service2", 
    "url": "http://example2.com/mcp"
  }
]''',
            height=200
        )
        
        if st.button("🚀 批量添加 (JSON)"):
            batch_add_from_json(json_config)
    
    # 方式2: CSV上传
    with st.expander("📊 CSV文件方式"):
        st.markdown("CSV格式: name,url,transport,description")
        
        uploaded_file = st.file_uploader(
            "选择CSV文件",
            type=['csv'],
            help="CSV文件应包含: name, url, transport, description列"
        )
        
        if uploaded_file and st.button("🚀 批量添加 (CSV)"):
            batch_add_from_csv(uploaded_file)
    
    st.markdown("---")
    
    # 批量操作
    st.markdown("#### 🔧 批量管理")
    
    # 获取服务列表用于批量操作
    api_client = st.session_state.api_client
    response = api_client.list_services()
    
    if response and response.get('data'):
        services = response['data']
        service_names = [s.get('name') for s in services]
        
        selected_services = st.multiselect(
            "选择要操作的服务",
            service_names
        )
        
        if selected_services:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 批量重启", key="service_batch_restart"):
                    batch_restart_services(selected_services)

            with col2:
                if st.button("🔍 批量检查", key="service_batch_check"):
                    batch_check_services(selected_services)
            
            with col3:
                if st.button("🗑️ 批量删除", type="secondary"):
                    if st.session_state.get('confirm_batch_delete'):
                        batch_delete_services(selected_services)
                    else:
                        st.session_state.confirm_batch_delete = True
                        st.warning("再次点击确认删除")

def show_service_details():
    """显示服务详情页面"""
    selected_service = st.session_state.get('selected_service')
    
    if not selected_service:
        st.info("请从服务列表中选择一个服务查看详情")
        return
    
    st.subheader(f"🔧 服务详情: {selected_service}")
    
    # 获取服务详细信息
    api_client = st.session_state.api_client
    response = api_client.get_service_info(selected_service)
    
    if not response:
        show_error_message("无法获取服务详情")
        return
    
    service_data = response.get('data', {})
    
    # 基本信息
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 基本信息")
        service_info = service_data.get('service', {})
        
        st.write(f"**名称**: {service_info.get('name', 'N/A')}")
        st.write(f"**URL**: {service_info.get('url', 'N/A')}")
        st.write(f"**传输类型**: {service_info.get('transport', 'N/A')}")
        st.write(f"**连接状态**: {service_data.get('connected', 'N/A')}")
    
    with col2:
        st.markdown("#### 📊 统计信息")
        tools = service_data.get('tools', [])
        st.metric("工具数量", len(tools))
        
        # 状态指示
        connected = service_data.get('connected', False)
        status_color = "🟢" if connected else "🔴"
        status_text = "已连接" if connected else "未连接"
        st.write(f"**状态**: {status_color} {status_text}")
    
    # 工具列表
    st.markdown("#### 🔧 可用工具")
    
    if tools:
        for tool in tools:
            with st.expander(f"🔧 {tool.get('name', 'Unknown')}"):
                st.write(f"**描述**: {tool.get('description', 'No description')}")
                
                # 显示参数schema
                if 'inputSchema' in tool:
                    st.markdown("**参数结构**:")
                    st.code(format_json(tool['inputSchema']), language='json')
    else:
        st.info("此服务暂无可用工具")

# ==================== 辅助函数 ====================

def check_all_services_health():
    """检查所有服务健康状态"""
    api_client = st.session_state.api_client
    
    with st.spinner("检查服务健康状态..."):
        response = api_client.check_services()
        
        if response:
            show_success_message("健康检查完成")
            st.rerun()
        else:
            show_error_message("健康检查失败")

def restart_service(service_name: str):
    """重启服务"""
    api_client = st.session_state.api_client
    
    with st.spinner(f"重启服务 {service_name}..."):
        response = api_client.restart_service(service_name)
        
        if response and response.get('success'):
            show_success_message(f"服务 {service_name} 重启成功")
            st.rerun()
        else:
            show_error_message(f"服务 {service_name} 重启失败")

def delete_service(service_name: str):
    """删除服务"""
    # 确认删除
    if not st.session_state.get(f'confirm_delete_{service_name}'):
        st.session_state[f'confirm_delete_{service_name}'] = True
        show_warning_message(f"确认删除服务 {service_name}？再次点击删除按钮确认。")
        return
    
    api_client = st.session_state.api_client
    
    with st.spinner(f"删除服务 {service_name}..."):
        response = api_client.delete_service(service_name)
        
        if response and response.get('success'):
            show_success_message(f"服务 {service_name} 删除成功")
            # 清理确认状态
            if f'confirm_delete_{service_name}' in st.session_state:
                del st.session_state[f'confirm_delete_{service_name}']
            st.rerun()
        else:
            show_error_message(f"服务 {service_name} 删除失败")

def add_preset_service(preset: Dict):
    """添加预设服务"""
    api_client = st.session_state.api_client
    
    with st.spinner(f"添加服务 {preset['name']}..."):
        response = api_client.add_service({
            "name": preset['name'],
            "url": preset['url']
        })
        
        if response and response.get('success'):
            show_success_message(f"服务 {preset['name']} 添加成功")
            st.rerun()
        else:
            show_error_message(f"服务 {preset['name']} 添加失败")

def add_custom_service(name: str, url: str, transport: str, keep_alive: bool, headers_text: str, env_text: str):
    """添加自定义服务"""
    # 验证输入
    if not validate_service_name(name):
        show_error_message("服务名称无效")
        return
    
    if not validate_url(url):
        show_error_message("URL格式无效")
        return
    
    # 构建配置
    config = {
        "name": name,
        "url": url
    }
    
    if transport != "auto":
        config["transport"] = transport
    
    if keep_alive:
        config["keep_alive"] = True
    
    # 解析headers
    if headers_text.strip():
        try:
            config["headers"] = json.loads(headers_text)
        except json.JSONDecodeError:
            show_error_message("请求头JSON格式错误")
            return
    
    # 解析环境变量
    if env_text.strip():
        try:
            config["env"] = json.loads(env_text)
        except json.JSONDecodeError:
            show_error_message("环境变量JSON格式错误")
            return
    
    # 添加服务
    api_client = st.session_state.api_client
    
    with st.spinner(f"添加服务 {name}..."):
        response = api_client.add_service(config)
        
        if response and response.get('success'):
            show_success_message(f"服务 {name} 添加成功")
            st.rerun()
        else:
            show_error_message(f"服务 {name} 添加失败")

def batch_add_from_json(json_config: str):
    """从JSON配置批量添加服务"""
    try:
        services = json.loads(json_config)
        
        if not isinstance(services, list):
            show_error_message("JSON配置必须是数组格式")
            return
        
        api_client = st.session_state.api_client
        
        with st.spinner("批量添加服务..."):
            response = api_client.batch_add_services(services)
            
            if response and response.get('success'):
                show_success_message(f"成功批量添加 {len(services)} 个服务")
                st.rerun()
            else:
                show_error_message("批量添加失败")
    
    except json.JSONDecodeError:
        show_error_message("JSON格式错误")

def batch_add_from_csv(uploaded_file):
    """从CSV文件批量添加服务"""
    try:
        # 简单的CSV解析，不依赖pandas
        import csv
        import io

        # 读取文件内容
        content = uploaded_file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))

        services = []
        for row in csv_reader:
            service = {
                "name": row.get('name', ''),
                "url": row.get('url', '')
            }

            if 'transport' in row and row['transport']:
                service['transport'] = row['transport']

            services.append(service)

        api_client = st.session_state.api_client

        with st.spinner("批量添加服务..."):
            response = api_client.batch_add_services(services)

            if response and response.get('success'):
                show_success_message(f"成功批量添加 {len(services)} 个服务")
                st.rerun()
            else:
                show_error_message("批量添加失败")

    except Exception as e:
        show_error_message(f"CSV处理失败: {e}")

def batch_restart_services(service_names: List[str]):
    """批量重启服务"""
    api_client = st.session_state.api_client
    
    success_count = 0
    
    with st.spinner("批量重启服务..."):
        for service_name in service_names:
            response = api_client.restart_service(service_name)
            if response and response.get('success'):
                success_count += 1
    
    show_success_message(f"成功重启 {success_count}/{len(service_names)} 个服务")
    st.rerun()

def batch_check_services(service_names: List[str]):
    """批量检查服务"""
    api_client = st.session_state.api_client
    
    with st.spinner("批量检查服务..."):
        response = api_client.check_services()
        
        if response:
            show_success_message("批量检查完成")
            st.rerun()
        else:
            show_error_message("批量检查失败")

def batch_delete_services(service_names: List[str]):
    """批量删除服务"""
    api_client = st.session_state.api_client
    
    success_count = 0
    
    with st.spinner("批量删除服务..."):
        for service_name in service_names:
            response = api_client.delete_service(service_name)
            if response and response.get('success'):
                success_count += 1
    
    show_success_message(f"成功删除 {success_count}/{len(service_names)} 个服务")
    
    # 清理确认状态
    st.session_state.confirm_batch_delete = False
    st.rerun()
