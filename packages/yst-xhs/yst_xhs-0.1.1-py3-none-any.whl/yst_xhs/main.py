import os
import argparse
from loguru import logger
from apis.pc_apis import XHS_Apis
from xhs_utils.common_utils import init
from xhs_utils.data_util import handle_note_info, download_note, save_to_xlsx

def spider_note(api, note_url, cookies_str, proxies=None):
    """
    爬取单个笔记
    """
    success, msg, note_info = api.get_note_info(note_url, cookies_str, proxies)
    if success:
        note_data = handle_note_info(note_info['data'])
        logger.success(f"成功获取笔记: {note_data['note_id']}")
        return note_data
    else:
        logger.error(f"获取笔记失败: {msg}")
        return None

def spider_some_note(api, notes, cookies_str, base_path, save_choice, excel_name='爬取结果', proxies=None):
    """
    爬取多个笔记
    """
    if (save_choice == 'all' or save_choice == 'excel') and excel_name == '':
        excel_name = '爬取结果'
        
    note_list = []
    for note_url in notes:
        success, msg, note_info = api.get_note_info(note_url, cookies_str, proxies)
        if success:
            note_data = handle_note_info(note_info['data'])
            note_list.append(note_data)
            logger.success(f"成功获取笔记: {note_data['note_id']}")
        else:
            logger.error(f"获取笔记失败: {msg}")
    
    logger.info(f"共获取 {len(note_list)} 个笔记")
    
    # 保存数据
    if save_choice == 'all' or save_choice == 'media':
        for note_info in note_list:
            download_note(note_info, base_path['media'])
            
    if save_choice == 'all' or save_choice == 'excel':
        file_path = os.path.abspath(os.path.join(base_path['excel'], f'{excel_name}.xlsx'))
        save_to_xlsx(note_list, file_path)
        logger.success(f"数据已保存至: {file_path}")

def spider_user_notes(api, user_url, cookies_str, base_path, save_choice, excel_name='用户笔记', proxies=None):
    """
    爬取用户所有笔记
    """
    success, msg, note_list = api.get_user_all_notes(user_url, cookies_str, proxies)
    if success:
        logger.success(f"成功获取用户笔记，共 {len(note_list)} 篇")
        
        processed_notes = []
        for note in note_list:
            processed_note = handle_note_info(note)
            processed_notes.append(processed_note)
        
        # 保存数据
        if save_choice == 'all' or save_choice == 'media':
            for note_info in processed_notes:
                download_note(note_info, base_path['media'])
                
        if save_choice == 'all' or save_choice == 'excel':
            file_path = os.path.abspath(os.path.join(base_path['excel'], f'{excel_name}.xlsx'))
            save_to_xlsx(processed_notes, file_path)
            logger.success(f"数据已保存至: {file_path}")
    else:
        logger.error(f"获取用户笔记失败: {msg}")

def search_and_spider_notes(api, query, num, cookies_str, base_path, save_choice, excel_name='搜索结果', proxies=None):
    """
    搜索并爬取笔记
    """
    success, msg, notes = api.search_some_note(query, num, cookies_str, proxies=proxies)
    if success:
        logger.success(f"搜索成功，共获取 {len(notes)} 篇笔记")
        
        processed_notes = []
        for note in notes:
            processed_note = handle_note_info(note)
            processed_notes.append(processed_note)
        
        # 保存数据
        if save_choice == 'all' or save_choice == 'media':
            for note_info in processed_notes:
                download_note(note_info, base_path['media'])
                
        if save_choice == 'all' or save_choice == 'excel':
            file_path = os.path.abspath(os.path.join(base_path['excel'], f'{excel_name}.xlsx'))
            save_to_xlsx(processed_notes, file_path)
            logger.success(f"数据已保存至: {file_path}")
    else:
        logger.error(f"搜索失败: {msg}")

def main():
    parser = argparse.ArgumentParser(description='小红书爬虫工具')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 笔记爬取子命令
    note_parser = subparsers.add_parser('note', help='爬取单个笔记')
    note_parser.add_argument('url', help='笔记URL')
    note_parser.add_argument('--save', choices=['all', 'media', 'excel', 'none'], default='all', 
                            help='保存选项: all=媒体和Excel, media=仅媒体, excel=仅Excel, none=不保存')
    
    # 多笔记爬取子命令
    notes_parser = subparsers.add_parser('notes', help='爬取多个笔记')
    notes_parser.add_argument('urls', nargs='+', help='笔记URL列表')
    notes_parser.add_argument('--save', choices=['all', 'media', 'excel', 'none'], default='all',
                             help='保存选项: all=媒体和Excel, media=仅媒体, excel=仅Excel, none=不保存')
    notes_parser.add_argument('--excel-name', default='爬取结果', help='Excel文件名')
    
    # 用户笔记爬取子命令
    user_parser = subparsers.add_parser('user', help='爬取用户所有笔记')
    user_parser.add_argument('url', help='用户页面URL')
    user_parser.add_argument('--save', choices=['all', 'media', 'excel', 'none'], default='all',
                            help='保存选项: all=媒体和Excel, media=仅媒体, excel=仅Excel, none=不保存')
    user_parser.add_argument('--excel-name', default='用户笔记', help='Excel文件名')
    
    # 搜索笔记子命令
    search_parser = subparsers.add_parser('search', help='搜索并爬取笔记')
    search_parser.add_argument('query', help='搜索关键词')
    search_parser.add_argument('--num', type=int, default=10, help='爬取数量')
    search_parser.add_argument('--save', choices=['all', 'media', 'excel', 'none'], default='all',
                              help='保存选项: all=媒体和Excel, media=仅媒体, excel=仅Excel, none=不保存')
    search_parser.add_argument('--excel-name', default='搜索结果', help='Excel文件名')
    
    args = parser.parse_args()
    
    # 初始化
    cookies_str, base_path = init()
    api = XHS_Apis()
    
    if args.command == 'note':
        note_data = spider_note(api, args.url, cookies_str)
        if note_data and args.save != 'none':
            if args.save == 'all' or args.save == 'media':
                download_note(note_data, base_path['media'])
            if args.save == 'all' or args.save == 'excel':
                file_path = os.path.abspath(os.path.join(base_path['excel'], '单笔记爬取.xlsx'))
                save_to_xlsx([note_data], file_path)
                logger.success(f"数据已保存至: {file_path}")
    
    elif args.command == 'notes':
        spider_some_note(api, args.urls, cookies_str, base_path, args.save, args.excel_name)
    
    elif args.command == 'user':
        spider_user_notes(api, args.url, cookies_str, base_path, args.save, args.excel_name)
    
    elif args.command == 'search':
        search_and_spider_notes(api, args.query, args.num, cookies_str, base_path, args.save, args.excel_name)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
