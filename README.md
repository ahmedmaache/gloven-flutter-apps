# Gloven Flutter Apps - 100 Apps Project

This repository contains 100 Flutter applications, all configured for Google Play Store publishing with package names under `org.gloven.*`.

## Structure

- `apps/` - Contains all 100 Flutter applications
- `.github/workflows/` - GitHub Actions workflows for building and publishing
- `scripts/` - Automation scripts for app generation and management

## Package Naming

All apps use the package naming convention: `org.gloven.app{01-100}`

## Building AAB Files

GitHub Actions automatically builds signed AAB files for all apps when changes are pushed.

## Publishing to Play Store

The workflow can automatically publish apps to Google Play Console using GitHub Actions.

