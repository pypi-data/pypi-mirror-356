from functools import lru_cache
from typing import Dict, List, Tuple
from functools import lru_cache


def generate_csv_output(info: List[Dict], model_class_name: str) -> str:
    """
    生成模型模块信息的CSV格式字符串
    :param info: get_module_info返回的模块信息列表
    :param model_class_name: 模型类名称（用于根模块显示）
    :return: CSV格式字符串
    """
    import csv
    from io import StringIO  # 用于捕获CSV输出为字符串

    all_rows = []
    
    # 计算最大层级深度（用于确定CSV列数）
    max_depth = 0
    for item in info:
        module_depth = item["depth"]
        param_depth = module_depth + 1 if item["parameters"] else 0
        max_depth = max(max_depth, module_depth, param_depth)

    # 生成层级列名（Depth0, Depth1, ..., DepthN）
    depth_columns = [f"Depth{i}" for i in range(max_depth + 1)]
    # 统计列名（新增 requires_grad）
    stat_columns = [
        "class_name",
        "total_params", "dtype_stats", "total_memory", 
        "recursive_params", "recursive_memory", "numel", "dtype", "size", "requires_grad"  # 新增列
    ]
    all_columns = depth_columns + stat_columns

    # 处理模块和参数数据
    for item in info:
        # 模块名称处理（根模块显示模型类名）
        module_name = item["module_name"] if item["module_name"] else model_class_name
        # 拆分层级路径（例如 "fc2.1" → ["fc2", "1"]）
        hierarchy = [model_class_name] + module_name.split('.') if module_name else [model_class_name]
        
        # 填充模块行数据
        row = {col: "" for col in all_columns}
        for i, part in enumerate(hierarchy):
            if i < len(depth_columns):
                row[f"Depth{i}"] = part
        
        # 模块统计信息
        row["class_name"] = item["class_name"]
        row["total_params"] = item["total_params"]
        row["dtype_stats"] = str(item["dtype_stats"])  # 转换为字符串避免字典格式问题
        row["total_memory"] = item["total_memory"]
        row["recursive_params"] = item["recursive_params"]
        row["recursive_memory"] = item["recursive_memory"]
        all_rows.append(row)

        # 处理模块下的参数数据
        for param in item["parameters"]:
            # 参数名称层级路径（例如 "fc1.weight" → ["fc1", "weight"]）
            param_hierarchy = [model_class_name] + param["name"].split('.')
            
            # 填充参数行数据
            param_row = {col: "" for col in all_columns}
            for i, part in enumerate(param_hierarchy):
                if i < len(depth_columns):
                    param_row[f"Depth{i}"] = part
            
            # 参数详细信息（新增 requires_grad）
            param_row["numel"] = param["numel"]
            param_row["dtype"] = param["dtype"]
            param_row["size"] = str(param["size"])  # 转换为字符串避免列表格式问题
            param_row["requires_grad"] = param["requires_grad"]  # 填充新增字段
            all_rows.append(param_row)

    # 生成CSV字符串
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=all_columns)
    writer.writeheader()
    writer.writerows(all_rows)
    
    return output.getvalue()


def get_module_info(model) -> List[Dict]:
    """
    递归获取模型所有子模块（含根模块）的参数信息（包含递归统计字段）
    """
    model: torch.nn.Module = model
    module_info = []
    
    depth_map = {"": 0}
    
    # 遍历所有子模块，收集基础信息（原有逻辑）
    for module_name, submodule in model.named_modules():
        # 计算当前模块的深度（基于父模块深度）
        if module_name == "":
            current_depth = 0
        else:
            # 提取父模块名称（例如"fc2.1.conv"的父模块是"fc2.1"）
            parent_name, _, _ = module_name.rpartition('.')
            current_depth = depth_map.get(parent_name, 0) + 1
        depth_map[module_name] = current_depth  # 记录当前模块深度
        
        # 统计参数（移除dtype_to_bytes，改用dtype.itemsize）
        params = list(submodule.named_parameters(recurse=False))
        total_params = sum(p.numel() for _, p in params)
        dtype_stats = {}
        total_memory = 0
        parameters = []
        
        for param_name, param in params:
            dtype = param.dtype
            numel = param.numel()
            # 直接使用dtype.itemsize获取字节数（替代原dtype_to_bytes）
            bytes_per_element = dtype.itemsize  # 关键优化点
            
            size = list(param.size())
            full_param_name = f"{module_name}.{param_name}" if module_name else param_name
            
            # 更新类型统计
            if dtype not in dtype_stats:
                dtype_stats[dtype] = (0, 0)
            current_count, current_memory = dtype_stats[dtype]
            dtype_stats[dtype] = (current_count + numel, current_memory + numel * bytes_per_element)
            total_memory += numel * bytes_per_element
            
            # 新增：记录参数的 requires_grad 状态
            parameters.append({
                "name": full_param_name,
                "numel": numel,
                "dtype": str(dtype),
                "size": size,
                "requires_grad": param.requires_grad  # 新增字段
            })
        
        module_info.append({
            "module_name": module_name,
            "class_name": submodule.__class__.__name__,  # 新增类名字段
            "total_params": total_params,
            "dtype_stats": {str(k): v for k, v in dtype_stats.items()},
            "total_memory": total_memory,
            "depth": current_depth,
            "parameters": parameters
        })
    
    # 新增：计算每个模块的递归参数和内存
    for parent in module_info:
        parent_name = parent["module_name"]
        recursive_params = parent["total_params"]  # 初始化为自身参数
        recursive_memory = parent["total_memory"]   # 初始化为自身内存
        
        # 遍历所有模块，累加子模块的参数和内存
        for child in module_info:
            child_name = child["module_name"]
            if child_name == parent_name:
                continue  # 跳过自身
            
            # 判断是否为子模块（根模块包含所有其他模块；非根模块需以"父模块名."开头）
            if (parent_name == "" or 
                (child_name.startswith(f"{parent_name}.") and len(child_name) > len(parent_name))):
                recursive_params += child["total_params"]
                recursive_memory += child["total_memory"]
        
        # 添加递归统计字段
        parent["recursive_params"] = recursive_params
        parent["recursive_memory"] = recursive_memory
    
    return module_info

def size_of_tensors(t:object):
    import torch
    if isinstance(t, torch.Tensor):
        return t.element_size() * t.nelement()
    elif isinstance(t, (list, tuple)):
        return sum(size_of_tensors(x) for x in t)
    elif isinstance(t, dict):
        return sum(size_of_tensors(x) for x in t.values())
    else:
        print(f"Unsupported type for t: {type(t)}")
        return 0
    

def serialize_obj(d, depth=0):
    import torch
    indent = ' ' * 4 * depth
    child_indent = ' ' * 4 * (depth + 1)
    
    if isinstance(d, dict):
        items = list(d.items())
        elements = []
        for i, (k, v) in enumerate(items):
            element = f"{child_indent}{k}: {serialize_obj(v, depth + 1)}"
            if i < len(items) - 1:
                element += ","
            elements.append(element)
        elements_str = '\n'.join(elements)
        return f"[Dict(len={len(d)}):\n{elements_str}\n{indent}]"
    
    elif isinstance(d, list):
        elements = []
        for i, item in enumerate(d):
            element = f"{child_indent}{serialize_obj(item, depth + 1)}"
            if i < len(d) - 1:
                element += ","
            elements.append(element)
        elements_str = '\n'.join(elements)
        return f"[List(len={len(d)}):\n{elements_str}\n{indent}]"
    
    elif isinstance(d, torch.Tensor):
        return f"[Tensor: shape={d.shape}, device={d.device}, dtype={d.dtype}]"
    
    elif str(type(d)).find("BatchEncoding") >= 0:
        items = list(d.items())
        elements = []
        for i, (k, v) in enumerate(items):
            element = f"{child_indent}{k}: {serialize_obj(v, depth + 1)}"
            if i < len(items) - 1:
                element += ","
            elements.append(element)
        elements_str = '\n'.join(elements)
        return f"[BatchEncoding(len={len(d)}):\n{elements_str}\n{indent}]"
    
    elif isinstance(d, (str, int, float, bool, type(None))):
        return f"[{type(d).__name__}: {repr(d) if isinstance(d, str) else d}]"

    elif isinstance(d, bytes):
        return f"[bytes(len={len(d)}): (0bxxxx)]"
    
    else:
        return f"[UnknownType({type(d)}): {str(d)}]"

@lru_cache
def get_value_from_env(key:str, default_value):
    import os
    if key not in os.environ: return default_value
    type_ = type(default_value)
    value = os.environ[key]
    if type_ == bool:
        # 补充更多常见的布尔表示形式（不区分大小写）
        value_lower = value.lower()
        if value_lower in ["true", "1", "yes", "y", "on", "enable"]:  # 新增on/enable
            return True
        elif value_lower in ["false", "0", "no", "n", "off", "disable"]:  # 新增off/disable
            return False
        else:
            raise ValueError(f"Invalid boolean value for {key}: {value}")
    return type_(value)
        

if __name__ == '__main__':
    a = [1,2,3]
    s = size_of_tensors(a)
    print(s)
    s = serialize_obj(a)
    print(s)
    
    from torch import nn
    simple_module = nn.Sequential(
        nn.Linear(10, 20),
        nn.ReLU(),
        nn.Linear(20, 10)
    )
    simple_module.requires_grad_(True)
    module_info = get_module_info(simple_module)
    print(module_info)
    csv_output = generate_csv_output(module_info, "SimpleModule")
    print(csv_output)
    with open(f"tmp.csv", "w") as f:
        f.write(csv_output)
        
    import os
    os.environ["Z_LOG"] = "debug"
    value = get_value_from_env("Z_LOG", "info")
    print(value)