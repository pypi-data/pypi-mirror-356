# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]

## [0.7.0] - 2025-06-20

### Fixed
- Changed embedding endpoint to be OAI compatible


## [0.6.0] - 2024-08-06

### Fixed

- Add constrained decoding backends as a generation parameter.

## [0.5.0] - 2024-08-06

### Fixed

- Add detokenization and tokenization endpoints.


## [0.4.3] - 2024-08-06

### Fixed

- Add chat templates
  

## [0.4.2] - 2024-06-07

### Fixed

- Add status endpoints into client, using the management API.

## [0.4.1] - 2024-03-19

### Fixed

- Fix the compatibility issue within takeoff-config package. Now starting from this version, we seperate the distribution since takeoff-config needs to follow cross-platform release strategy.

## [0.4.0] - 2024-03-07

### Added

- Support for management api endpoints, new release process that pushes takeoff-config to pypi alongside the client with the same version [PR 1079](https://github.com/TNBase/pantheon/pull/1079)

## [0.3.0] - 2024-02-27

### Fixed

- fix the client package unit tests support for python 3.8
- fix the compatibility issue in takeoff client

## [0.2.0] - 2024-02-19

### Added

- add support for image to text models, by adding an `image_path` keyword argument to the `generate` method.

### Changed

- Changed default value for embedding endpoint from `'embed'` to `'primary'` to match takeoff defaults.

## [0.1.0] - 2024-02-07

### Added

- add classify to the takeoff client to match the new endpoint

## [0.0.4] - 2024-01-06

### Added

- add sseclient-py dependency into pyproject.toml

## [0.0.3] - 2024-01-05

- initial release
- add takeoff python client, publishing on [PyPI](https://pypi.org/project/takeoff-client/)

<!-- Links -->

[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
