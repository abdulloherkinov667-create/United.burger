from aiogram import Router, F
from aiogram.types import CallbackQuery

from buttons.inline_butto import (
    start_inline_buttons,
    categories_inline_buttons,
    products_inline_buttons,
    product_detail_inline_buttons,
)
from database import (
    get_all_categories,
    get_category_by_id,
    get_products_by_category,
    get_product_by_id,
)

router = Router()


@router.callback_query(F.data == "main_menu")
async def show_categories(callback: CallbackQuery):
    categories = get_all_categories()

    if not categories:
        await callback.answer("Hozircha hech qanday kategoriya yo'q!", show_alert=True)
        return

    try:
        await callback.message.delete()
    except Exception:
        pass

    # Menyu bosilganda chiqadigan qiziqarli matn
    welcome_text = (
        "🍔 *Ishtahangiz qo'zg'aldimi?* 🍔\n\n"
        "Bizning *Premium Katalog* sizni mazali taomlar bilan kutmoqda!\n"
        "Har bir mahsulot sevgi va did bilan tayyorlanadi 😋\n\n"
        "👇 *Quyidan o'zingizga yoqqan kategoriyani tanlang:*"
    )

    await callback.message.answer(
        text=welcome_text,
        reply_markup=categories_inline_buttons(categories),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("category_"))
async def show_category_products(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    products = get_products_by_category(category_id)

    if not products:
        await callback.answer("Bu kategoriyada hozircha mahsulot yo'q!", show_alert=True)
        return

    try:
        await callback.message.delete()
    except Exception:
        pass

    # Kategoriya rasmini bazadan olamiz
    category = get_category_by_id(category_id)
    category_image = category[2] if category and category[2] else None

    caption_text = (
        "✨ *Kategoriya ichidagi mahsulotlar ro'yxati:*\n\n"
        "👇 Quyidagi tugmalardan birini tanlang:"
    )

    if category_image:
        try:
            await callback.message.answer_photo(
                photo=category_image,
                caption=caption_text,
                reply_markup=products_inline_buttons(products),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Kategoriya rasmi xato: {e}")
            await callback.message.answer(
                text=caption_text,
                reply_markup=products_inline_buttons(products),
                parse_mode="Markdown"
            )
    else:
        await callback.message.answer(
            text=caption_text,
            reply_markup=products_inline_buttons(products),
            parse_mode="Markdown"
        )

    await callback.answer()


@router.callback_query(F.data.startswith("product_"))
async def show_product_detail(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = get_product_by_id(product_id)

    if not product:
        await callback.answer("Mahsulot topilmadi!", show_alert=True)
        return

    _, category_id, name, price, description, image_id = product

    try:
        price_formatted = f"{int(price):,}"
    except (ValueError, TypeError):
        price_formatted = str(price)

    caption = (
            f"📝 *Batafsil:* {description}\n\n"
            f"👑 *Nomi:* *{name}*\n"
            f"💰 *Narxi:* *{price_formatted} so'm*\n"            
        )

    try:
        await callback.message.delete()
    except Exception:
        pass

    try:
        await callback.message.answer_photo(
            photo=image_id,
            caption=caption,
            reply_markup=product_detail_inline_buttons(category_id=category_id),
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"Mahsulot rasmi xato: {e}")
        await callback.message.answer(
            text=caption,
            reply_markup=product_detail_inline_buttons(category_id=category_id),
            parse_mode="Markdown",
        )

    await callback.answer()


@router.callback_query(F.data == "back_to_start")
async def back_to_start_handler(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer(
        text="🏠 *Asosiy menyuga qaytdingiz:*",
        reply_markup=start_inline_buttons(),
        parse_mode="Markdown"
    )
    await callback.answer()