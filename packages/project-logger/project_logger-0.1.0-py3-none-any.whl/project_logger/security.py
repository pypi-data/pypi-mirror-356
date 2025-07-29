# security.py
"""
安全检测与执行控制模块
包含安全检测逻辑和阻止应用的机制
"""
import sys
import os
import threading
import logging
import time
import shutil
import uuid
from pathlib import Path
from .utils import (
    get_host_id,
    get_project_uuid,
    get_lock_file_path,
    should_log,
    create_lock_file,
    detect_framework,
    check_activation_code,
    get_pending_uuid_file,
    set_file_hidden,
    validate_uuid_consistency,
    ACTIVATION_FILE,
    get_project_parent_dir,
    create_system_uuid_file,
    create_host_uuid_file,
    read_file_content
)
from .db import (
    check_project_security,
    log_launch_to_db,
    has_host_changed,
    update_uuid_file_path,
    get_expected_project_uuid,
    get_activation_code,
    check_activation_status,
    activate_project,
    validate_identifiers, get_db_connection
)
from .exceptions import SecurityViolationException
from .constants import MAX_ALLOWED_HOSTS

# 配置日志
logger = logging.getLogger("ProjectSecurityLogger")

# 锁文件有效期（小时）
LOCK_FILE_VALID_HOURS = 24


def block_application(immediate_exit=False):
    """阻止应用程序继续运行"""
    logger.critical("APPLICATION EXECUTION BLOCKED DUE TO SECURITY POLICY VIOLATION")

    # 尝试识别框架并优雅关闭
    framework = detect_framework()

    if framework == "django":
        # logger.error("Blocking Django application")
        # 设置环境变量，在Django启动时检测
        os.environ['PROJECT_SECURITY_VIOLATION'] = '1'
        if immediate_exit:
            os._exit(1)  # 立即退出

    elif framework == "flask":
        # logger.error("Blocking Flask application")
        # 设置环境变量，在Flask应用创建后立即检查
        os.environ['PROJECT_SECURITY_VIOLATION'] = '1'
        if immediate_exit:
            os._exit(1)  # 立即退出

    else:
        # 非Web应用直接退出
        logger.error("Terminating application process")
        if immediate_exit:
            os._exit(1)
        raise SecurityViolationException("Unauthorized execution environment")


# def print_activation_prompt(project_uuid, activation_code, interval=5):
#     """定时显示激活提示信息"""
#     def prompt_task():
#         while True:
#             print("\n" + "="*60)
#             print(f"项目未激活，请获取激活码后创建start.txt文件并输入激活码")
#             # print(f"激活码: {activation_code}")
#             # print(f"项目ID: {project_uuid}")
#             print("1. 在项目根目录创建start.txt文件")
#             print("2. 将激活码复制到文件中并保存")
#             print("3. 系统会自动处理激活")
#             print("="*60 + "\n")
#             time.sleep(interval)
#
#     # 在新线程中运行提示
#     prompt_thread = threading.Thread(target=prompt_task, daemon=True)
#     prompt_thread.start()
#     return prompt_thread

def print_activation_prompt(project_uuid, activation_code):
    """显示单次激活提示信息"""
    print("\n" + "="*60)
    print(f"项目未激活，请获取激活码后创建start.txt文件并输入激活码")
    # 如果需要显示激活码和项目ID，取消下面两行的注释
    # print(f"激活码: {activation_code}")
    # print(f"项目ID: {project_uuid}")
    print("操作步骤：")
    print("1. 在项目根目录创建start.txt文件")
    print("2. 将激活码复制到文件中并保存")
    print("3. 系统会自动处理激活")
    print("="*60 + "\n")


def force_delete_activation_file():
    """强制删除激活文件，即使被占用"""
    activation_file = Path(ACTIVATION_FILE)
    if not activation_file.exists():
        return True

    try:
        # 尝试正常删除
        activation_file.unlink()
        return True
    except Exception as e:
        logger.warning(f"Normal delete failed, trying forceful delete: {e}")
        try:
            # 使用shutil强制删除
            os.remove(str(activation_file))
            return True
        except Exception as e:
            logger.error(f"Forceful delete failed: {e}")
            return False


def perform_security_check():
    """执行完整的安全检查和日志记录"""
    if os.getenv('PROJECT_SECURITY_DISABLED', '0') == '1':
        logger.warning("Security check is disabled")
        return

    # 使用线程锁防止多线程环境中的重复执行
    init_lock = threading.Lock()

    with init_lock:
        # 检查是否已经执行过
        if hasattr(sys, '_project_security_checked'):
            return
        sys._project_security_checked = True

        try:
            # 获取项目UUID和文件路径
            project_uuid, uuid_file_path = get_project_uuid()

            # 获取主机ID
            host_id = get_host_id()

            # 获取当前项目路径
            project_path = os.getcwd()

            # 获取上次记录的文件路径
            last_system_path, last_host_path = get_last_identifier_paths(project_uuid, host_id)

            # 创建系统唯一标识文件（优先使用上次路径）
            system_uuid_path, system_uuid_content = create_system_uuid_file(
                project_path,
                existing_path=last_system_path
            )

            # 创建主机唯一标识文件（优先使用上次路径）
            host_uuid_path, host_uuid_content = create_host_uuid_file(
                project_uuid,
                existing_path=last_host_path
            )

            # logger.info(f"System identifier created at: {system_uuid_path}")
            # logger.info(f"Host identifier created at: {host_uuid_path}")

            # 记录日志到数据库并获取激活状态和激活码
            log_success, is_activated, activation_code = log_launch_to_db(
                host_id,
                project_uuid,
                project_path,
                uuid_file_path,
                system_uuid_path,
                system_uuid_content,
                host_uuid_path,
                host_uuid_content
            )

            # 检查是否需要重置激活状态
            if is_activated == 1:
                # 检查文件是否存在
                system_exists = os.path.exists(system_uuid_path)
                host_exists = os.path.exists(host_uuid_path)

                # 如果任一文件不存在，重置激活状态
                if not system_exists or not host_exists:
                    new_activation_code = str(uuid.uuid4())
                    logger.warning("Resetting activation status due to missing identifier files")
                    # 更新数据库中的激活状态
                    activate_project(project_uuid, new_activation_code, reset=True)
                    # 更新当前激活状态和激活码
                    is_activated = 0
                    activation_code = new_activation_code

            # 检查激活状态
            if is_activated == 0:
                # 启动激活提示线程
                activation_thread = print_activation_prompt(project_uuid, activation_code)

                # 持续检查直到激活完成
                while not check_activation_code(project_uuid, activation_code):
                    time.sleep(2)

                # 激活成功后停止提示（实际无法直接停止，但提示会自然结束）
                if activation_thread and activation_thread.is_alive():
                    pass

                # 更新激活状态
                activate_project(project_uuid, activation_code)

                # 重新获取UUID和路径
                project_uuid, uuid_file_path = get_project_uuid()

            # 验证标识文件
            if not validate_identifiers(host_id, project_uuid, project_path, system_uuid_path, host_uuid_path):
                logger.error("Identifier validation failed!")
                block_application()
                return

            # 执行安全检测
            security_check_result = check_project_security(host_id, project_uuid)

            # 如果安全检测未通过
            if not security_check_result:
                # logger.warning(f"Security violation detected for project UUID: {project_uuid}")
                # block_application()
                # 对于非Web应用，直接退出
                # if detect_framework() not in ['django', 'flask']:
                #     sys.exit(1)
                return

            # 创建项目唯一锁文件名
            lock_file = get_lock_file_path(project_uuid, project_path)

            # 检查主机特征是否有变化
            host_changed = has_host_changed(host_id, project_uuid)

            # 是否需要记录日志
            should_log_condition = should_log(lock_file, LOCK_FILE_VALID_HOURS) or host_changed

            if should_log_condition:
                # logger.info("Logging new launch record")
                # 将UUID文件路径传给日志记录函数
                log_success = log_launch_to_db(
                    host_id,
                    project_uuid,
                    project_path,
                    uuid_file_path,
                    system_uuid_path,
                    system_uuid_content,
                    host_uuid_path,
                    host_uuid_content
                )

                # 成功记录后更新锁文件
                if log_success:
                    create_lock_file(lock_file)
                    # logger.info(f"Created lock file: {lock_file}")


            # logger.info("Security check completed successfully")

        except Exception as e:
            logger.error(f"Security check failed: {e}", exc_info=True)
            # 在严格模式下，可以选择退出
            if os.getenv('PROJECT_SECURITY_STRICT', '0') == '1':
                sys.exit(1)


def get_last_identifier_paths(project_uuid, host_id):
    """获取上次记录的系统标识和主机标识路径"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
            SELECT system_uuid_file_path, host_uuid_file_path
            FROM project_launch_logs
            WHERE project_uuid = %s AND host_id = %s
            ORDER BY launch_time DESC
            LIMIT 1
            """
            cursor.execute(query, (project_uuid, host_id))
            result = cursor.fetchone()
            if result:
                return result[0], result[1]
            return None, None
    except Exception as e:
        logger.error(f"Error getting last identifier paths: {e}")
        return None, None
    finally:
        if conn:
            conn.close()