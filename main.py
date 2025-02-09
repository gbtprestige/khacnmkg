from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from PIL import Image
import io
import schedule
import time
import random
import json
import logging

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Clé API Telegram (remplacez par votre clé réelle)
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# URL de l'image du token KHACN
IMAGE_URL = "https://raw.githubusercontent.com/startar-bronze/khacngit/main/PNG%20KHAC%20LOGO.png"

# Fichier pour stocker les groupes
GROUPS_FILE = "groups.json"

# Charger la liste des groupes depuis un fichier JSON
def load_groups():
    try:
        with open(GROUPS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Sauvegarder la liste des groupes dans un fichier JSON
def save_groups(groups):
    with open(GROUPS_FILE, "w") as file:
        json.dump(groups, file)

# Fonction pour récupérer le prix du KHACN depuis l'API
def get_khacn_price():
    try:
        response = requests.get("https://topcryptocap.org/api/khacn", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return float(data.get("price_usd", 550))  # Utilise 550 comme valeur par défaut
        else:
            logger.error(f"Erreur lors de la requête API : {response.status_code}")
            return 550  # Valeur par défaut
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du prix : {e}")
        return 550  # Valeur par défaut

# Fonction pour redimensionner l'image
def resize_image(image_url):
    try:
        response = requests.get(image_url, timeout=10)
        img = Image.open(io.BytesIO(response.content))
        img_resized = img.resize((300, 300))  # Redimensionne l'image à 300x300 pixels
        img_byte_arr = io.BytesIO()
        img_resized.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return img_byte_arr
    except Exception as e:
        logger.error(f"Erreur lors du redimensionnement de l'image : {e}")
        return None

# Messages en français et anglais
def start(update: Update, context: CallbackContext):
    price = get_khacn_price()
    message_fr = f"""
    Bienvenue dans le bot KharYsma Coin ! 🚀
    Prix actuel : ${price:.2f} USD
    """
    message_en = f"""
    Welcome to the KharYsma Coin bot! 🚀
    Current Price: ${price:.2f} USD
    """
    update.message.reply_text(message_fr)
    update.message.reply_text(message_en)

def shill(update: Update, context: CallbackContext):
    price = get_khacn_price()
    message_fr = f"""
    💰 Investissez dans KharYsma Coins !
    Prix actuel : ${price:.2f} USD
    Token ERC-20 innovant basé sur les actifs tangibles de l'artiste KharYsma Arafat NZABA.
    Contrat : 0x11c1b94294A7967092F747434dEE4876EcA5fD53
    Site web : https://khacn.startarcoins.com
    Pool Uniswap : https://app.uniswap.org/explore/tokens/ethereum/0x11c1b94294a7967092f747434dee4876eca5fd53
    Capitalisation : https://topcryptocap.org
    """
    message_en = f"""
    💰 Invest in KharYsma Coins!
    Current Price: ${price:.2f} USD
    Innovative ERC-20 token based on the tangible assets of artist KharYsma Arafat NZABA.
    Contract: 0x11c1b94294A7967092F747434dEE4876EcA5fD53
    Website: https://khacn.startarcoins.com
    Uniswap Pool: https://app.uniswap.org/explore/tokens/ethereum/0x11c1b94294a7967092f747434dee4876eca5fd53
    Market Cap: https://topcryptocap.org
    """
    update.message.reply_text(message_fr)
    update.message.reply_text(message_en)

# Publication automatique dans des groupes
def send_shill_message(bot):
    global GROUPS_TO_POST

    if not GROUPS_TO_POST:
        logger.info("Aucun groupe configuré pour la publication.")
        return

    price = get_khacn_price()
    message_fr = f"🚀 KharYsma Coins - L'avenir des cryptos ! Prix actuel : ${price:.2f} USD. Rejoignez-nous : https://khacn.startarcoins.com"
    message_en = f"🚀 KharYsma Coins - The future of crypto! Current price: ${price:.2f} USD. Join us: https://khacn.startarcoins.com"

    resized_image = resize_image(IMAGE_URL)
    if not resized_image:
        logger.error("Impossible de redimensionner l'image.")
        return

    groups_to_remove = []

    for group_id in GROUPS_TO_POST:
        try:
            media = InputMediaPhoto(media=resized_image, caption=message_fr)
            bot.send_media_group(chat_id=group_id, media=[media])
            time.sleep(2)  # Attendre 2 secondes entre les messages

            media = InputMediaPhoto(media=resized_image, caption=message_en)
            bot.send_media_group(chat_id=group_id, media=[media])
            time.sleep(2)  # Attendre 2 secondes entre les messages

        except Exception as e:
            logger.error(f"Erreur lors de la publication dans le groupe {group_id} : {e}")
            groups_to_remove.append(group_id)

    # Supprimer les groupes où le bot a échoué
    for group_id in groups_to_remove:
        GROUPS_TO_POST.remove(group_id)
    save_groups(GROUPS_TO_POST)

# Ajout automatique de nouveaux groupes
def add_new_groups(bot):
    global GROUPS_TO_POST

    new_groups = fetch_relevant_groups()

    for group_id in new_groups:
        if group_id not in GROUPS_TO_POST:
            try:
                # Vérifie si le bot peut poster dans le groupe
                bot.send_message(chat_id=group_id, text="Test de connexion au groupe.", timeout=10)
                GROUPS_TO_POST.append(group_id)
                save_groups(GROUPS_TO_POST)
                logger.info(f"Groupe ajouté : {group_id}")
            except Exception as e:
                logger.error(f"Impossible d'ajouter le groupe {group_id} : {e}")

# Récupérer des groupes pertinents via un service tiers
def fetch_relevant_groups():
    try:
        # Exemple : Utiliser un service tiers pour récupérer des groupes publics
        response = requests.get("https://api.telegram-groups-service.com/crypto-groups", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("groups", [])
        else:
            logger.error(f"Erreur lors de la récupération des groupes : {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des groupes : {e}")
        return []

# Planification des tâches
def schedule_tasks(updater):
    bot = updater.bot
    schedule.every(1).hours.do(send_shill_message, bot)
    schedule.every(6).hours.do(add_new_groups, bot)

def main():
    global GROUPS_TO_POST

    # Charger les groupes existants
    GROUPS_TO_POST = load_groups()

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Ajouter des commandes
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("shill", shill))

    # Démarrer le bot
    updater.start_polling()

    # Gestion des tâches planifiées
    schedule_tasks(updater)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logger.error(f"Erreur critique dans le scheduler : {e}")
            time.sleep(10)  # Attente avant de réessayer

if __name__ == "__main__":
    main()
