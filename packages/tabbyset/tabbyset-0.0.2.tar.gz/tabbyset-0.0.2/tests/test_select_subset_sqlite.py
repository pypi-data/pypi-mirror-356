import unittest

from tabbyset.entities import TestCase
from tabbyset.file_formats import Csv1Reader
from tabbyset.testing import TestCaseAssertions
from tabbyset.utils import Folder
from tabbyset.scripts.select_subset_sqlite import run_select_subset_sqlite, IteratorType
from tabbyset.scripts.select_subset_sqlite.s0_setup_sqlite import setup_sqlite
from tabbyset.scripts.select_subset_sqlite.constants import DB_NAME


class TestSelectSubsetSQLite(TestCaseAssertions):
    folder_cases: Folder
    folder_traces: Folder
    output_folder_counts_iter: Folder
    output_folder_weights_iter: Folder
    coverage_script = 'test1'

    @classmethod
    def setUpClass(cls) -> None:
        # TODO: Add open source test data
        cls.folder_cases = Folder.mount_from_current_module('../../ex_subset_selector/tests/csv')
        cls.folder_traces = Folder.mount_from_current_module('../../ex_subset_selector/tests/Test')
        outputs = Folder.mount_from_current_module('./assets/select_subset_sqlite/output')
        cls.output_folder_counts_iter = outputs.mount_subfolder('counts_iter')
        cls.output_folder_weights_iter = outputs.mount_subfolder('weights_iter')
        for folder_output, iterator_type in cls.get_zipped_iterators():
            run_select_subset_sqlite(
                venue='TEST',
                folder_cases=cls.folder_cases,
                folder_traces=cls.folder_traces,
                folder_output=folder_output,
                keep_db=True,
                with_code_coverage=True,
                coverage_script=cls.coverage_script,
                iterator_type=iterator_type
            )

    def test_all_traces_covered(self):
        for folder_output, iterator_type in self.get_zipped_iterators():
            with self.subTest(iterator_type=iterator_type.name):
                db = setup_sqlite(str(folder_output.get_file_path(DB_NAME)))
                for subset in ['maxanno', 'minanno']:
                    with self.subTest(subset=subset):
                        uncovered_traces = db.conn.execute(f"""
                                WITH covered_traces AS (
                                    SELECT DISTINCT tctt.trace_hash
                                    FROM {subset.capitalize()}Selections ms
                                    JOIN TestCasesToTraces tctt ON tctt.test_case_hash = ms.test_case_hash
                                )
                                SELECT DISTINCT t.Summary, t.File, t.Line
                                FROM Traces t
                                LEFT JOIN covered_traces ct ON ct.trace_hash = t.hash
                                WHERE ct.trace_hash IS NULL
                            """).fetchall()
                        self.assertEqual(0, len(uncovered_traces), f"Uncovered traces: {uncovered_traces}")
                db.conn.close()

    def test_all_chosen_cases_are_saved(self):
        self.skipTest('Proprietary test data is not replaced')
        for folder_output, iterator_type in self.get_zipped_iterators():
            with self.subTest(iterator_type=iterator_type.name):
                db = setup_sqlite(str(folder_output.get_file_path(DB_NAME)))
                for subset in ['maxanno', 'minanno']:
                    with self.subTest(subset=subset):
                        chosen_cases = set()
                        rows = db.conn.execute(f"""
                                    SELECT tc.TestScript, tc.TestCase 
                                    FROM TestCases tc 
                                    JOIN {subset.capitalize()}Selections ms ON tc.hash  = ms.test_case_hash 
                                    ORDER BY tc.TestScript 
                                """)
                        for row in rows:
                            chosen_cases.add(row[1])
                        saved_cases = set()
                        subset_reader = Csv1Reader(folder_output.get_file_path(f'{self.coverage_script}.{subset}.csv'))
                        for test_case in subset_reader:
                            saved_cases.add(test_case.name)
                        subset_reader.close()
                        self.assertEqual(chosen_cases, saved_cases)
                db.conn.close()

    def test_chosen_test_cases_healthy(self):
        self.skipTest('Proprietary test data is not replaced')
        all_test_cases: list[TestCase] = []
        for file in self.folder_cases.glob('*.csv'):
            csv1_reader = Csv1Reader(file)
            all_test_cases.extend(csv1_reader)
            csv1_reader.close()
        for folder_output, iterator_type in self.get_zipped_iterators():
            with self.subTest(iterator_type=iterator_type.name):
                for subset in ['maxanno', 'minanno']:
                    with self.subTest(subset=subset):
                        subset_reader = Csv1Reader(folder_output.get_file_path(f'{self.coverage_script}.{subset}.csv'))
                        for test_case in subset_reader:
                            with self.subTest(test_case=test_case.name):
                                global_tc = next(filter(lambda tc: tc.name == test_case.name, all_test_cases))
                                self.assertTestCasesEqual(global_tc, test_case)
                        subset_reader.close()

    @classmethod
    def get_zipped_iterators(cls) -> list[tuple[Folder, IteratorType]]:
        return zip(
            [cls.output_folder_counts_iter, cls.output_folder_weights_iter],
            [IteratorType.COUNT_ITERATOR, IteratorType.WEIGHTS_ITERATOR]
        )


if __name__ == '__main__':
    unittest.main()
