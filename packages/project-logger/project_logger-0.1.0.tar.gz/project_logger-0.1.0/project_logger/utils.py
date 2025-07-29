# utils.py
"""
实用工具函数
包含UUID管理、主机特征识别等功能
"""
import os
import sys
import hashlib
import socket
import getpass
import uuid
import time
import platform
import subprocess
import logging
import stat
import shutil
import random
import string
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ProjectSecurityLogger")

# 锁文件有效期（小时），可配置
LOCK_FILE_VALID_HOURS = 24

# 项目UUID文件配置
UUID_FILE = ".project_uuid"  # 隐藏文件
PENDING_UUID_FILE = ".pending_uuid"  # 未激活状态临时UUID文件
LOCK_FILE_PREFIX = ".project_lock_"  # 锁文件前缀
HOST_IDENTIFIER_PREFIX = "host_identifier_"

# 激活码文件
ACTIVATION_FILE = "start.txt"

# 系统标识文件配置（在项目最深目录）
SYSTEM_IDENTIFIER_DIR = "security"
SYSTEM_IDENTIFIER_FILE = "system_identifier.js"

# 主机标识文件配置（在固定路径）
HOST_IDENTIFIER_DIR = "~/.project_security"
HOST_IDENTIFIER_FILE = "host_identifier.dat"


def set_file_hidden(file_path):
    """将文件属性设置为隐藏（Windows）或其他系统等效操作"""
    try:
        # Windows系统设置隐藏属性
        if platform.system() == "Windows":
            import ctypes
            # 组合属性：系统文件 + 隐藏文件
            FILE_ATTRIBUTE_SYSTEM = 0x04
            FILE_ATTRIBUTE_HIDDEN = 0x02
            attributes = FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_HIDDEN

            ctypes.windll.kernel32.SetFileAttributesW(file_path, attributes)
            return True

        # Unix-like系统使用点前缀作为隐藏文件，文件名中已包含点
        # 设置文件权限为仅所有者读写
        file = Path(file_path)
        file.chmod(stat.S_IRUSR | stat.S_IWUSR)
        return True
    except Exception as e:
        logger.error(f"Failed to set hidden attribute for {file_path}: {e}")
        return False


def get_project_parent_dir():
    """获取项目父目录（项目文件夹的上一级）"""
    # 获取当前项目目录
    project_dir = Path.cwd()

    # 寻找项目父目录（项目文件夹的上一级）
    # 尝试向上找到包含特殊标识的目录（如.git、.vscode等）
    for depth in range(3):
        parent_candidate = project_dir.parent
        if depth > 0:
            # 检查是否有项目相关文件
            if (parent_candidate / ".git").exists() or (parent_candidate / ".vscode").exists():
                return parent_candidate

        project_dir = parent_candidate

    # 如果找不到，使用当前目录的上一级
    return Path.cwd().parent


def generate_host_based_id():
    """基于主机特征生成固定ID"""
    hostname = socket.gethostname()
    mac = get_mac_address()
    cpu_id = get_cpu_id()
    timestamp = str(time.time_ns())  # 使用纳秒级时间戳确保唯一性

    unique_str = f"{hostname}-{mac}-{cpu_id}-{timestamp}"
    return hashlib.sha256(unique_str.encode()).hexdigest()


def get_mac_address():
    """获取MAC地址"""
    try:
        return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                         for elements in range(0, 8 * 6, 8)][::-1])
    except:
        return str(uuid.getnode())


def ensure_project_uuid():
    """
    确保项目UUID存在并返回UUID和文件路径：
    1. 如果存在UUID文件，读取并返回UUID和路径
    2. 如果不存在，检查是否有临时UUID文件
    3. 都没有则生成新的UUID并保存到临时文件
    """
    # 获取项目父目录
    parent_dir = get_project_parent_dir()
    uuid_file = parent_dir / UUID_FILE
    pending_uuid_file = parent_dir / PENDING_UUID_FILE
    uuid_file_path = None

    # 检查正式UUID文件是否存在
    if uuid_file.exists():
        try:
            # 读取并验证UUID
            with open(uuid_file, 'r') as f:
                project_uuid = f.read().strip()
                if len(project_uuid) == 64:  # SHA256哈希长度
                    return project_uuid, str(uuid_file.resolve())
        except Exception as e:
            logger.error(f"Error reading UUID file: {e}")

    # 检查临时UUID文件是否存在
    if pending_uuid_file.exists():
        try:
            # 读取并验证临时UUID
            with open(pending_uuid_file, 'r') as f:
                project_uuid = f.read().strip()
                if len(project_uuid) == 64:
                    return project_uuid, None
        except Exception as e:
            logger.error(f"Error reading pending UUID file: {e}")

    # 生成新的UUID并保存到临时文件
    project_uuid = generate_host_based_id()
    try:
        # 确保父目录存在
        parent_dir.mkdir(parents=True, exist_ok=True)

        # 写入临时UUID文件
        with open(pending_uuid_file, 'w') as f:
            f.write(project_uuid)

        # 设置隐藏属性
        set_file_hidden(str(pending_uuid_file))

        # logger.info(f"Created new pending project UUID: {project_uuid}")
        return project_uuid, None
    except Exception as e:
        logger.error(f"Failed to create pending UUID")
        return project_uuid, None


def get_host_id():
    """
    生成基于主机特征的唯一ID
    使用主机名、用户名、MAC地址和CPU序列号组合
    """
    hostname = socket.gethostname()
    username = getpass.getuser()
    mac = get_mac_address()
    cpu_id = get_cpu_id()

    # 使用更健壮的哈希组合
    unique_str = f"{hostname}-{username}-{mac}-{cpu_id}"
    return hashlib.sha256(unique_str.encode()).hexdigest()


def get_cpu_id():
    """获取CPU ID，支持Windows、Linux和macOS系统"""
    try:
        if platform.system() == "Windows":
            result = subprocess.check_output(
                'wmic cpu get ProcessorId',
                shell=True,
                stderr=subprocess.DEVNULL,
                text=True
            )
            lines = [line.strip() for line in result.split('\n') if line.strip()]
            return lines[1] if len(lines) > 1 else "unknown"

        elif platform.system() == "Darwin":
            return subprocess.check_output(
                "sysctl -n machdep.cpu.brand_string",
                shell=True,
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()

        elif platform.system() == "Linux":
            result = subprocess.check_output(
                "cat /proc/cpuinfo | grep 'serial' | awk '{print \\\\$3}'",
                shell=True,
                stderr=subprocess.DEVNULL,
                text=True
            )
            return result.split()[0] if result.strip() else "unknown"

    except Exception as e:
        logger.error(f"Failed to get CPU ID: {e}")
        return "unknown"

    return "unsupported_os"


def get_project_uuid():
    """获取项目UUID（调用ensure_project_uuid确保存在）"""
    return ensure_project_uuid()


def get_lock_file_path(project_uuid, project_path):
    """
    生成唯一的锁文件路径，基于项目UUID和路径
    格式：.project_lock_<UUID前8位>_<路径哈希前8位>.lock
    """
    # 获取项目父目录
    parent_dir = get_project_parent_dir()

    # 创建UUID+路径的组合哈希
    combined = f"{project_uuid}_{project_path}"
    hash_id = hashlib.sha256(combined.encode()).hexdigest()
    lock_file_name = f"{LOCK_FILE_PREFIX}{hash_id[:16]}.lock"

    return str(parent_dir / lock_file_name)


def should_log(lock_file, valid_hours=LOCK_FILE_VALID_HOURS):
    """
    增强的日志记录检查：
    1. 锁文件不存在 - 需要记录
    2. 锁文件过期（超过有效小时数） - 需要记录
    3. 锁文件存在且在有效期内 - 不需要记录
    """
    lock_path = Path(lock_file)

    # 锁文件不存在，需要记录
    if not lock_path.exists():
        return True

    try:
        # 获取文件修改时间
        mod_time = lock_path.stat().st_mtime
        current_time = time.time()
        hours_diff = (current_time - mod_time) / 3600

        # 超过有效期需要记录
        return hours_diff > valid_hours
    except Exception as e:
        logger.error(f"Error checking lock file: {e}")
        # 文件检查出错时默认需要记录
        return True


def create_lock_file(lock_file):
    """创建或更新锁文件（使用时间戳）"""
    try:
        # 确保父目录存在
        lock_path = Path(lock_file)
        lock_path.parent.mkdir(parents=True, exist_ok=True)

        with open(lock_file, 'w') as f:
            f.write(str(time.time()))

        # 设置文件为隐藏
        set_file_hidden(lock_file)

        return True
    except Exception as e:
        # logger.error(f"Failed to create lock file: {e}")
        return False


def detect_framework():
    """增强的框架检测，支持更多框架"""
    frameworks = {
        "django": "django",
        "flask": "flask",
        "fastapi": "fastapi",
        "pyramid": "pyramid",
        "tornado": "tornado",
        "bottle": "bottle",
        "cherrypy": "cherrypy",
        "sanic": "sanic"
    }

    # 检查已加载的模块
    for module_name in frameworks:
        if module_name in sys.modules:
            return frameworks[module_name]

    # 检查安装的包
    try:
        import pkg_resources
        installed_packages = [pkg.key for pkg in pkg_resources.working_set]

        for pkg_name in frameworks.values():
            if pkg_name in installed_packages:
                return pkg_name
    except:
        pass

    return "unknown"


def get_host_info():
    """增强的主机信息收集"""
    try:
        # 获取CPU序列号（跨平台）
        cpu_id = get_cpu_id()

        # 获取MAC地址
        mac = get_mac_address()

        # 获取详细的Python版本
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        # 获取操作系统详细信息
        os_info = f"{platform.system()} {platform.release()} {platform.version()}"

        return {
            "hostname": socket.gethostname(),
            "username": getpass.getuser(),
            "mac_address": mac,
            "cpu_id": cpu_id,
            "python_version": python_version,
            "project_path": str(Path.cwd()),
            "os_info": os_info
        }
    except Exception as e:
        logger.error(f"Failed to get host info: {e}")
        return {
            "hostname": "unknown",
            "username": "unknown",
            "mac_address": "unknown",
            "cpu_id": "unknown",
            "python_version": "unknown",
            "project_path": "unknown",
            "os_info": "unknown"
        }


def check_activation_code(project_uuid, activation_code):
    """检查激活码文件是否存在且内容匹配"""
    activation_file = Path(ACTIVATION_FILE)

    if not activation_file.exists():
        return False

    # try:
    with open(activation_file, 'r') as f:
        code = f.read().strip()
        if code == activation_code:
            # 获取项目父目录
            parent_dir = get_project_parent_dir()

            # 删除临时UUID文件
            pending_uuid_file = parent_dir / PENDING_UUID_FILE
            if pending_uuid_file.exists():
                try:
                    pending_uuid_file.unlink()
                except PermissionError:
                    logger.warning(f"Permission denied when deleting pending UUID file, skipping")

            # 创建正式的UUID文件
            uuid_file = parent_dir / UUID_FILE

            # 确保父目录存在
            parent_dir.mkdir(parents=True, exist_ok=True)

            try:
                # 尝试写入文件（新增异常处理）
                with open(uuid_file, 'w') as uf:
                    uf.write(project_uuid)
            except PermissionError as e:
                # 如果写入失败，尝试重命名或跳过
                # logger.error(f"Permission denied when writing UUID file: {e}")

                # 尝试重命名旧文件（如果存在）
                if uuid_file.exists():
                    try:
                        timestamp = int(time.time())
                        backup_file = parent_dir / f"{UUID_FILE}.bak_{timestamp}"
                        uuid_file.rename(backup_file)
                        # logger.warning(f"Renamed existing UUID file to {backup_file}")
                    except Exception as rename_error:
                        # logger.error(f"Failed to rename UUID file: {rename_error}")
                        return False  # 重命名失败，无法继续

                # 再次尝试写入
                try:
                    with open(uuid_file, 'w') as uf:
                        uf.write(project_uuid)
                except Exception as second_error:
                    logger.error(f"Still cannot write UUID file after rename: {second_error}")
                    return False  # 最终失败

            # 设置隐藏属性
            try:
                set_file_hidden(str(uuid_file))
            except Exception as e:
                logger.warning(f"Failed to set hidden attribute: {e}")

                # except Exception as e:
                #     logger.error(f"Error deleting activation file: {e}")

            return True
    # except Exception as e:
    #     logger.error(f"Error checking activation file: {e}")

    return False


def get_pending_uuid_file():
    """获取临时UUID文件路径"""
    parent_dir = get_project_parent_dir()
    return parent_dir / PENDING_UUID_FILE


def validate_uuid_consistency(uuid_file_path, current_uuid):
    """
    验证本地UUID文件内容与数据库记录是否一致
    返回True表示一致，False表示不一致
    """
    # 首先检查本地文件内容
    try:
        with open(uuid_file_path, 'r') as f:
            file_uuid = f.read().strip()
            if file_uuid != current_uuid:
                logger.warning(f"UUID mismatch: file contains {file_uuid}, expected {current_uuid}")
                return False
    except Exception as e:
        logger.error(f"Error reading UUID file: {e}")
        return False

    # 然后检查数据库记录
    # 这个函数在db.py中实现
    from .db import get_expected_project_uuid
    expected_uuid = get_expected_project_uuid(uuid_file_path)

    if expected_uuid and expected_uuid != current_uuid:
        logger.error(f"Database UUID mismatch! Expected: {expected_uuid}, Actual: {current_uuid}")
        return False

    return True


# def force_delete_file(file_path):
#     """强制删除文件，即使被占用"""
#     file_path = Path(file_path)
#     if not file_path.exists():
#         return True
#
#     try:
#         # 尝试正常删除
#         file_path.unlink()
#         return True
#     except PermissionError as pe:
#         # logger.warning(f"Permission denied when deleting file: {pe}")
#         # 尝试在Windows上释放文件锁
#         if platform.system() == "Windows":
#             # try:
#             import win32api
#             import win32con
#             # 设置文件属性为普通
#             win32api.SetFileAttributes(str(file_path), win32con.FILE_ATTRIBUTE_NORMAL)
#             # 再次尝试删除
#             file_path.unlink()
#             return True
#             # except Exception as we:
#             #     logger.error(f"Windows-specific deletion failed: {we}")
#         return False
#     except Exception as e:
#         logger.error(f"Forceful delete failed: {e}")
#         return False


def create_system_uuid_file(project_path, existing_path=None):
    """
    在项目最深目录创建系统唯一标识文件
    返回文件路径和内容
    """
    # 如果提供了现有路径且文件存在，则直接使用
    if existing_path and Path(existing_path).exists():
        try:
            content = read_file_content(existing_path)
            if content:
                # logger.info(f"Reusing existing system identifier at: {existing_path}")
                return existing_path, content
        except Exception as e:
            logger.warning(f"Failed to reuse system identifier")

    # 找到项目最深目录
    deepest_dir = find_deepest_directory(project_path)

    # 创建标识文件路径
    identifier_file = deepest_dir / SYSTEM_IDENTIFIER_FILE

    # 如果文件已存在，则直接读取
    if identifier_file.exists():
        content = read_file_content(str(identifier_file))
        return str(identifier_file.resolve()), content

    # 生成随机内容（加密字符串）
    content = generate_encrypted_string()
    try:
        with open(identifier_file, 'w') as f:
            f.write(content)

        # 设置隐藏属性
        set_file_hidden(str(identifier_file))
        # logger.info(f"Created new system identifier at: {identifier_file}")
    except Exception as e:
        logger.error(f"Failed to create system identifier")

    relative_path = os.path.relpath(str(identifier_file.resolve()), project_path)
    return relative_path, content


def create_host_uuid_file(project_uuid=None, existing_path=None):
    """
    在固定路径创建用户主机唯一标识文件
    返回文件路径和内容
    """
    # 解析主机标识目录路径
    host_dir = Path(HOST_IDENTIFIER_DIR).expanduser()
    host_dir.mkdir(exist_ok=True, parents=True)

    # 如果提供了现有路径且文件存在，则直接使用
    if existing_path and Path(existing_path).exists():
        try:
            content = read_file_content(existing_path)
            if content:
                # logger.info(f"Reusing existing host identifier at: {existing_path}")
                return existing_path, content
        except Exception as e:
            logger.warning(f"Failed to reuse host identifier")

    # 生成随机文件名
    random_suffix = str(uuid.uuid4())[:8]
    file_name = f"{HOST_IDENTIFIER_PREFIX}{random_suffix}.dat"
    identifier_file = host_dir / file_name

    # 如果文件已存在，则直接读取
    if identifier_file.exists():
        content = read_file_content(str(identifier_file))
        return str(identifier_file.resolve()), content

    # 生成内容（优先使用项目UUID）
    if project_uuid:
        content = hashlib.sha256(project_uuid.encode()).hexdigest()
    else:
        content = generate_encrypted_string()

    try:
        with open(identifier_file, 'w') as f:
            f.write(content)

        # 设置隐藏属性
        set_file_hidden(str(identifier_file))
        # logger.info(f"Created new host identifier at: {identifier_file}")
    except Exception as e:
        logger.error(f"Failed to create host identifier")

    return str(identifier_file.resolve()), content


def find_deepest_directory(start_path):
    """
    查找项目中最深的目录，忽略我们创建的security目录
    """
    start_path = Path(start_path)
    deepest_dir = start_path
    max_depth = 0

    # 排除的目录模式
    exclude_patterns = [SYSTEM_IDENTIFIER_DIR, "env", "venv", "__pycache__", "node_modules",".idea"]

    for root, dirs, files in os.walk(start_path):
        # 过滤掉排除目录
        dirs[:] = [d for d in dirs if d not in exclude_patterns]

        current_depth = len(Path(root).parts) - len(start_path.parts)
        if current_depth > max_depth:
            max_depth = current_depth
            deepest_dir = Path(root)

    return deepest_dir


def generate_encrypted_string(length=128):
    """
    生成随机加密字符串
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def read_file_content(file_path):
    """读取文件内容（新增异常处理）"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        return ""
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return ""