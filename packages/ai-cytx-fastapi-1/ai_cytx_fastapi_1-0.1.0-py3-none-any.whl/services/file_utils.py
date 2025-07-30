# 示例代码仅供参考，请勿在生产环境中直接使用
import hashlib
import os
def calculate_md5(file_path):
    """计算文档的 MD5 值。

    Args:
        file_path (str): 文档的路径。

    Returns:
        str: 文档的 MD5 值。
    """
    md5_hash = hashlib.md5()

    # 以二进制形式读取文件
    with open(file_path, "rb") as f:
        # 按块读取文件，避免大文件占用过多内存
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()

#获取文件的大小
def get_file_size(file_path):
    return os.path.getsize(file_path)

# 删除文件
def delete_file(file_path):
    os.remove(file_path)

# 从filepath获取文件名
def get_file_name(file_path):
    return os.path.basename(file_path)

if __name__ == "__main__":
    # 使用示例
    file_path = "/Users/lazylee/Works/doc/01Mlink/3.project/ai/01财蕴天下/1.xlsx"
    md5_value = calculate_md5(file_path)
    print(f"文档的大小为: {get_file_size(file_path)}")
    print(f"文档的MD5值为: {md5_value}")