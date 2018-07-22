from android_studio_translator.web.model.translator.segment import Segment
from android_studio_translator.web.model.translator.test.test_sql import TestSql
from android_studio_translator.web.util.data_importer import DataImporter
from android_studio_translator.web.util.time_logger import TimeLogger


class TestSegment(TestSql):
    test_object = Segment()

    def test_insert_sql(self):
        """可以包含更新时间"""
        print(self.test_object.generate_insert_formatter_sql())

    def test_insert(self, execute=True):
        self.test_object.source = 'it\'s a test'
        super().test_insert(execute)

    def test_import_from_tmx_and_save(self):
        tmx_file = r'D:\workspace\TranslatorX\JetBrains\omegat\project_save.tmx'
        time_logger = TimeLogger('解析 tmx ')
        segment_list = DataImporter().load_segments_from_tmx_file(tmx_file)
        print(f'共 {len(segment_list)} 条')
        time_logger.stop()

        # 不再需要，已经很快了
        # time_logger = TimeLogger('保存进 json ')
        # DataImporter.save_segment_list_to_json_file(segment_list, self.segment_list_file)
        # time_logger.stop()

        time_logger = TimeLogger('保存数据')
        DataImporter.save_segments(segment_list)
        time_logger.stop()
