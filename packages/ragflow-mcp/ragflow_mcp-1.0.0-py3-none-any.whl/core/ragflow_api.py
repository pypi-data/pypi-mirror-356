import requests
import tempfile
import os

def get_datasets(address, api_key, page=1, page_size=10, orderby=None, desc=None, dataset_name=None, dataset_id=None):
    """
    调用数据集API获取数据集列表
    
    Args:
        address: API服务器地址
        api_key: API密钥
        page: 页码，默认为1
        page_size: 每页大小，默认为10
        orderby: 排序字段
        desc: 是否降序
        dataset_name: 数据集名称过滤
        dataset_id: 数据集ID过滤
    
    Returns:
        响应的JSON数据
    """
    url = f"http://{address}/api/v1/datasets"
    
    # 构建查询参数
    params = {
        'page': page,
        'page_size': page_size
    }
    
    # 添加可选参数
    if orderby:
        params['orderby'] = orderby
    if desc is not None:
        params['desc'] = desc
    if dataset_name:
        params['name'] = dataset_name
    if dataset_id:
        params['id'] = dataset_id
    
    # 设置请求头
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def get_dataset_documents(address, api_key, dataset_id, page=1, page_size=30, orderby='create_time', desc=True, keywords=None, document_id=None, document_name=None):
    """
    调用数据集文档API获取指定数据集的文档列表
    
    Args:
        address: API服务器地址
        api_key: API密钥
        dataset_id: 数据集ID (必需)
        page: 页码，默认为1
        page_size: 每页大小，默认为30
        orderby: 排序字段，可选值: create_time (默认), update_time
        desc: 是否降序，默认为True
        keywords: 用于匹配文档标题的关键词
        document_id: 要检索的文档ID
        document_name: 文档名称过滤
    
    Returns:
        响应的JSON数据
    """
    url = f"http://{address}/api/v1/datasets/{dataset_id}/documents"
    
    # 构建查询参数
    params = {
        'page': page,
        'page_size': page_size,
        'orderby': orderby,
        'desc': desc
    }
    
    # 添加可选参数
    if keywords:
        params['keywords'] = keywords
    if document_id:
        params['id'] = document_id
    if document_name:
        params['name'] = document_name
    
    # 设置请求头
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def create_dataset(address, api_key, name, avatar=None, description=None, language="English", 
                  embedding_model="textembedding3large", permission="me", chunk_method="naive", parser_config=None):
    """
    创建数据集API
    
    Args:
        address: API服务器地址
        api_key: API密钥
        name: 数据集名称 (必需) - 只能包含英文字母、数字、下划线，以字母或下划线开头，最大65535字符
        avatar: 头像的Base64编码
        description: 数据集描述
        language: 语言设置，可选值: "English" (默认), "Chinese"
        embedding_model: 嵌入模型名称，例如: "BAAI/bge-zh-v1.5"，默认用textembedding3large@Azure-OpenAI
        permission: 访问权限，目前只能设置为 "me"
        chunk_method: 分块方法，可选值:
            "naive": 通用 (默认)
            "manual": 手动
            "qa": 问答
            "table": 表格
            "paper": 论文
            "book": 书籍
            "laws": 法律
            "presentation": 演示文稿
            "picture": 图片
            "one": 单一
            "knowledge_graph": 知识图谱
            "email": 邮件
        parser_config: 解析器配置，JSON对象，根据chunk_method不同而变化
    
    Returns:
        响应的JSON数据
    """
    url = f"http://{address}/api/v1/datasets"
    
    # 构建请求体
    data = {
        "name": name,
        "language": language,
        "permission": permission,
        "chunk_method": chunk_method
    }
    
    # 添加可选参数
    if avatar:
        data["avatar"] = avatar
    if description:
        data["description"] = description
    if embedding_model:
        data["embedding_model"] = embedding_model
    
    # 处理parser_config
    if parser_config is None:
        # 根据chunk_method设置默认parser_config
        if chunk_method == "naive":
            data["parser_config"] = {
                "chunk_token_count": 128,
                "layout_recognize": True,
                "html4excel": False,
                "delimiter": "\n!?。；！？",
                "task_page_size": 12,
                "raptor": {"use_raptor": False}
            }
        elif chunk_method in ["qa", "manual", "paper", "book", "laws", "presentation"]:
            data["parser_config"] = {
                "raptor": {"use_raptor": False}
            }
        elif chunk_method in ["table", "picture", "one", "email"]:
            data["parser_config"] = {}
        elif chunk_method == "knowledge_graph":
            data["parser_config"] = {
                "chunk_token_count": 128,
                "delimiter": "\n!?。；！？",
                "entity_types": ["organization", "person", "location", "event", "time"]
            }
    else:
        data["parser_config"] = parser_config
    
    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        print(f"数据集创建成功: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def create_chunk(address, api_key, dataset_id, document_id, content, important_keywords=None):
    """
    创建文档chunk的API
    
    Args:
        address: API服务器地址
        api_key: API密钥
        dataset_id: 数据集ID (必需)
        document_id: 文档ID (必需)
        content: chunk的文本内容 (必需)
        important_keywords: 与chunk相关的关键词列表
    
    Returns:
        响应的JSON数据
    """
    url = f"http://{address}/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks"
    
    # 构建请求体
    data = {
        "content": content
    }
    
    # 添加可选参数
    if important_keywords:
        data["important_keywords"] = important_keywords
    
    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def retrieve_chunks(address, api_key, question, dataset_ids=None, document_ids=None, page=1, 
                   page_size=30, similarity_threshold=0.2, vector_similarity_weight=0.3, 
                   top_k=1024, rerank_id=None, keyword=False, highlight=False):
    """
    从指定数据集中检索chunks的API
    
    Args:
        address: API服务器地址
        api_key: API密钥
        question: 用户查询或查询关键词 (必需)
        dataset_ids: 要搜索的数据集ID列表
        document_ids: 要搜索的文档ID列表
        page: 页码，默认为1
        page_size: 每页最大chunk数量，默认为30
        similarity_threshold: 最小相似度分数，默认为0.2
        vector_similarity_weight: 向量余弦相似度权重，默认为0.3
        top_k: 参与向量余弦计算的chunk数量，默认为1024
        rerank_id: 重排序模型ID
        keyword: 是否启用基于关键词的匹配，默认为False
        highlight: 是否启用匹配词高亮显示，默认为False
    
    Returns:
        响应的JSON数据
    
    Note:
        必须设置dataset_ids或document_ids中的至少一个
    """
    url = f"http://{address}/api/v1/retrieval"
    
    # 构建请求体
    data = {
        "question": question,
        "page": page,
        "page_size": page_size,
        "similarity_threshold": similarity_threshold,
        "vector_similarity_weight": vector_similarity_weight,
        "top_k": top_k,
        "keyword": keyword,
        "highlight": highlight
    }
    
    # 添加可选参数
    if dataset_ids:
        data["dataset_ids"] = dataset_ids
    if document_ids:
        data["document_ids"] = document_ids
    if rerank_id:
        data["rerank_id"] = rerank_id
    
    # 验证必需参数
    if not dataset_ids and not document_ids:
        print("错误: 必须提供dataset_ids或document_ids中的至少一个")
        return None
    
    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        result = response.json()
        
        # 检查返回的错误码
        if result.get('code') != 0:
            print(f"API返回错误 - 错误码: {result.get('code')}, 错误信息: {result.get('message')}")
            
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def upload_document(address, api_key, dataset_id, file_path, document_name=None):
    """
    上传文档到指定数据集
    
    Args:
        address: API服务器地址
        api_key: API密钥
        dataset_id: 数据集ID (必需)
        file_path: 要上传的文件路径 (必需)
        document_name: 文档名称，如果不提供则使用文件名
    
    Returns:
        响应的JSON数据
    """
    url = f"http://{address}/api/v1/datasets/{dataset_id}/documents"
    
    # 设置请求头
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        # 准备文件上传
        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {}
            if document_name:
                # 只使用主要的参数名
                data['name'] = document_name
            
            print(f"上传文档，指定名称: {document_name}")  # 调试信息
            print(f"上传参数: {data}")  # 调试上传参数
            response = requests.post(url, files=files, data=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"上传结果: {result}")  # 调试信息
            return result
    except requests.exceptions.RequestException as e:
        print(f"文档上传失败: {e}")
        return None
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
        return None

def create_empty_document(address, api_key, dataset_id, document_name):
    """
    创建一个空白文档（通过上传最小文件实现）
    
    Args:
        address: API服务器地址
        api_key: API密钥
        dataset_id: 数据集ID (必需)
        document_name: 文档名称 (必需)
    
    Returns:
        响应的JSON数据，包含新创建的文档ID
    """
    # 创建临时文件
    temp_content = f"# {document_name}\n\n这是一个空白文档，准备通过API添加内容。"
    
    try:
        # 创建一个具有指定名称的临时文件
        # 使用安全的文件名（移除特殊字符）
        safe_filename = "".join(c for c in document_name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_filename:
            safe_filename = "document"
        
        temp_file_path = f"/tmp/{safe_filename}.txt"
        
        # 写入文件内容
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(temp_content)
        
        # 使用上传API创建文档
        result = upload_document(
            address=address,
            api_key=api_key,
            dataset_id=dataset_id,
            file_path=temp_file_path,
            document_name=document_name  # 仍然传递文档名称参数
        )
        
        # 清理临时文件
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        return result
    
    except Exception as e:
        print(f"创建空白文档失败: {e}")
        # 确保清理临时文件
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return None

def test_upload_document_with_different_params(address, api_key, dataset_id, file_path, document_name):
    """
    测试不同的参数名来上传文档，用于调试
    """
    url = f"http://{address}/api/v1/datasets/{dataset_id}/documents"
    headers = {'Authorization': f'Bearer {api_key}'}
    
    # 测试不同的参数名组合
    param_combinations = [
        {'name': document_name},
        {'filename': document_name},
        {'document_name': document_name},
        {'title': document_name},
        {'display_name': document_name},
    ]
    
    for i, data in enumerate(param_combinations):
        print(f"\n=== 测试组合 {i+1}: {data} ===")
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(url, files=files, data=data, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('code') == 0:
                        doc_info = result.get('data', {})
                        created_name = doc_info.get('name', '未知')
                        print(f"✅ 成功! 创建的文档名: {created_name}")
                        if document_name in created_name:
                            print(f"🎉 找到正确的参数组合: {data}")
                            return data
                    else:
                        print(f"❌ API错误: {result}")
                else:
                    print(f"❌ HTTP错误: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ 异常: {e}")
    
    return None

def find_document_dataset(address, api_key, document_id):
    """
    查找文档所属的数据集ID
    
    Args:
        address: API服务器地址
        api_key: API密钥  
        document_id: 文档ID
    
    Returns:
        数据集ID，如果未找到则返回None
    """
    # 获取所有数据集
    datasets_result = get_datasets(
        address=address,
        api_key=api_key,
        page=1,
        page_size=100
    )
    
    if not datasets_result or datasets_result.get('code') != 0:
        print("获取数据集列表失败")
        return None
    
    datasets = datasets_result.get('data', [])
    
    # 在每个数据集中查找文档
    for dataset in datasets:
        dataset_id = dataset.get('id')
        if not dataset_id:
            continue
            
        # 查找文档
        docs_result = get_dataset_documents(
            address=address,
            api_key=api_key,
            dataset_id=dataset_id,
            document_id=document_id,  # 按文档ID查找
            page=1,
            page_size=1
        )
        
        if docs_result and docs_result.get('code') == 0:
            docs = docs_result.get('data', {}).get('docs', [])
            if docs and len(docs) > 0:
                found_doc = docs[0]
                if found_doc.get('id') == document_id:
                    print(f"找到文档 {document_id} 在数据集 {dataset.get('name')} (ID: {dataset_id})")
                    return dataset_id
    
    print(f"未找到文档 {document_id} 所属的数据集")
    return None

def download_document(address, api_key, dataset_id, document_id, output_path=None):
    """
    从指定数据集下载文档
    
    Args:
        address: API服务器地址
        api_key: API密钥
        dataset_id: 数据集ID (必需)
        document_id: 文档ID (必需)
        output_path: 输出文件路径，如果不提供则保存到当前目录下以document_id命名的文件
    
    Returns:
        下载成功返回文件保存路径，失败返回None
    """
    url = f"http://{address}/api/v1/datasets/{dataset_id}/documents/{document_id}"
    
    # 设置请求头
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        
        # 检查HTTP状态码
        if response.status_code == 200:
            # 确定保存路径
            if not output_path:
                # 尝试从响应头获取文件名
                content_disposition = response.headers.get('content-disposition', '')
                if 'filename=' in content_disposition:
                    # 提取文件名
                    filename = content_disposition.split('filename=')[1].strip('"')
                    output_path = f"./{filename}"
                else:
                    # 使用document_id作为文件名
                    output_path = f"./document_{document_id}.txt"
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 保存文件
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            
            print(f"文档下载成功，保存到: {output_path}")
            return output_path
        else:
            # 尝试解析错误响应
            try:
                error_data = response.json()
                error_msg = error_data.get('message', f'HTTP错误: {response.status_code}')
                print(f"文档下载失败: {error_msg}")
            except:
                print(f"文档下载失败: HTTP错误 {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"下载请求失败: {e}")
        return None
    except Exception as e:
        print(f"文档下载异常: {e}")
        return None


# 使用示例
if __name__ == "__main__":
    # 配置参数
    ADDRESS = "ragflow.iepose.cn"  # 替换为实际地址
    API_KEY = "ragflow-g4ZTU4ZjM4YTAwMTExZWZhZjkyMDI0Mm"  # 替换为实际的API密钥
    
    # # 调用数据集API
    # result = get_datasets(
    #     address=ADDRESS,
    #     api_key=API_KEY,
    #     page=1,
    #     page_size=20
    #     # dataset_name="第二大脑"  # 可选参数
    # )
    
    # if result:
    #     print("数据集API调用成功:")
    #     print(result)
    # else:
    #     print("数据集API调用失败")
    
    # # 调用文档API示例（需要实际的dataset_id）
    dataset_id = "c3303d4ee45611ef9b610242ac180003"  # 替换为实际的数据集ID
    # docs_result = get_dataset_documents(
    #     address=ADDRESS,
    #     api_key=API_KEY,
    #     dataset_id=dataset_id,
    #     page=1,
    #     page_size=10,
    #     keywords=None  # 可选参数
    #     orderby="update_time"
    # )
    
    # if docs_result:
    #     print("文档API调用成功:")
    #     print(docs_result)
    # else:
    #     print("文档API调用失败")
    
    # 创建chunk示例（需要实际的document_id）
    document_id = "6e18ef4be45911ef9d800242ac180003"  # 替换为实际的文档ID
    # chunk_result = create_chunk(
    #     address=ADDRESS,
    #     api_key=API_KEY,
    #     dataset_id=dataset_id,
    #     document_id=document_id,
    #     content="openmemory是一个开源的RAG框架，旨在帮助用户构建自己的知识库。",
    #     important_keywords=["openmemory", "rag", "全局记忆", "知识库"]  # 可选参数
    # )
    
    # if chunk_result:
    #     print("chunk创建成功:")
    #     print(chunk_result)
    # else:
    #     print("chunk创建失败")
    
    # 检索chunks示例
    # retrieval_result = retrieve_chunks(
    #     address=ADDRESS,
    #     api_key=API_KEY,
    #     question="什么是openmemory？",
    #     dataset_ids=[dataset_id],  # 使用数据集ID列表
    #     page=1,
    #     page_size=5,  # 减少页面大小
    #     similarity_threshold=0.1,  # 降低相似度阈值
    #     vector_similarity_weight=0.5,  # 调整权重
    #     top_k=50,  # 减少top_k数量
    #     keyword=False,  # 先禁用关键词匹配
    #     highlight=False  # 先禁用高亮显示
    # )
    
    # if retrieval_result:
    #     print("检索成功:")
    #     print(retrieval_result)
    # else:
    #     print("检索失败")
    
    # # 创建数据集示例
    # create_result = create_dataset(
    #     address=ADDRESS,
    #     api_key=API_KEY,
    #     name="my_new_dataset",
    #     description="这是一个新的数据集",
    #     language="English",
    #     permission="me",
    #     chunk_method="naive"
    # )
    
    # if create_result:
    #     print("数据集创建成功:")
    #     print(create_result)
    # else:
    #     print("数据集创建失败")
    
    # # 创建数据集示例
    # create_result = create_dataset(
    #     address=ADDRESS,
    #     api_key=API_KEY,
    #     name="my_new_dataset",
    #     description="这是一个新的数据集",
    #     language="English",
    #     embedding_model="BAAI/bge-zh-v1.5",
    #     permission="me",
    #     chunk_method="naive"
    # )
    
    # if create_result:
    #     print("数据集创建成功:")
    #     print(create_result)
    # else:
    #     print("数据集创建失败")
    
    # 测试文档上传的不同参数名
    # test_result = test_upload_document_with_different_params(
    #     address=ADDRESS,
    #     api_key=API_KEY,
    #     dataset_id=dataset_id,
    #     file_path="path/to/your/file.txt",  # 替换为实际文件路径
    #     document_name="测试文档"
    # )
    
    # 查找文档所属数据集示例
    document_id_to_find = "6e18ef4be45911ef9d800242ac180003"  # 替换为实际的文档ID
    # dataset_id_found = find_document_dataset(
    #     address=ADDRESS,
    #     api_key=API_KEY,
    #     document_id=document_id_to_find
    # )
    
    # if dataset_id_found:
    #     print(f"文档 {document_id_to_find} 所属的数据集ID: {dataset_id_found}")
    # else:
    #     print(f"未找到文档 {document_id_to_find} 所属的数据集")