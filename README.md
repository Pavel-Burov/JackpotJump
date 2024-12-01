# Jackpot Game Automation

## Overview
This project automates interactions with the Jackpot Jump game on the Kingmaker Games website. It launches 200 accounts across 10 servers, simulates predefined click patterns, and performs automated game interactions.

## Requirements
- Python 3.x
- Playwright
- Docker (optional for multi-server setup)

## Installation
1. Install Python dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Install Playwright:
    ```
    python -m playwright install
    ```

## Usage
1. Configure the settings in `config/settings.py`.
2. Run the automation:
    ```
    python main.py
    ```

## Logging
Logs will be written to the `logs/automation.log` file.
