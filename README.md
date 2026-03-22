# Discord Betting Bot

A simple coin flip betting bot for private Discord servers. Runs locally on your machine — no cloud hosting needed for the bot itself.

---

## Infrastructure

| Component | What | Notes |
|---|---|---|
| **Bot** | Python script running on your local machine | Keep your terminal/PC on while playing |
| **Database** | [Supabase](https://supabase.com) (hosted PostgreSQL) | Free tier, cloud-hosted, always on |
| **Discord** | Discord Bot Token | Registered at discord.com/developers |

```
Your PC (runs bot.py)
      │
      │  discord.py (WebSocket)
      ▼
Discord Servers API
      │
      │  psycopg2 (TCP)
      ▼
Supabase PostgreSQL (cloud)
```

> The bot process must be running on your local machine for commands to work. If you close the terminal, the bot goes offline. The Supabase database stays online independently.

---

## Prerequisites

- Python 3.11+
- A [Supabase](https://supabase.com) project (free tier is fine)
- A Discord Bot Token from [discord.com/developers](https://discord.com/developers/applications)

---

## Setup

**1. Clone and install dependencies**
```bash
pip install -r requirements.txt
```

**2. Configure environment**
```bash
copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux
```

Edit `.env` and fill in both values:
```
DISCORD_TOKEN=your_discord_bot_token
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

> Get `DATABASE_URL` from: Supabase Dashboard → Project → **Settings → Database → Connection string → URI**

**3. Run the bot**
```bash
py bot.py
```

You should see:
```
Logged in as CBot#1234 (ID: ...)
```

The `users` table is created automatically in Supabase on first run.

---

## Commands

| Command | Example | Description |
|---|---|---|
| `cbot coinflip <amount> <heads\|tails>` | `cbot coinflip 200 heads` | Bet on a coin flip |
| `cbot balance` | `cbot balance` | Check your coin balance |
| `cbot give <@user> <amount>` | `cbot give @friend 100` | Transfer coins to a player |
| `cbot cam` | `cbot cam` | 👑 |
| `cbot tin` | `cbot tin` | 👑 |
| `cbot help` | `cbot help` | Show this command list |

**Aliases:** `coinflip` → `cf` · `balance` → `bal`

> Every new user starts with **1000 coins** automatically.

---

## Invite Bot to Server

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications) → your app
2. **OAuth2 → URL Generator** → scope: `bot` → permissions: `Send Messages`, `Read Message History`
3. Copy the generated URL → paste in browser → select your server → Authorize
4. Enable **Message Content Intent** under **Bot → Privileged Gateway Intents**

---

## Troubleshooting

| Error | Likely Cause | Fix |
|---|---|---|
| `KeyError: DATABASE_URL` | `.env` file missing | Copy `.env.example` to `.env` |
| `could not translate host name` | DNS / network issue or Supabase project paused | Check Supabase dashboard, try DNS `1.1.1.1` |
| Bot not responding | Message Content Intent disabled | Enable it in Discord Developer Portal |
| Bot offline | Local script not running | Run `py bot.py` again |

---

> **Security:** Never commit `.env` to version control. It is listed in `.gitignore` by default.
