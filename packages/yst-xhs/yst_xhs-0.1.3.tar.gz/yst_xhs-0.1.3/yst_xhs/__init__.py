# 导出主要类和函数
from .apis.pc_apis import XHS_Apis
from .xhs_utils.common_utils import init
from .xhs_utils.data_util import handle_note_info, download_note, save_to_xlsx

__version__ = '0.1.3'  # 保持与setup.py一致