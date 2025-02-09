from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from PIL import Image
import io
import schedule
import time
import random

# Clé API Telegram
TOKEN = "7303960829:AAFSS5lpxXt9TXEmoItAyCvNysedsV9M73w"

# URL de l'image du token KHACN
IMAGE_URL = "https://raw.githubusercontent.com/startar-bronze/khacngit/main/PNG%20KHAC%20LOGO.png"

# Fonction pour récupérer le prix du KHACN depuis l'API
def get_khacn_price():
    try:
        response = requests.get("https://topcryptocap.org/api/khacn")
        data = response.json()
        return data.get("price_usd", "N/A")
    except Exception as e:
        print(f"Erreur lors de la récupération du prix : {e}")
        return "N/A"

# Fonction pour redimensionner l'image
def resize_image(image_url):
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))
    img_resized = img.resize((300, 300))  # Redimensionne l'image à 300x300 pixels
    img_byte_arr = io.BytesIO()
    img_resized.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr

# Messages en français et anglais
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bienvenue dans le bot KharYsma Coin ! 🚀")
    update.message.reply_text("Welcome to the KharYsma Coin bot! 🚀")

def shill(update: Update, context: CallbackContext):
    price = get_khacn_price()
    message_fr = f"""
    💰 Investissez dans KharYsma Coins !
    Prix actuel : ${price} USD
    Token ERC-20 innovant basé sur les actifs tangibles de l'artiste KharYsma Arafat NZABA.
    Contrat : 0x11c1b94294A7967092F747434dEE4876EcA5fD53
    Site web : https://khacn.startarcoins.com
    Pool Uniswap : https://app.uniswap.org/explore/tokens/ethereum/0x11c1b94294a7967092f747434dee4876eca5fd53
    Capitalisation : https://topcryptocap.org
    """
    message_en = f"""
    💰 Invest in KharYsma Coins!
    Current Price: ${price} USD
    Innovative ERC-20 token based on the tangible assets of artist KharYsma Arafat NZABA.
    Contract: 0x11c1b94294A7967092F747434dEE4876EcA5fD53
    Website: https://khacn.startarcoins.com
    Uniswap Pool: https://app.uniswap.org/explore/tokens/ethereum/0x11c1b94294a7967092f747434dee4876eca5fd53
    Market Cap: https://topcryptocap.org
    """
    update.message.reply_text(message_fr)
    update.message.reply_text(message_en)

# Recherche automatique de groupes pertinents
def find_and_post(bot):
    # Liste de mots-clés pour trouver des groupes pertinents
    keywords = ["crypto", "blockchain", "ethereum", "defi", "tokens"]

    for keyword in keywords:
        try:
            # Recherche de groupes (simulée car Telegram n'autorise pas directement la recherche programmatique)
            groups = simulate_group_search(keyword)  # Fonction simulée

            for group_id in groups:
                price = get_khacn_price()
                message_fr = f"🚀 KharYsma Coins - L'avenir des cryptos ! Prix actuel : ${price} USD. Rejoignez-nous : https://khacn.startarcoins.com"
                message_en = f"🚀 KharYsma Coins - The future of crypto! Current price: ${price} USD. Join us: https://khacn.startarcoins.com"

                # Redimensionner l'image
                resized_image = resize_image(IMAGE_URL)

                # Envoyer le message avec l'image
                media = InputMediaPhoto(media=resized_image, caption=message_fr)
                bot.send_media_group(chat_id=group_id, media=[media])
                time.sleep(2)  # Attendre 2 secondes entre les messages

                media = InputMediaPhoto(media=resized_image, caption=message_en)
                bot.send_media_group(chat_id=group_id, media=[media])
                time.sleep(2)  # Attendre 2 secondes entre les messages

        except Exception as e:
            print(f"Erreur lors de la publication dans les groupes : {e}")

# Simulation de la recherche de groupes
def simulate_group_search(keyword):
    # Simule la recherche de groupes pertinents (remplacez par une implémentation réelle si possible)
    return ["-1001234567890", "-1009876543210"]  # IDs simulés de groupes

# Planification des publications automatiques
def schedule_posts(updater):
    bot = updater.bot
    schedule.every(1).hours.do(find_and_post, bot)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Ajouter des commandes
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("shill", shill))

    # Démarrer le bot
    updater.start_polling()

    # Gestion des tâches planifiées
    schedule_posts(updater)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
