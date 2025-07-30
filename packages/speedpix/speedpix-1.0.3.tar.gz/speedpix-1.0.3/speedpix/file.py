import io
import mimetypes
import os
import pathlib
from typing import BinaryIO, Literal, Optional, TypedDict, Union

from typing_extensions import NotRequired, Unpack

from speedpix.resource import Namespace, Resource

FileEncodingStrategy = Literal["base64", "url"]


class File(Resource):
    """
    SpeedPix 文件上传后的文件对象
    """

    path: str
    """文件路径"""

    expire_time: Optional[str]
    """过期时间"""

    upload_url: str
    """上传 URL"""

    access_url: str
    """访问 URL，用于后续推理"""

    object_key: str
    """对象键"""

    # 本地文件信息
    name: Optional[str] = None
    """文件名"""

    content_type: Optional[str] = None
    """内容类型"""

    size: Optional[int] = None
    """文件大小（字节）"""

    @property
    def url(self) -> str:
        """获取文件的访问 URL"""
        return self.access_url

    def __str__(self) -> str:
        """字符串表示返回访问 URL"""
        return self.access_url


class Files(Namespace):
    """文件管理命名空间"""

    class CreateFileParams(TypedDict):
        """创建文件的参数"""

        filename: NotRequired[str]
        """文件名"""

        content_type: NotRequired[str]
        """内容类型"""

    def create(
        self,
        file: Union[str, pathlib.Path, BinaryIO, io.IOBase],
        **params: Unpack["Files.CreateFileParams"],
    ) -> File:
        """
        上传文件到 SpeedPix，可以用作模型输入

        Args:
            file: 文件路径或文件对象
            **params: 可选参数

        Returns:
            File: 上传后的文件对象
        """
        if isinstance(file, (str, pathlib.Path)):
            file_path = pathlib.Path(file)
            params["filename"] = params.get("filename", file_path.name)
            with open(file, "rb") as f:
                return self.create(f, **params)
        elif not isinstance(file, (io.IOBase, BinaryIO)):
            raise ValueError("不支持的文件类型。必须是文件路径或文件对象。")

        # 准备文件信息
        filename = params.get(
            "filename", os.path.basename(getattr(file, "name", "file"))
        )
        content_type = (
            params.get("content_type")
            or mimetypes.guess_type(filename)[0]
            or "application/octet-stream"
        )

        # 获取文件大小
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(0)  # 回到文件开头

        # 1. 调用 /scc/sp_create_temp_file_upload_sign 获取上传签名
        from speedpix.schema import TempFileCreateResponse

        sign_response = self._client._request(
            "POST",
            "/scc/sp_create_temp_file_upload_sign",
            json={
                "contentType": content_type,
                "originalFilename": filename,
            },
        )

        # 解析响应数据
        try:
            response_data = TempFileCreateResponse.from_dict(sign_response.json())
        except (ValueError, KeyError, AttributeError) as e:
            raise ValueError(f"解析上传签名响应失败: {e}") from e

        # 检查响应状态
        if response_data.err_code or not response_data.data:
            # 构建更易读的错误消息
            error_parts = []
            if response_data.err_message:
                error_parts.append(f"错误: {response_data.err_message}")
            if response_data.sub_err_message:
                error_parts.append(f"详细: {response_data.sub_err_message}")
            if response_data.err_code:
                error_parts.append(f"错误码: {response_data.err_code}")
            if response_data.sub_err_code:
                error_parts.append(f"子错误码: {response_data.sub_err_code}")

            error_message = (
                " | ".join(error_parts) if error_parts else "获取上传签名失败"
            )
            raise ValueError(f"获取上传签名失败: {error_message}")

        sign_data = response_data.data
        upload_url = sign_data.upload_url

        if not upload_url:
            raise ValueError("上传签名响应中缺少上传 URL")

        # 2. 使用 PUT 方法上传文件到指定 URL
        file.seek(0)  # 确保从文件开头读取
        upload_response = self._client._client.put(
            upload_url,
            content=file.read(),
            headers={
                "Content-Type": content_type,
                "Content-Length": str(file_size),
            },
        )

        upload_response.raise_for_status()

        # 3. 返回文件对象
        file_obj = File(
            path=sign_data.path,
            expire_time=str(sign_data.expire_time) if sign_data.expire_time else None,
            upload_url=upload_url,
            access_url=sign_data.access_url or "",
            object_key=sign_data.object_key,
            name=filename,
            content_type=content_type,
            size=file_size,
        )

        return file_obj

    async def async_create(
        self,
        file: Union[str, pathlib.Path, BinaryIO, io.IOBase],
        **params: Unpack["Files.CreateFileParams"],
    ) -> File:
        """
        异步上传文件到 SpeedPix

        Args:
            file: 文件路径或文件对象
            **params: 可选参数

        Returns:
            File: 上传后的文件对象
        """
        if isinstance(file, (str, pathlib.Path)):
            file_path = pathlib.Path(file)
            params["filename"] = params.get("filename", file_path.name)
            with open(file_path, "rb") as f:
                return await self.async_create(f, **params)
        elif not isinstance(file, (io.IOBase, BinaryIO)):
            raise ValueError("不支持的文件类型。必须是文件路径或文件对象。")

        # 准备文件信息
        filename = params.get(
            "filename", os.path.basename(getattr(file, "name", "file"))
        )
        content_type = (
            params.get("content_type")
            or mimetypes.guess_type(filename)[0]
            or "application/octet-stream"
        )

        # 获取文件大小
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(0)  # 回到文件开头

        # 1. 调用 /scc/sp_create_temp_file_upload_sign 获取上传签名
        from speedpix.schema import TempFileCreateResponse

        sign_response = await self._client._async_request(
            "POST",
            "/scc/sp_create_temp_file_upload_sign",
            json={
                "contentType": content_type,
                "originalFilename": filename,
            },
        )

        # 解析响应数据
        try:
            response_data = TempFileCreateResponse.from_dict(sign_response.json())
        except (ValueError, KeyError, AttributeError) as e:
            raise ValueError(f"解析上传签名响应失败: {e}") from e

        # 检查响应状态
        if response_data.err_code or not response_data.data:
            # 构建更易读的错误消息
            error_parts = []
            if response_data.err_message:
                error_parts.append(f"错误: {response_data.err_message}")
            if response_data.sub_err_message:
                error_parts.append(f"详细: {response_data.sub_err_message}")
            if response_data.err_code:
                error_parts.append(f"错误码: {response_data.err_code}")
            if response_data.sub_err_code:
                error_parts.append(f"子错误码: {response_data.sub_err_code}")

            error_message = (
                " | ".join(error_parts) if error_parts else "获取上传签名失败"
            )
            raise ValueError(f"获取上传签名失败: {error_message}")

        sign_data = response_data.data
        upload_url = sign_data.upload_url

        if not upload_url:
            raise ValueError("上传签名响应中缺少上传 URL")

        # 2. 使用 PUT 方法上传文件到指定 URL
        file.seek(0)  # 确保从文件开头读取
        upload_response = await self._client._async_client.put(
            upload_url,
            content=file.read(),
            headers={
                "Content-Type": content_type,
                "Content-Length": str(file_size),
            },
        )

        upload_response.raise_for_status()

        # 3. 返回文件对象
        file_obj = File(
            path=sign_data.path,
            expire_time=str(sign_data.expire_time) if sign_data.expire_time else None,
            upload_url=upload_url,
            access_url=sign_data.access_url or "",
            object_key=sign_data.object_key,
            name=filename,
            content_type=content_type,
            size=file_size,
        )

        return file_obj
