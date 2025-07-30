import os
import ast
from datetime import datetime
from mjkit.init_generator.base import BaseInitGenerator
import logging


class InitGenerator(BaseInitGenerator):
    """
    InitGenerator는 지정한 루트 디렉토리부터 시작해 모든 하위 패키지를 순회하며,
    각 패키지 내의 파이썬 모듈에서 공개 클래스 및 함수 이름을 추출하여
    해당 디렉토리의 __init__.py 파일을 자동 생성하는 클래스입니다.

    생성된 __init__.py는 자동 임포트 및 __all__ 리스트를 포함하여
    패키지 내부 심볼을 명시적으로 노출합니다.

    로깅 기능을 포함하여 각 단계별 작업 진행상황과 결과를 기록합니다.
    """

    def extract_symbols_from_file(self, filepath: str):
        """
        주어진 파이썬 파일에서 공개 클래스 및 함수 이름을 추출합니다.

        Args:
            filepath (str): 분석할 파이썬 파일 경로

        Returns:
            list[str]: 클래스명 및 함수명 리스트 (private 멤버는 제외)

        Example:
            >>> symbols = generator.extract_symbols_from_file("mjkit/mixin/some_mixin.py")
            >>> print(symbols)
            ['LoggingMixin', 'AttributePrinterMixin']
        """
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        symbols = []
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                if not node.name.startswith("_"):
                    symbols.append(node.name)
        self.logger.info(f"Extracted symbols from {filepath}: {symbols}")
        return symbols

    def _collect_symbols_in_package(self, package_dir: str):
        """
        패키지 디렉토리 내 모든 파이썬 파일을 스캔하여 모듈별 심볼(클래스/함수)를 수집합니다.

        Args:
            package_dir (str): 패키지 디렉토리 경로

        Returns:
            tuple: (imports: list[str], exports: list[str])
                - imports: from .module import Symbol 형태 리스트
                - exports: __all__에 포함할 심볼 이름 리스트
        """
        imports = []
        exports = []
        self.logger.debug(f"Scanning package dir for symbols: {package_dir}")

        for fname in os.listdir(package_dir):
            if not (fname.endswith(".py") and fname != "__init__.py"):
                continue
            module = fname[:-3]
            full_path = os.path.join(package_dir, fname)
            symbols = self.extract_symbols_from_file(full_path)
            for symbol in symbols:
                imports.append(f"from .{module} import {symbol}")
                exports.append(f'"{symbol}"')

        self.logger.debug(f"Collected imports:\n{imports}")
        self.logger.debug(f"Collected exports:\n{exports}")
        return imports, exports

    def _generate_header(self):
        """
        자동 생성 파일 헤더 생성

        Returns:
            str: 파일 상단 주석 문자열
        """
        return (
            f'"""\n'
            f'자동 생성 파일입니다. 직접 수정하지 마세요.\n'
            f'생성일자: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
            f'"""\n\n'
        )

    def _write_init_file(self, init_path: str, imports: list[str], exports: list[str]):
        """
        __init__.py 파일에 내용을 작성합니다.

        Args:
            init_path (str): __init__.py 파일 경로
            imports (list[str]): from 문 리스트
            exports (list[str]): __all__ 리스트에 포함할 심볼 문자열 리스트
        """
        content = self._generate_header()
        content += "\n".join(imports)
        content += "\n\n__all__ = [\n    " + ",\n    ".join(exports) + "\n]\n"

        with open(init_path, "w", encoding="utf-8") as f:
            f.write(content)

        self.logger.info(f"✅ Generated __init__.py at {init_path} with {len(exports)} exports")

    def process_package(self, package_dir: str):
        """
        단일 패키지 디렉토리에 대해 __init__.py 파일을 생성합니다.

        Args:
            package_dir (str): __init__.py 파일을 생성할 패키지 디렉토리 경로

        Example:
            >>> generator.process_package("/path/to/mjkit/mixin")
            # 로그: 생성 성공 메시지 출력
        """
        self.logger.info(f"Processing package: {package_dir}")
        imports, exports = self._collect_symbols_in_package(package_dir)
        init_path = os.path.join(package_dir, "__init__.py")

        if imports and exports:
            self._write_init_file(init_path, imports, exports)
        else:
            self.logger.warning(f"⚠️  No exports found in: {package_dir}")

    def walk_packages(self):
        """
        루트 디렉토리부터 시작해 하위 모든 패키지를 순회하며
        process_package를 호출하여 __init__.py 파일을 생성합니다.

        로그에 현재 탐색중인 디렉토리와 처리 결과를 기록합니다.

        Example:
            >>> generator.walk_packages()
            # 각 패키지별 처리 로그 출력
        """
        self.logger.info(f"Starting package walk at root: {self.root_dir}")
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            if "__pycache__" in dirpath:
                continue
            py_files = [f for f in filenames if f.endswith(".py") and f != "__init__.py"]
            if py_files:
                self.logger.debug(f"Found python files in {dirpath}: {py_files}")
                self.process_package(dirpath)
        self.logger.info("Completed walking packages.")


if __name__ == "__main__":
    from mjkit.utiles.get_folder_path import get_root_dir

    package_path = os.path.join(get_root_dir(), "mjkit")
    generator = InitGenerator(root_dir=package_path, log_level=logging.DEBUG)
    generator.run()
