# db.py
import os
import logging
import pymysql
import uuid
from dbutils.pooled_db import PooledDB
from .utils import (
    get_host_info,
    get_project_parent_dir,
    create_system_uuid_file,
    create_host_uuid_file,
    read_file_content,
    set_file_hidden
)
from .exceptions import DatabaseConnectionException

# 配置日志
logger = logging.getLogger("ProjectSecurityLogger")

# 连接池全局变量
db_pool = None
pool_initialized = False

# 允许的最大主机数量
from .constants import MAX_ALLOWED_HOSTS


def initialize_db_pool():
    """初始化数据库连接池"""
    global db_pool, pool_initialized

    if pool_initialized:
        return db_pool

    try:
        # 从环境变量获取数据库配置
        db_config = {
            'host': os.getenv('DB_HOST', 'mysql5.sqlpub.com'),
            'user': os.getenv('DB_USER', 'funnel'),
            'password': os.getenv('DB_PASSWORD', 'BX4FwWuqDrciPg8H'),
            'database': os.getenv('DB_NAME', 'do_not_use'),
            'port': int(os.getenv('DB_PORT', '3310')),
            'connect_timeout': 5,
        }

        # SSL配置
        ssl_config = {}
        if os.getenv('DB_SSL', 'false').lower() == 'true':
            ssl_ca = os.getenv('DB_SSL_CA', '')
            ssl_cert = os.getenv('DB_SSL_CERT', '')
            ssl_key = os.getenv('DB_SSL_KEY', '')

            if ssl_ca and ssl_cert and ssl_key:
                ssl_config = {
                    'ssl': {
                        'ca': ssl_ca,
                        'cert': ssl_cert,
                        'key': ssl_key,
                        'check_hostname': False
                    }
                }
            else:
                logger.warning("DB_SSL is true but SSL files not provided. Using default SSL context")
                ssl_config = {'ssl': True}

        # 创建pymysql连接池
        db_pool = PooledDB(
            creator=pymysql,
            maxconnections=10,  # 增加连接池大小
            blocking=True,
            setsession=[],
            ping=1,  # 每次使用时ping服务器检查连接
            **db_config,
            **ssl_config
        )

        pool_initialized = True
        # logger.info("Database connection pool initialized with pymysql")
        return db_pool

    except Exception as e:
        # logger.error(f"Database pool initialization failed: {e}", exc_info=True)
        raise DatabaseConnectionException("Failed to initialize database pool") from e


def get_db_connection():
    """获取数据库连接"""
    global db_pool

    if not pool_initialized:
        initialize_db_pool()

    try:
        conn = db_pool.connection()
        return conn
    except Exception as e:
        logger.error(f"Failed to get database connection: {e}", exc_info=True)
        raise DatabaseConnectionException("Failed to get database connection") from e


def check_project_security(host_id, project_uuid):
    """
    增强的安全策略：
    1. 检查项目是否已启动
    2. 如果项目未启动或当前主机是最早的两台设备之一，允许运行
    3. 否则阻止执行

    使用 first_launch_time 字段判断最早的两台主机
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 第一步：获取项目启动的最早两台主机（按首次启动时间排序）
            early_hosts_query = """
            SELECT host_id, MIN(first_launch_time) as first_time 
            FROM project_launch_logs 
            WHERE project_uuid = %s 
            GROUP BY host_id 
            ORDER BY first_time ASC 
            LIMIT %s
            """
            cursor.execute(early_hosts_query, (project_uuid, MAX_ALLOWED_HOSTS))
            early_hosts = cursor.fetchall()
            early_host_ids = [host[0] for host in early_hosts] if early_hosts else []

            # 如果项目未启动或当前主机是最早的之一，允许运行
            if not early_hosts or host_id in early_host_ids:
                # logger.info(f"Project authorized on this host (one of the first {MAX_ALLOWED_HOSTS} hosts)")
                return True

            # 获取当前主机的首次启动时间
            current_host_query = """
            SELECT first_launch_time 
            FROM project_launch_logs 
            WHERE project_uuid = %s AND host_id = %s
            ORDER BY first_launch_time ASC
            LIMIT 1
            """
            cursor.execute(current_host_query, (project_uuid, host_id))
            current_host_time = cursor.fetchone()

            # 如果当前主机有记录但不在前面，记录警告
            # if current_host_time and current_host_time[0]:
            #     logger.warning(
            #         f"Host first started at {current_host_time[0]} but is not in the first {MAX_ALLOWED_HOSTS} hosts")

            # 列出最早的两台设备及其首次启动时间
            # logger.warning(
            #     f"First {MAX_ALLOWED_HOSTS} hosts allowed: {[f'{host_id[:8]}... (first: {first_time})' for host_id, first_time in early_hosts]}")

            # 当前主机不是最早的两台，阻止运行
            return False

    except Exception as e:
        logger.error(f"Security check database error: {e}", exc_info=True)
        # 安全检测失败时默认允许执行，避免阻塞合法操作
        return True
    finally:
        if conn:
            conn.close()


def log_launch_to_db(host_id, project_uuid, project_path, uuid_file_path,
                     system_uuid_path, system_uuid_content,
                     host_uuid_path, host_uuid_content):
    """记录启动日志到数据库，优先更新相同主机ID和系统标识内容的记录"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 第一步：检查是否存在相同主机ID和系统标识内容的记录
            check_query = """
            SELECT id, first_launch_time, is_activated, activation_code 
            FROM project_launch_logs 
            WHERE host_id = %s 
              AND system_uuid_content = %s
            ORDER BY first_launch_time ASC
            LIMIT 1
            """
            cursor.execute(check_query, (host_id, system_uuid_content))
            existing_record = cursor.fetchone()

            # 如果找到匹配记录，更新现有记录
            if existing_record:
                record_id, first_launch_time, is_activated, existing_activation_code = existing_record
                update_query = """
                UPDATE project_launch_logs 
                SET 
                    project_uuid = %s,
                    project_path = %s,
                    uuid_file_path = %s,
                    launch_time = NOW(),
                    hostname = %s,
                    username = %s,
                    mac_address = %s,
                    cpu_id = %s,
                    python_version = %s,
                    os_info = %s,
                    system_uuid_file_path = %s,
                    host_uuid_file_path = %s,
                    host_uuid_content = %s
                WHERE id = %s
                """
                host_info = get_host_info()
                cursor.execute(update_query, (
                    project_uuid,
                    project_path,
                    uuid_file_path,
                    host_info["hostname"],
                    host_info["username"],
                    host_info["mac_address"],
                    host_info["cpu_id"],
                    host_info["python_version"],
                    host_info["os_info"],
                    system_uuid_path,
                    host_uuid_path,
                    host_uuid_content,
                    record_id
                ))
                conn.commit()
                return True, is_activated, existing_activation_code

            # 第二步：如果没有匹配记录，检查是否存在相同主机ID和项目路径的记录
            check_path_query = """
            SELECT id, first_launch_time, is_activated, activation_code 
            FROM project_launch_logs 
            WHERE host_id = %s 
              AND project_path = %s
            LIMIT 1
            """
            cursor.execute(check_path_query, (host_id, project_path))
            existing_path_record = cursor.fetchone()

            # 更新现有记录（基于项目路径）
            if existing_path_record:
                record_id, first_launch_time, is_activated, existing_activation_code = existing_path_record
                update_query = """
                UPDATE project_launch_logs 
                SET 
                    project_uuid = %s,
                    uuid_file_path = %s,
                    launch_time = NOW(),
                    hostname = %s,
                    username = %s,
                    mac_address = %s,
                    cpu_id = %s,
                    python_version = %s,
                    os_info = %s,
                    system_uuid_file_path = %s,
                    system_uuid_content = %s,
                    host_uuid_file_path = %s,
                    host_uuid_content = %s
                WHERE id = %s
                """
                host_info = get_host_info()
                cursor.execute(update_query, (
                    project_uuid,
                    uuid_file_path,
                    host_info["hostname"],
                    host_info["username"],
                    host_info["mac_address"],
                    host_info["cpu_id"],
                    host_info["python_version"],
                    host_info["os_info"],
                    system_uuid_path,
                    system_uuid_content,
                    host_uuid_path,
                    host_uuid_content,
                    record_id
                ))
                conn.commit()
                return True, is_activated, existing_activation_code

            # 第三步：如果都没有找到，插入新记录
            # 获取主机信息
            host_info = get_host_info()

            insert_query = """
            INSERT INTO project_launch_logs (
                host_id, 
                project_uuid,
                project_path,
                uuid_file_path,
                first_launch_time,
                hostname,
                username,
                mac_address,
                cpu_id,
                python_version,
                os_info,
                activation_code,
                is_activated,
                system_uuid_file_path,
                system_uuid_content,
                host_uuid_file_path,
                host_uuid_content
            ) VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 生成激活码（UUID格式）
            activation_code = str(uuid.uuid4())

            values = (
                host_id,
                project_uuid,
                project_path,
                uuid_file_path,
                host_info["hostname"],
                host_info["username"],
                host_info["mac_address"],
                host_info["cpu_id"],
                host_info["python_version"],
                host_info["os_info"],
                activation_code,
                0,  # 默认未激活
                system_uuid_path,
                system_uuid_content,
                host_uuid_path,
                host_uuid_content
            )

            cursor.execute(insert_query, values)
            conn.commit()
            return True, 0, activation_code

    except Exception as e:
        logger.error(f"Database error during logging: {e}", exc_info=True)
        return False, 0, None
    finally:
        if conn:
            conn.close()


def update_uuid_file_path(host_id, project_uuid, uuid_file_path):
    """
    更新数据库中记录的UUID文件路径
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 更新查询
            update_query = """
            UPDATE project_launch_logs 
            SET uuid_file_path = %s
            WHERE host_id = %s 
              AND project_uuid = %s
            """

            cursor.execute(update_query, (
                uuid_file_path,
                host_id,
                project_uuid
            ))

            if cursor.rowcount > 0:
                # logger.info(f"Successfully updated UUID file path: {uuid_file_path}")
                conn.commit()
                return True
            else:
                # logger.warning("No matching record found for UUID file path update")
                return False

    except Exception as e:
        logger.error(f"Database error during UUID file path update", exc_info=True)
        return False
    finally:
        if conn:
            conn.close()


def has_host_changed(host_id, project_uuid):
    """
    检查主机特征是否有变化：
    1. 项目首次运行：默认为有变化
    2. 数据库中不存在相同主机ID：有变化
    3. 存在相同主机ID但特征不同：有变化

    使用 first_launch_time 字段判断主机首次运行时间
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 检查该项目是否有历史记录
            query = """
            SELECT host_id, MIN(first_launch_time) as first_time 
            FROM project_launch_logs 
            WHERE project_uuid = %s
            GROUP BY host_id
            """
            cursor.execute(query, (project_uuid,))
            results = cursor.fetchall()

            # 项目第一次运行
            if not results:
                # logger.info("Project is running for the first time")
                return True

            # 检查当前主机是否在历史记录中
            host_found = False
            for result in results:
                stored_host_id, first_time = result
                if stored_host_id == host_id:
                    # logger.info(f"Project authorized on this host (first run: {first_time})")
                    host_found = True
                    break

            # 主机特征已变化
            if not host_found:
                # logger.warning(f"Host characteristics changed, new host detected")
                return True

            return False  # 主机特征未变化

    except Exception as e:
        logger.error(f"Host change check database error", exc_info=True)
        # 出错时保守返回True，确保日志被记录
        return True
    finally:
        if conn:
            conn.close()


def get_expected_project_uuid(uuid_file_path):
    """
    根据UUID文件路径获取预期的项目UUID
    用于验证本地UUID与数据库记录是否一致
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
            SELECT project_uuid 
            FROM project_launch_logs 
            WHERE uuid_file_path = %s
            ORDER BY first_launch_time ASC
            LIMIT 1
            """
            cursor.execute(query, (uuid_file_path,))
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        logger.error(f"Error getting expected UUID: {e}")
        return None
    finally:
        if conn:
            conn.close()


def get_activation_code(project_uuid):
    """从数据库获取激活码"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
            SELECT activation_code 
            FROM project_launch_logs 
            WHERE project_uuid = %s
            ORDER BY first_launch_time ASC
            LIMIT 1
            """
            cursor.execute(query, (project_uuid,))
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        logger.error(f"Error getting activation code: {e}")
        return None
    finally:
        if conn:
            conn.close()


def check_activation_status(project_uuid):
    """检查项目是否已激活"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
            SELECT is_activated 
            FROM project_launch_logs 
            WHERE project_uuid = %s
            ORDER BY first_launch_time ASC
            LIMIT 1
            """
            cursor.execute(query, (project_uuid,))
            result = cursor.fetchone()
            return result[0] if result else False
    except Exception as e:
        logger.error(f"Error checking activation status: {e}")
        return False
    finally:
        if conn:
            conn.close()


def activate_project(project_uuid, activation_code):
    """激活项目"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            update_query = """
            UPDATE project_launch_logs 
            SET is_activated = 1
            WHERE project_uuid = %s
              AND activation_code = %s
            """
            cursor.execute(update_query, (project_uuid, activation_code))

            if cursor.rowcount > 0:
                conn.commit()
                # logger.info(f"Project {project_uuid} activated successfully")
                return True
            else:
                # logger.warning(f"Activation failed for project {project_uuid}")
                return False
    except Exception as e:
        logger.error(f"Database error during activation")
        return False
    finally:
        if conn:
            conn.close()


def validate_identifiers(host_id, project_uuid, current_project_path, system_uuid_path, host_uuid_path):
    """验证系统标识和主机标识是否匹配数据库记录"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                SELECT system_uuid_file_path, system_uuid_content, host_uuid_content 
                FROM project_launch_logs 
                WHERE project_uuid = %s
                  AND host_id = %s
                LIMIT 1
                """
            cursor.execute(query, (project_uuid, host_id))
            result = cursor.fetchone()

            if not result:
                return False

            stored_system_path, stored_system_content, stored_host_content = result

            # 处理相对路径：转换为当前项目下的绝对路径
            if not os.path.isabs(stored_system_path):
                actual_system_path = os.path.join(current_project_path, stored_system_path)
            else:
                actual_system_path = stored_system_path

            # 读取本地文件内容
            current_system_content = read_file_content(actual_system_path)
            current_host_content = read_file_content(host_uuid_path)

            # 验证内容是否匹配
            system_match = stored_system_content == current_system_content
            host_match = stored_host_content == current_host_content

            return system_match and host_match

    except Exception as e:
        logger.error(f"Identifier validation error")
        return False
    finally:
        if conn:
            conn.close()