# Nutrition & Wellness Telegram Bot

Bot Telegram che offre consigli nutrizionali, con accesso premium tramite abbonamento Stripe da 9€/mese.

## Funzionalità
- Accesso via abbonamento mensile (Stripe)
- Consigli nutrizionali automatici
- Integrazione con Telegram Bot API

## Setup locale
1. **Crea un file `.env`** nella root del progetto con questo contenuto:

   ```env
   TELEGRAM_TOKEN=il_tuo_token_telegram
   STRIPE_SECRET_KEY=la_tua_chiave_segreta_stripe
   STRIPE_PRICE_ID=il_tuo_price_id_stripe
