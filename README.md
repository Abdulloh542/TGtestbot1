# Telegram Shop Bot (aiogram v3)

Uzbek tilidagi onlayn do'kon bot. Mahsulotlar, savat, buyurtmalar, admin panel va support ticketlar bilan.

## Talablar
- Python 3.11+
- Telegram bot token

## Konfiguratsiya
`.env.example` faylidan nusxa oling:

```bash
cp .env.example .env
```

`.env` ichida quyidagilarni to'ldiring:
- `BOT_TOKEN`
- `ADMIN_IDS` (vergul bilan ajratilgan Telegram user IDlar)
- `DATABASE_URL` (standart: `sqlite+aiosqlite:///./shop.db`, Postgres uchun `postgresql+asyncpg://user:pass@host:5432/db`)

## O'rnatish

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ishga tushirish (Polling)

```bash
./start.sh
```

## Migratsiya va seed
Ushbu loyiha SQLAlchemy `create_all()` bilan ishga tushganda jadval yaratadi va demo data (`3x5` mahsulot) seed qiladi.

## Asosiy imkoniyatlar
- Kategoriyalar -> mahsulotlar -> mahsulot tafsiloti
- Savat (qty +/-), tozalash, checkout
- Buyurtmalarim (so'nggi 10 ta)
- Support ticketlar va admin javobi
- Admin panel (yangi buyurtmalar, status, statistika, CSV eksport)

## Deploy qilish

### Render
1. Repo'ni Render'ga ulang.
2. Environment Variables bo'limida `BOT_TOKEN`, `ADMIN_IDS`, `DATABASE_URL` ni kiriting.
3. Start command: `./start.sh`

### Railway
1. Project yarating va repo'ni ulang.
2. Variables ichida `BOT_TOKEN`, `ADMIN_IDS`, `DATABASE_URL` ni kiriting.
3. Start command: `./start.sh`

### VPS (systemd)

```bash
sudo useradd -m telegrambot
sudo su - telegrambot

git clone <repo_url>
cd <repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`/etc/systemd/system/shopbot.service`:

```ini
[Unit]
Description=Telegram Shop Bot
After=network.target

[Service]
Type=simple
User=telegrambot
WorkingDirectory=/home/telegrambot/<repo>
Environment=BOT_TOKEN=your_token
Environment=ADMIN_IDS=123456789
Environment=DATABASE_URL=sqlite+aiosqlite:///./shop.db
ExecStart=/home/telegrambot/<repo>/.venv/bin/python -m app.main
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable shopbot
sudo systemctl start shopbot
sudo systemctl status shopbot
```
