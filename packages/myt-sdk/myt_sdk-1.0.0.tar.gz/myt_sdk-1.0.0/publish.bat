@echo off
REM PyPI发布快速脚本
REM 使用方法：
REM   publish.bat test    - 发布到TestPyPI
REM   publish.bat prod    - 发布到正式PyPI
REM   publish.bat clean   - 只清理构建文件

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%"

echo ========================================
echo MYT SDK PyPI 发布脚本
echo ========================================

if "%1"=="" (
    echo 用法: publish.bat [test|prod|clean]
    echo   test  - 发布到TestPyPI
    echo   prod  - 发布到正式PyPI  
    echo   clean - 清理构建文件
    goto :end
)

if "%1"=="clean" (
    echo 清理构建文件...
    if exist "dist" rmdir /s /q "dist"
    if exist "build" rmdir /s /q "build"
    for /d %%i in ("*.egg-info") do if exist "%%i" rmdir /s /q "%%i"
    echo 清理完成！
    goto :end
)

REM 检查Python和pip
echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请确保Python已安装并添加到PATH
    goto :error
)

REM 检查必要的包
echo 检查必要的包...
python -c "import setuptools, wheel, twine" >nul 2>&1
if errorlevel 1 (
    echo 安装必要的包...
    pip install setuptools wheel twine
    if errorlevel 1 (
        echo 错误: 无法安装必要的包
        goto :error
    )
)

REM 清理旧的构建文件
echo 清理旧的构建文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
for /d %%i in ("*.egg-info") do if exist "%%i" rmdir /s /q "%%i"

REM 运行测试（可选）
echo 运行测试...
python -m pytest tests/ -v
if errorlevel 1 (
    echo 警告: 测试失败，是否继续？
    set /p "continue=继续发布？(y/N): "
    if /i not "!continue!"=="y" goto :end
)

REM 构建包
echo 构建包...
python setup.py sdist bdist_wheel
if errorlevel 1 (
    echo 错误: 构建失败
    goto :error
)

REM 检查包
echo 检查包完整性...
twine check dist/*
if errorlevel 1 (
    echo 错误: 包检查失败
    goto :error
)

REM 上传包
if "%1"=="test" (
    echo 上传到TestPyPI...
    twine upload --repository testpypi dist/*
    if errorlevel 1 (
        echo 错误: 上传到TestPyPI失败
        goto :error
    )
    echo.
    echo 成功上传到TestPyPI！
    echo 测试安装命令:
    echo pip install --index-url https://test.pypi.org/simple/ myt-sdk
) else if "%1"=="prod" (
    echo 警告: 即将上传到正式PyPI，这个操作不可撤销！
    set /p "confirm=确认上传？(yes/no): "
    if not "!confirm!"=="yes" (
        echo 上传已取消
        goto :end
    )
    
    echo 上传到正式PyPI...
    twine upload dist/*
    if errorlevel 1 (
        echo 错误: 上传到PyPI失败
        goto :error
    )
    echo.
    echo 成功上传到PyPI！
    echo 安装命令:
    echo pip install myt-sdk
) else (
    echo 错误: 未知的参数 "%1"
    echo 用法: publish.bat [test|prod|clean]
    goto :error
)

echo.
echo 发布完成！
goto :end

:error
echo.
echo 发布失败！
exit /b 1

:end
echo.
pause