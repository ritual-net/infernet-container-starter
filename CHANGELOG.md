# Changelog

All notable changes to this project will be documented in this file.

- ##### The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
- ##### This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - XXXX-XX-XX

### Changed
- Simplified examples to the minimum core functionality necessary and removed all dependencies on `infernet-ml`.
- Updated images used for deploying the Infernet Node.

## [1.0.2] - 2024-07-31

### Changed
- Set `trail_head_blocks` to `0` in `config.json` for all projects. This fixes an issue where the node would not start due to a lack of trailing blocks.
- Updated `registry_address` to `0x663F3ad617193148711d28f5334eE4Ed07016602` to point to the correct registry address

## [1.0.1] - 2024-07-31

### Fixed
- `config.json` fixes to adhere to node `v1.0.0` configuration specification.
- Bumped dependency versions to fix vulnerabilities.
- Pinned image versions in `docker-compose.yaml`.

## [1.0.0] - 2024-06-06

### Added
- New project `payment` for an end-to-end flow of the payments feature of `infernet
  1.0.0`.

### Changed
- All workflows are updated to use `infernet-ml 1.0.0`
- All contracts are updated to use `infernet-sdk 1.0.0`

### Fixed
- Recursive submodule cloning issue with forge's libraries.

## [0.1.0] - 2024-03-21

### Added
- Initial release of the Infernet Container Starter repository.
