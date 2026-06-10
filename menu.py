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

    await callback.message.answer(
        text="Kategoriyani tanlang:",
        reply_markup=categories_inline_buttons(categories),
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

    await callback.message.answer(
        text="Mahsulotni tanlang:",
        reply_markup=products_inline_buttons(products),
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

    caption = (
        f"*{name}*\n\n"
        f"💰 Narxi: *{price} so'm*\n\n"
        f"📝 {description}"
    )

    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer_photo(
        photo=image_id,
        caption=caption,
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
        text="Asosiy menyu:",
        reply_markup=start_inline_buttons(),
    )
    await callback.answer()