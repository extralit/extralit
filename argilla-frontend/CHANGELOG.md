# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
These are the section headers that we use:
* "Added" for new features.
* "Changed" for changes in existing functionality.
* "Deprecated" for soon-to-be removed features.
* "Removed" for now removed features.
* "Fixed" for any bug fixes.
* "Security" in case of vulnerabilities.
-->

## [Extralit] [0.5.0](https://github.com/extralit/extralit/compare/v0.4.1...v0.5.0)


## [Argilla] [2.8.0](https://github.com/argilla-io/argilla/compare/v2.7.1...v2.8.0)

### Added

- Added Japanese language ([#5816](https://github.com/argilla-io/argilla/pull/5816)). Contributed by @Tomoya-Matsubara.

## [Argilla] [2.7.1](https://github.com/argilla-io/argilla/compare/v2.7.0...v2.7.1)

### Fixed

- Fixed error when requesting dataset info the datasets-viewer API. ([#5804](https://github.com/argilla-io/argilla/pull/5804))

## [Argilla] [2.7.0](https://github.com/argilla-io/argilla/compare/v2.6.0...v2.7.0)

## [Argilla] [2.6.0](https://github.com/argilla-io/argilla/compare/v2.5.0...v2.6.0)

### Added

- Add share progress feature ([#5727](https://github.com/argilla-io/argilla/pull/5727))
- Added feature to export datasets from Argilla to Hugging Face hub from the UI ([#5730](https://github.com/argilla-io/argilla/pull/5730))

### Fixed

- Improved performance and accessibility ([#5724](https://github.com/argilla-io/argilla/pull/5724))
- Fixed dataset update date information in the dataset list ([#5741](https://github.com/argilla-io/argilla/pull/#5741))

## [Argilla] [2.5.0](https://github.com/argilla-io/argilla/compare/v2.4.1...v2.5.0)

### Added

- Add new dataset list page ([#5684](https://github.com/argilla-io/argilla/pull/5684))
- Add a high-contrast theme & improvements for the forced-colors mode. ([#5661](https://github.com/argilla-io/argilla/pull/5661))
- Add English as the default language and add language selector in the user settings page. ([#5690](https://github.com/argilla-io/argilla/pull/5690))

### Fixed

- Assign field to span question on dataset creation. ([#5717](https://github.com/argilla-io/argilla/pull/5717))
- Fixed visible_options when updating question setting. ([#5716](https://github.com/argilla-io/argilla/pull/5716))
- Fixed highlighting on same record ([#5693](https://github.com/argilla-io/argilla/pull/5693))

## [Extralit] [0.4.0](https://github.com/extralit/extralit/compare/v0.3.0...v0.4.0)

### Fixed
- Fixed ES index type for TableField and TableQuestion

## [Extralit] [0.3.0](https://github.com/extralit/extralit/compare/v0.2.3...v0.3.0)

### Added
- Added support for `TableField` for table fields.
- Added `TableQuestion` to support table questions.

### Fixed
- Fixed use_table setting update in `TextField`

### Changed
- Refactored `argilla-frontend/components/base/base-render-table/RenderTable.vue` to add `TableData`, `Validation`, `Extraction` entities.


## [Argilla] [2.4.1](https://github.com/argilla-io/argilla/compare/v2.4.0...v2.4.1)

### Added

- Added redirect to error page when repoId is invalid ([#5670](https://github.com/argilla-io/argilla/pull/5670))

### Fixed

- Fixed redirection problems after users sign-in using HF OAuth. ([#5635](https://github.com/argilla-io/argilla/pull/5635))
- Fixed highlighting of the searched text in text, span and chat fields ([#5678](https://github.com/argilla-io/argilla/pull/5678))
- Fixed validation for rating question when creating a dataset ([#5670](https://github.com/argilla-io/argilla/pull/5670))
- Fixed question name based on question type when creating a dataset ([#5670](https://github.com/argilla-io/argilla/pull/5670))

## [Argilla] [2.4.0](https://github.com/argilla-io/argilla/compare/v2.3.0...v2.4.0)

### Added

- Added new dataset configurator to import datasets from Hugging Face using Argilla UI. ([#5532](https://github.com/argilla-io/argilla/pull/5532))
- Improve Accessibility for Screenreaders ([#5634](https://github.com/argilla-io/argilla/pull/5634))

### Fixed

- Refine German translations and update non-localized UI elements. ([#5632](https://github.com/argilla-io/argilla/pull/5632))

## [Argilla] [2.3.0](https://github.com/argilla-io/argilla/compare/v2.2.0...v2.3.0)

### Added

- Added new field `CustomField`. ([#5462](https://github.com/argilla-io/argilla/pull/5462))

### Fixed

- Fix autofill form on sign-in page. ([#5522](https://github.com/argilla-io/argilla/pull/5522))
- Support copy on clipboard for no secure context. ([#5535](https://github.com/argilla-io/argilla/pull/5535))

## [Argilla] [2.2.0](https://github.com/argilla-io/argilla/compare/v2.1.0...v2.2.0)

### Added

- Added `Required/Optional` label on `Field dataset settings tab` and `Question dataset settings tab`. ([#5394](https://github.com/argilla-io/argilla/pull/5394))
- Added new `ChatField`. ([#5376](https://github.com/argilla-io/argilla/pull/5376))

## [Argilla] [2.1.0](https://github.com/argilla-io/argilla/compare/v2.0.1...v2.1.0)

### Added

- Added `DarkMode` ([#5412](https://github.com/argilla-io/argilla/pull/5412))
- Added new `empty queue messages` ([#5403](https://github.com/argilla-io/argilla/pull/5403))
- Added `HTML Sandbox` to support external and custom CSS and Javascript in fields ([#5353](https://github.com/argilla-io/argilla/pull/5353))
- Added `Spanish` languages ([#5416](https://github.com/argilla-io/argilla/pull/5416))
- Added new `ImageField` supporting URLs and Data URLs. ([#5279](https://github.com/argilla-io/argilla/pull/5279))

> [!NOTE]
> For older versions, please review the argilla/CHANGELOG.md and argilla-server/CHANGELOG.md files.
