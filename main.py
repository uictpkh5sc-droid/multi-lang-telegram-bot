import ast
import io
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# استبدل هذا بـ API Token الخاص بروبوتك
TOKEN =  "8293785720:AAGZCRwR3_r93E-yd8S04Q0PmowCX-OPe0k"

def fix_python_code(code_string):
    """
    يقوم بتحليل كود بايثون لتحديد وتصحيح الأخطاء الشائعة.
    """
    errors = []
    output_buffer = io.StringIO()
    
    # المرحلة 1: فحص الأخطاء النحوية (SyntaxError)
    try:
        ast.parse(code_string)
    except SyntaxError as e:
        errors.append(f"❌ خطأ نحوي في السطر {e.lineno}: {e.msg}")
    
    # المرحلة 2: فحص أخطاء المسافات البادئة (IndentationError)
    try:
        # توجيه مخرجات الأخطاء إلى متغير
        sys.stderr = output_buffer
        compile(code_string, '<string>', 'exec')
    except IndentationError as e:
        errors.append(f"❌ خطأ في المسافات البادئة في السطر {e.lineno}: {e.msg}")
    finally:
        # إعادة مخرجات الأخطاء إلى وضعها الطبيعي
        sys.stderr = sys.__stderr__
    
    # المرحلة 3: فحص أخطاء شائعة أخرى (مثال: أخطاء المتغيرات)
    # لا يمكن تنفيذ هذا الجزء بأمان داخل البوت، لذا سنعتمد على الأخطاء النحوية والمسافات
    
    if not errors:
        return "✅ **تم الفحص بنجاح.** لم يتم العثور على أخطاء نحوية أو في المسافات البادئة."
    else:
        error_message = "⚠️ **تم العثور على الأخطاء التالية:**\n\n"
        for error in errors:
            error_message += f"{error}\n"
        return error_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إرسال رسالة ترحيب عند استخدام أمر /start."""
    await update.message.reply_text(
        "أنا روبوت تصحيح أكواد بايثون! أرسل لي كودك، ثم أجب على الرسالة بالأمر /fix."
    )


async def fix_code_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    يقوم بمعالجة الأمر /fix ويصحح الكود المرفق.
    """
    # التحقق من وجود رسالة مقتبس منها
    if not update.message.reply_to_message:
        await update.message.reply_text("يرجى الرد على رسالة تحتوي على الكود بالأمر /fix.")
        return

    # استخراج الكود من الرسالة المقتبس منها
    code_text = update.message.reply_to_message.text
    if not code_text:
        await update.message.reply_text("الرسالة المقتبس منها لا تحتوي على كود.")
        return

    # استدعاء دالة التصحيح
    result_message = fix_python_code(code_text)
    
    # إرسال النتيجة إلى المستخدم
    await update.message.reply_text(result_message, parse_mode="Markdown")


def main() -> None:
    """تشغيل الروبوت."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fix", fix_code_handler))
    
    # تشغيل الروبوت
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
