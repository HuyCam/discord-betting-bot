# Discord Betting Bot

A simple coin flip betting bot for private Discord servers.

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials
2. `pip install -r requirements.txt`
3. `python bot.py`

## Commands

| Command | Example | Description |
|---|---|---|
| `cbot coinflip <amount>` | `cbot coinflip 200` | 50/50 win or lose |
| `cbot balance` | `cbot balance` | Check your coin balance |
| `cbot give <@user> <amount>` | `cbot give @friend 100` | Transfer coins |

> **Note:** Keep your `.env` file secret and never commit it to version control.
