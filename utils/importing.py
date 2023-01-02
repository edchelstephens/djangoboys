"""import_export module utils"""

from import_export.results import Result
from tablib import Dataset

from utils.debug import DebuggerMixin
from utils.exceptions import EmptyDataSetImport


class ImportExportDebuggerMixin(DebuggerMixin):
    """Import export debugger mixin."""

    def pprint_dataset(self, dataset: Dataset) -> None:
        """Print dataset for debugging."""
        print()
        self.pprint_label("Dataset")
        print(dataset)
        print()

    def pprint_results(self, import_result: Result) -> None:
        """Print import results."""
        import_results_data = vars(import_result)
        failed_dataset = import_result.failed_dataset
        base_errors = import_result.base_errors
        invalid_rows = import_result.invalid_rows
        invalid_rows_data = [vars(row) for row in invalid_rows]
        rows = import_result.rows

        has_error = import_result.has_errors()
        error_rows = import_result.row_errors()

        row_results = []
        for row in rows:
            result_data = vars(row)
            row_errors = result_data["errors"]
            row_errors_result = [vars(error) for error in row_errors]
            row_result = {
                "result_data": result_data,
                "row_errors_result": row_errors_result,
            }
            row_results.append(row_result)

        total_rows = import_result.total_rows
        totals = import_result.totals

        self.pprint_data(import_results_data, "import_results_data")

        self.pprint_data(base_errors, "base_errors")
        print(base_errors)

        self.pprint_label("failed_dataset")
        print(failed_dataset)
        self.pprint_data(vars(failed_dataset), "Failed Dataset vars")

        self.pprint_data(invalid_rows_data, "invalid_rows_data")

        self.pprint_data(row_results, "row_results")

        self.pprint_data(total_rows, "total_rows")

        self.pprint_data(totals, "totals")

        self.pprint_data(has_error, "has error")
        self.pprint_data(error_rows, "error_rows")


class ModelResourceImportMixin(ImportExportDebuggerMixin):
    """Mixin class for importing.

    Override class variables below to implement different import actions.


    Import results are stored in Result.totals as an ordered dict with keys mapping to counts.

        Available keys:
            `update`
            `new`
            `delete`
            `skip`
            `error`
            `invalid`

        Available keys are also used as actions.

    https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.resources.Resource.import_data

    `Resource` class attribute must be overriden with actual ModelResource class.
    """

    mode = "new"
    success_action = "added"
    file_input_name = "importFile"
    Resource = None
    dry_run = False
    raise_errors = True

    def prepare_dataset_for_import(self, dataset: Dataset) -> None:
        """Get import action dataset."""
        raise NotImplementedError("Must implement prepare_dataset_for_import()")

    def load_dataset(self, request) -> Dataset:
        """Load and return dataset."""
        try:

            import_file = request.FILES[self.file_input_name]
            extension = import_file.name.split(".")[-1].lower()
            dataset = Dataset()

            if extension == "csv":
                dataset.load(import_file.read().decode("utf-8"), format=extension)
            else:
                dataset.load(import_file.read(), format=extension)

            if self.is_dataset_empty(dataset):
                raise EmptyDataSetImport()

            return dataset

        except Exception as exc:
            raise exc

    def is_dataset_empty(self, dataset: Dataset) -> bool:
        """Check if dataset does not contain rows."""
        return dataset.height == 0

    def get_cleaned_dataset(
        self, error_rows_numbers: list, dataset: Dataset
    ) -> Dataset:
        """Get new cleaned dataset excluding error rows."""

        cleaned_dataset = Dataset()
        cleaned_dataset.headers = dataset.headers

        for index, data in enumerate(dataset.dict):
            error_row = index + 1 in error_rows_numbers
            if error_row:
                continue
            clean_data_values = tuple(data.values())
            cleaned_dataset.append(clean_data_values)

        return cleaned_dataset

    def get_total_rows_count(self, dataset: Dataset) -> int:
        """Get the total rows count."""
        return dataset.height

    def get_import_results(
        self, resource: Resource, dataset: Dataset, **kwargs
    ) -> Result:
        """Get import results."""
        return resource.import_data(
            dataset,
            raise_errors=self.raise_errors,
            collect_failed_rows=True,
            dry_run=self.dry_run,
            **kwargs,
        )

    def get_results_count(self, import_result: Result, key: str) -> int:
        """Get import results count.

        Available keys:
            `new`
            `update`
            `delete`
            `skip`
            `error`
            `invalid`
        """
        totals_dict = dict(import_result.totals)
        count = totals_dict[key]
        return count

    def get_new_results_count(self, import_result: Result) -> int:
        """Return new or added count."""
        return self.get_results_count(import_result, key="new")

    def get_update_results_count(self, import_result: Result) -> int:
        """Return updated count."""
        return self.get_results_count(import_result, key="update")

    def get_skip_results_count(self, import_result: Result) -> int:
        """Return skipped count."""
        return self.get_results_count(import_result, key="skip")

    def get_error_results_count(self, import_result: Result) -> int:
        """Return error count."""
        return self.get_results_count(import_result, key="error")

    def get_invalid_results_count(self, import_result: Result) -> int:
        """Return invalid count."""
        return self.get_results_count(import_result, key="invalid")

    def get_import_success_message(self, import_result: Result, noun: str) -> str:
        """Get success message based on mode and success results count."""

        count = self.get_success_results_count(import_result)
        noun = self.get_results_noun(count, noun=noun)

        return f"{count} {noun} successfully {self.success_action}."

    def get_success_results_count(self, import_result: Result) -> int:
        """Get imports success count."""
        return self.get_results_count(import_result, key=self.mode)

    def get_error_rows(self, import_result: Result) -> tuple[list, list[dict]]:
        """Get error rows data.

        Returns a tuple:
            `rows_numbers`
            `error_rows` list with dict items data
        """

        error_rows = []
        rows_numbers = []
        row_errors = import_result.row_errors()

        for row_number, error_list in row_errors:
            error_data = {
                "row_number": row_number,
                "row_errors": [self.get_error_data(error) for error in error_list],
            }

            error_rows.append(error_data)
            rows_numbers.append(row_number)

        return rows_numbers, error_rows

    def get_results_noun(self, count: int, noun: str) -> str:
        """Get singular or plural noun based on count for success message."""
        return noun if count == 1 else noun + "s"

    def get_results_noun_capitalized(self, count: int, noun: str) -> str:
        """Get results noun capitalized."""
        noun = self.get_results_noun(count, noun)
        return noun.capitalize()
