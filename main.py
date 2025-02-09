from telegram import InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from PIL import Image
import io
import schedule
import time
import random
import json
import logging
import os
from flask import Flask, request
from threading import Thread

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Clé API Telegram (chargée depuis une variable d'environnement)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7303960829:AAFSS5lpxXt9TXEmoItAyCvNysedsV9M73w")

# URL publique pour le webhook (Replit)
WEBHOOK_URL = f"https://{os.getenv('REPL_SLUG', 'khacnmkg')}.{os.getenv('REPL_OWNER', 'your-replit-username')}.repl.co"

# URL de l'image du token KHACN
IMAGE_URL = "https://raw.githubusercontent.com/startar-bronze/khacngit/main/PNG%20KHAC%20LOGO.png"

# Fichier pour stocker les groupes
GROUPS_FILE = "groups.json"

# Initialiser le fichier groups.json si nécessaire
def initialize_groups_file():
    if not os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "w") as file:
            json.dump([], file)
        logger.info("Fichier groups.json initialisé.")

# Charger la liste des groupes depuis un fichier JSON
def load_groups():
    try:
        with open(GROUPS_FILE, "r") as file:
            groups = json.load(file)
            if not isinstance(groups, list):  # Vérifie que le contenu est un tableau
                logger.error("Le fichier groups.json est mal formé. Réinitialisation.")
                return []
            return groups
    except FileNotFoundError:
        logger.info("Le fichier groups.json n'existe pas. Création d'un fichier vide.")
        return []
    except json.JSONDecodeError:
        logger.error("Le fichier groups.json est mal formé. Réinitialisation.")
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
async def start(update, context):
    price = get_khacn_price()
    message_fr = f"""
Bienvenue dans le bot KharYsma Coin ! 🚀
Prix actuel : ${price:.2f} USD
"""
    message_en = f"""
Welcome to the KharYsma Coin bot! 🚀
Current Price: ${price:.2f} USD
"""
    await update.message.reply_text(message_fr)
    await update.message.reply_text(message_en)

async def shill(update, context):
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
Contract: 0x11c1b94294A7967092F747434dee4876eca5fD53
Website: https://khacn.startarcoins.com
Uniswap Pool: https://app.uniswap.org/explore/tokens/ethereum/0x11c1b94294a7967092f747434dee4876eca5fd53
Market Cap: https://topcryptocap.org
"""
    await update.message.reply_text(message_fr)
    await update.message.reply_text(message_en)

# Message de bienvenue privée
async def welcome_new_member(update, context):
    for member in update.message.new_chat_members:
        message = f"""
Bonjour {member.first_name} ! 🚀

Bienvenue dans le groupe KharYsma Coin ! Voici comment participer activement :

✅ **Devenir Liquidity Provider** :
1. Ajoutez du liquidity à notre pool Uniswap.
2. Suivez ce lien : https://app.uniswap.org/explore/tokens/ethereum/0x11c1b94294a7967092f747434dee4876eca5fd53
3. Configurez le prix à 1 KHACN = 550 USD minimum.
4. Connectez votre portefeuille Ethereum (MetaMask ou autre).

✅ **Acheter des KHACN** :
1. Ajoutez KHACN comme token personnalisé dans votre portefeuille avec l'adresse : 0x11c1b94294A7967092F747434dee4876eca5fD53.
2. Suivez ce lien : https://app.uniswap.org/explore/tokens/ethereum/0x11c1b94294a7967092f747434dee4876eca5fd53
3. Suivez les instructions à l'écran pour échanger vos ETH contre des KHACN.

Rejoignez-nous sur : https://t.me/gbtcryptohub
Site web : https://khacn.startarcoins.com
"""
        try:
            await context.bot.send_message(chat_id=member.id, text=message)
        except Exception as e:
            logger.error(f"Impossible d'envoyer un message privé à {member.first_name} : {e}")

# Publication automatique dans des groupes
async def send_shill_message(application):
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
            await application.bot.send_media_group(chat_id=group_id, media=[media])
            time.sleep(2)  # Attendre 2 secondes entre les messages

            media = InputMediaPhoto(media=resized_image, caption=message_en)
            await application.bot.send_media_group(chat_id=group_id, media=[media])
            time.sleep(2)  # Attendre 2 secondes entre les messages

        except Exception as e:
            logger.error(f"Erreur lors de la publication dans le groupe {group_id} : {e}")
            groups_to_remove.append(group_id)

    # Supprimer les groupes où le bot a échoué
    for group_id in groups_to_remove:
        GROUPS_TO_POST.remove(group_id)
    save_groups(GROUPS_TO_POST)

# Planification des tâches
def schedule_tasks(application):
    bot = application.bot
    schedule.every(1).hours.do(lambda: asyncio.create_task(send_shill_message(application)))

# Configurer le webhook
async def configure_webhook(application):
    if WEBHOOK_URL:
        try:
            await application.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
            logger.info(f"Webhook configuré avec succès sur {WEBHOOK_URL}/{TOKEN}.")
        except Exception as e:
            logger.error(f"Erreur lors de la configuration du webhook : {e}")
            application.run_polling()  # Basculer vers polling en cas d'échec
    else:
        logger.error("L'URL du webhook n'est pas définie. Le bot utilisera polling...")
        application.run_polling()

# Maintenir le bot en ligne avec Flask
def keep_alive():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Bot en ligne !"

    @app.route('/' + TOKEN, methods=['POST'])
    async def webhook():
        update = await application.update_queue.put(request.get_json(force=True))
        return '', 200

    def run():
        app.run(host='0.0.0.0', port=8080)

    t = Thread(target=run)
    t.start()

# Gestionnaire d'erreurs global
async def error_handler(update, context):
    logger.error(f"Erreur non gérée : {context.error}")
    if update.effective_message:
        await update.effective_message.reply_text("Une erreur s'est produite. Veuillez réessayer plus tard.")

# Fonction principale
async def main():
    global GROUPS_TO_POST

    # Initialiser le fichier groups.json si nécessaire
    initialize_groups_file()

    # Charger les groupes existants
    GROUPS_TO_POST = load_groups()

    # Initialiser l'application
    application = Application.builder().token(TOKEN).build()

    # Ajouter des commandes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shill", shill))

    # Gérer les nouveaux membres
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    # Ajouter un gestionnaire d'erreurs global
    application.add_error_handler(error_handler)

    # Configurer le webhook ou utiliser polling
    await configure_webhook(application)

    # Maintenir le bot en ligne
    keep_alive()

    # Boucle infinie pour exécuter les tâches planifiées
    while True:
        try:
            schedule.run_pending()
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Erreur critique dans le scheduler : {e}")
            await asyncio.sleep(10)  # Attente avant de réessayer

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
