# Changelog

## 1.2.7

- Don't fail if a dimension value label does not exist (e.g. `BDF/ECOFI/FSI.FR.FSERA_PT._Z.Q` where `_Z` has no label)

## 1.2.6

- Stop quoting URLs twice. Solves a bug with the series IDs like `OECD/DSD_KEI@DF_KEI/BRA.M.CP.GR._Z._Z.GY`.
- Revert from `httpx` to `requests` because the latter does not re-quotes the URL it is given.

## 1.2.5

- Follow redirects for dataset "latest" releases.

## 1.2.4

- Add default timeout of 1 minute.
- Implement a retry strategy when fetching from DBnomics API.

## 1.2.3

- Do not fail when fetching a series without dimensions.

## 1.2.2

- Fix error when fetching a series which ID contains a `+` [#972](https://git.nomics.world/dbnomics-fetchers/management/-/issues/972)

## 1.2.1

Non-breaking changes:

- Fix error when series does not use every dimension of the dataset [#660](https://git.nomics.world/dbnomics-fetchers/management/-/issues/660)

## 1.2.0

- Add dimension labels columns to dataframe. See example notebook.

## 1.1.0

- Implement filtering series by passing a `filters` argument to the `fetch_series` and `fetch_series_by_api_link` functions.
- Enhance order of columns in DataFrame to be more convinient to read: frequency, provider, dataset, series and dimensions.
- Enhance error reporting if a series can't be fetched: error is now displayed in red before the DataFrame.

## 1.0.2

The DataFrame returned by `fetch_series_by_api_link` and `fetch_series` now use `numpy.NaN` to represent "NA" (not available) values in its column `value`. A new column names `original_value` is added, in the same spirit than the `original_period` column, to give access to data as stored by DBnomics, but user may prefer to use the `value` column.

## 1.0.0 -> 1.0.1

Fix fetching all the series of a dataset.

## 0.4.0 -> 1.0.0

Breaking changes in Python API:

- `fetch_series` function: rename `code_mask` to `series_code`. Before it could only be a mask. Now it's possible to use it as a normal series code or a mask.

## 0.3.0 -> 0.4.0

Breaking changes in column names:

- Rename `period` to `original_period`, and `period_start_day` to `period`.

## 0.2.1 -> 0.3.0

Breaking changes in Python API:

- Remove `period_to_datetime` keyword argument from functions `fetch_series` and `fetch_series_by_api_link`. A new column named `period_start_day` has been added to the `DataFrame`, which contains the first day of the `period` column. This has been done because some periods formats are not understood by Pandas, for example "2018-B2" which corresponds to march and april 2018. See also: <https://git.nomics.world/dbnomics/dbnomics-data-model/> for a list of periods formats.
