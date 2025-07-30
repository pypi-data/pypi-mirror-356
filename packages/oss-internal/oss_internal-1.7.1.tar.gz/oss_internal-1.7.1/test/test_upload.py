import sys
import os
import tempfile
import datetime
import asyncio
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.oss_internal.oss_upload import (
    upload_file_to_oss, 
    batch_upload_file_to_oss, 
    aupload_file_to_oss, 
    abatch_upload_file_to_oss,
    upload_directory_to_oss,
    aupload_directory_to_oss,
    upload_large_file_to_oss_v2
)
from src.oss_internal.oss_download import (
    download_single_file_from_oss,
    download_batch_files_from_oss,
    download_large_file_from_oss
)
from src.oss_internal.schemas.error import EmptyDirectoryError, NotADirectoryError, FileNotFoundError

if __name__ == "__main__":
    # 测试配置
    ALI_ACCESS_KEY_ID = 'LTAI5tQe2TUCGB5q7AAaD3rX'
    ALI_ACCESS_SECRET = '9HX2hrBiiyM4BfBa5YeomjYIvb7H23'
    OSS_ORIGIN = 'oss-cn-beijing'
    BUCKET_NAME = 'micro-drama'
    DEFAULT_PREFIX = "test"
    import time
    
    def create_test_file(size_mb=1):
        """创建测试文件"""
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b'0' * (size_mb * 1024 * 1024))
        temp_file.close()
        return temp_file.name

    def create_test_directory(num_files=3, size_mb=1):
        """创建测试目录"""
        temp_dir = tempfile.mkdtemp()
        for i in range(num_files):
            file_path = os.path.join(temp_dir, f"test_file_{i}.txt")
            with open(file_path, 'wb') as f:
                f.write(b'0' * (size_mb * 1024 * 1024))
        return temp_dir

    def test_single_upload():
        """测试单个文件上传"""
        print("\n测试单个文件上传:")
        # test_file = create_test_file(1)  # 创建1MB的测试文件
        test_file = '/data/Xingjian/test_ma_ma/03.mp4'
        file_size = os.path.getsize(test_file)
        start_time = time.time()
        try:
            oss_key, bucket_name = upload_large_file_to_oss_v2(
                file_path=test_file,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME,
                default_prefix=DEFAULT_PREFIX
            )
            print(f"上传成功，文件key: {oss_key}, bucket_name: {bucket_name}")
        except Exception as e:
            print(f"上传失败: {e}")
        finally:
            #os.unlink(test_file)
            pass
        end_time = time.time()
        print(f"上传时间: {end_time - start_time}秒")
        print(f"上传速度: {file_size / (end_time - start_time)} MB/s")

    def test_single_download():
        """测试单个文件下载"""
        print("\n测试单个文件下载:")
        oss_key = 'test/simple_upload_2025-06-19_16-36/model-00002-of-00004.safetensors'
        bucket_name = 'micro-drama'
        start_time = time.time()
        try:
            file_path = download_large_file_from_oss(
                oss_key=oss_key,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=bucket_name,
                internal=True
            )
            print(f"下载成功，文件路径: {file_path}")
        except Exception as e:
            print(f"下载失败: {e}")
        finally:
            pass
        end_time = time.time()
        print(f"下载时间: {end_time - start_time}秒")

    def test_batch_upload():
        """测试批量文件上传"""
        print("\n测试批量文件上传:")
        test_files = [create_test_file(1) for _ in range(3)]  # 创建3个1MB的测试文件
        try:
            oss_keys, bucket_name = batch_upload_file_to_oss(
                file_paths=test_files,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,  
                bucket_name=BUCKET_NAME,
                default_prefix=DEFAULT_PREFIX
            )
            print(f"批量上传成功，文件key: {oss_keys}, bucket_name: {bucket_name}")
        except Exception as e:
            print(f"批量上传失败: {e}")
        finally:
            for file in test_files:
                os.unlink(file)

    async def test_async_single_upload():
        """测试异步单个文件上传"""
        print("\n测试异步单个文件上传:")
        test_file = create_test_file(1)  # 创建1MB的测试文件
        try:
            oss_key, bucket_name = await aupload_file_to_oss(
                file_path=test_file,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME,
                default_prefix=DEFAULT_PREFIX
            )
            print(f"异步上传成功，文件key: {oss_key}, bucket_name: {bucket_name}")
        except Exception as e:
            print(f"异步上传失败: {e}")
        finally:
            os.unlink(test_file)

    async def test_async_batch_upload():
        """测试异步批量文件上传"""
        print("\n测试异步批量文件上传:")
        test_files = [create_test_file(1) for _ in range(3)]  # 创建3个1MB的测试文件
        try:
            oss_keys, bucket_name = await abatch_upload_file_to_oss(
                file_paths=test_files,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME,
                default_prefix=DEFAULT_PREFIX
            )
            print(f"异步批量上传成功，文件key: {oss_keys}, bucket_name: {bucket_name}")
        except Exception as e:
            print(f"异步批量上传失败: {e}")
        finally:
            for file in test_files:
                os.unlink(file)

    async def test_concurrent_uploads():
        """测试并发上传"""
        print("\n测试并发上传:")
        test_files = [create_test_file(1) for _ in range(3)]  # 创建3个1MB的测试文件
        try:
            # 并发执行多个异步上传任务
            tasks = [
                aupload_file_to_oss(
                    file_path=file,
                    ali_access_key_id=ALI_ACCESS_KEY_ID,
                    ali_access_secret=ALI_ACCESS_SECRET,
                    oss_origin=OSS_ORIGIN,
                    bucket_name=BUCKET_NAME,
                    default_prefix=DEFAULT_PREFIX
                ) for file in test_files
            ]
            results = await asyncio.gather(*tasks)
            print("并发上传成功，结果:")
            for oss_key, bucket_name in results:
                print(f"文件key: {oss_key}, bucket_name: {bucket_name}")
        except Exception as e:
            print(f"并发上传失败: {e}")
        finally:
            for file in test_files:
                os.unlink(file)

    def test_directory_upload():
        """测试目录上传"""
        print("\n测试目录上传:")
        test_dir = create_test_directory(3)  # 创建包含3个1MB文件的测试目录
        try:
            oss_keys, bucket_name = upload_directory_to_oss(
                directory_path=test_dir,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME,
                default_prefix=DEFAULT_PREFIX
            )
            print(f"目录上传成功，文件keys: {oss_keys}, bucket_name: {bucket_name}")
        except Exception as e:
            print(f"目录上传失败: {e}")
        finally:
            shutil.rmtree(test_dir)

    def test_directory_upload_errors():
        """测试目录上传的错误情况"""
        print("\n测试目录上传错误情况:")
        
        # 测试不存在的目录
        try:
            upload_directory_to_oss(
                directory_path="/path/to/nonexistent/dir",
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME
            )
        except FileNotFoundError as e:
            print(f"预期的错误 - 目录不存在: {e}")
        
        # 测试空目录
        empty_dir = tempfile.mkdtemp()
        try:
            upload_directory_to_oss(
                directory_path=empty_dir,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME
            )
        except EmptyDirectoryError as e:
            print(f"预期的错误 - 空目录: {e}")
        finally:
            shutil.rmtree(empty_dir)
        
        # 测试文件路径（而不是目录）
        test_file = create_test_file(1)
        try:
            upload_directory_to_oss(
                directory_path=test_file,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME
            )
        except NotADirectoryError as e:
            print(f"预期的错误 - 不是目录: {e}")
        finally:
            os.unlink(test_file)

    async def test_async_directory_upload():
        """测试异步目录上传"""
        print("\n测试异步目录上传:")
        test_dir = create_test_directory(3)  # 创建包含3个1MB文件的测试目录
        try:
            oss_keys, bucket_name = await aupload_directory_to_oss(
                directory_path=test_dir,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME,
                default_prefix=DEFAULT_PREFIX
            )
            print(f"异步目录上传成功，文件keys: {oss_keys}, bucket_name: {bucket_name}")
        except Exception as e:
            print(f"异步目录上传失败: {e}")
        finally:
            shutil.rmtree(test_dir)

    async def test_async_directory_upload_errors():
        """测试异步目录上传的错误情况"""
        print("\n测试异步目录上传错误情况:")
        
        # 测试不存在的目录
        try:
            await aupload_directory_to_oss(
                directory_path="/path/to/nonexistent/dir",
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME
            )
        except FileNotFoundError as e:
            print(f"预期的错误 - 目录不存在: {e}")
        
        # 测试空目录
        empty_dir = tempfile.mkdtemp()
        try:
            await aupload_directory_to_oss(
                directory_path=empty_dir,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME
            )
        except EmptyDirectoryError as e:
            print(f"预期的错误 - 空目录: {e}")
        finally:
            shutil.rmtree(empty_dir)
        
        # 测试文件路径（而不是目录）
        test_file = create_test_file(1)
        try:
            await aupload_directory_to_oss(
                directory_path=test_file,
                ali_access_key_id=ALI_ACCESS_KEY_ID,
                ali_access_secret=ALI_ACCESS_SECRET,
                oss_origin=OSS_ORIGIN,
                bucket_name=BUCKET_NAME
            )
        except NotADirectoryError as e:
            print(f"预期的错误 - 不是目录: {e}")
        finally:
            os.unlink(test_file)

    async def run_async_tests():
        """运行所有异步测试"""
        await test_async_single_upload()
        await test_async_batch_upload()
        await test_concurrent_uploads()
        await test_async_directory_upload()
        await test_async_directory_upload_errors()
    
    # 运行同步测试
    print("=== 运行同步测试 ===")
    test_single_upload()
    # test_single_download()
    # test_batch_upload()
    # test_directory_upload()
    # test_directory_upload_errors()
    
    # # 运行异步测试
    # print("\n=== 运行异步测试 ===")
    # asyncio.run(run_async_tests())