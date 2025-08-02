import telebot
from telebot import types
from googletrans import Translator, LANGUAGES

# قم باستبدال 'YOUR_BOT_TOKEN' بالتوكن الخاص بك
BOT_TOKEN = 'BOT_TOKEN'
bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()

# قائمة باللغات المدعومة مع أسماء ودية
LANG_OPTIONS = {
    'العربية': 'ar', 'الإنجليزية': 'en', 'الفرنسية': 'fr',
    'الألمانية': 'de', 'الإسبانية': 'es', 'الروسية': 'ru',
    'الصينية': 'zh-cn', 'اليابانية': 'ja', 'الكورية': 'ko'
}

# أمر /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    # إضافة أزرار اللغات للترحيب
    buttons = [types.KeyboardButton(lang) for lang in LANG_OPTIONS.keys()]
    markup.add(*buttons)
    
    bot.send_message(message.chat.id, 
                     "أهلاً بك! أنا **بوت الترجمة السريعة**.\n"
                     "أرسل لي أي نص، وسأترجمه لك على الفور.\n\n"
                     "**أولًا، اختر لغة الترجمة من الأزرار الموجودة في الأسفل:**", 
                     reply_markup=markup, 
                     parse_mode='Markdown')

# معالجة اختيار اللغة
@bot.message_handler(func=lambda message: message.text in LANG_OPTIONS)
def set_language(message):
    lang_name = message.text
    lang_code = LANG_OPTIONS[lang_name]
    
    # حفظ اللغة المختارة للمستخدم الحالي
    bot.user_data = getattr(bot, 'user_data', {})
    bot.user_data[message.chat.id] = {'target_lang': lang_code}
    
    bot.reply_to(message, 
                 f"تم اختيار **{lang_name}** كلغة ترجمة.\n"
                 "الآن أرسل لي النص الذي تريد ترجمته.",
                 parse_mode='Markdown')

# معالجة النصوص للترجمة
@bot.message_handler(func=lambda message: True)
def translate_message(message):
    user_id = message.chat.id
    
    # التحقق مما إذا كان المستخدم قد اختار لغة من قبل
    if not hasattr(bot, 'user_data') or user_id not in bot.user_data:
        send_welcome(message) # إعادة توجيه المستخدم لصفحة الترحيب لاختيار اللغة
        return

    try:
        text_to_translate = message.text
        target_lang_code = bot.user_data[user_id]['target_lang']
        
        # الكشف عن لغة النص المصدر لتجنب الترجمة لنفس اللغة
        detected_lang = translator.detect(text_to_translate).lang
        
        if detected_lang == target_lang_code:
            bot.reply_to(message, 
                         "النص الذي أرسلته بنفس لغة الترجمة المختارة. يرجى إرسال نص بلغة مختلفة.")
            return

        translated_text = translator.translate(text_to_translate, dest=target_lang_code).text
        
        # الحصول على اسم اللغة الهدف من الكود
        target_lang_name = next(name for name, code in LANG_OPTIONS.items() if code == target_lang_code)
        
        response = f"**تمت الترجمة إلى {target_lang_name}:**\n{translated_text}"
                   
        bot.send_message(message.chat.id, response, parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, "عذرًا، حدث خطأ أثناء الترجمة. يرجى المحاولة مرة أخرى.")

# تشغيل البوت
if __name__ == "__main__":
    print("البوت يعمل الآن...")
    bot.polling()
    bot.reply_to(message, 
                 f"تم اختيار **{lang_name}** كلغة ترجمة.\n"
                 "الآن أرسل لي النص الذي تريد ترجمته.",
                 parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    user_id = message.chat.id
    if not hasattr(bot, 'user_data') or user_id not in bot.user_data:
        send_welcome(message)
        return

    try:
        text_to_translate = message.text
        target_lang_code = bot.user_data[user_id]['target_lang']
        detected_lang = translator.detect(text_to_translate).lang

        if detected_lang == target_lang_code:
            bot.reply_to(message, 
                         "النص الذي أرسلته بنفس لغة الترجمة المختارة. يرجى إرسال نص بلغة مختلفة.")
            return

        translated_text = translator.translate(text_to_translate, dest=target_lang_code).text
        target_lang_name = next(name for name, code in LANG_OPTIONS.items() if code == target_lang_code)

        response = f"**تمت الترجمة إلى {target_lang_name}:**\n{translated_text}"
        bot.send_message(message.chat.id, response, parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, "عذرًا، حدث خطأ أثناء الترجمة. يرجى المحاولة مرة أخرى.")

if __name__ == "__main__":
    print("البوت يعمل الآن...")
    bot.polling()
