from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_inline_buttons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🍔 Menyu", callback_data="main_menu")
            ],
            [
                InlineKeyboardButton(text="🛒 Savatchamm)", callback_data="show_cart"),
                InlineKeyboardButton(text="ℹ️ Biz haqimizda", callback_data="about_us")
            ]
        ]
    )
    return keyboard


def operator_inline_buttons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📋 Yangi buyurtmalar", callback_data="view_orders")
            ],
            [
                InlineKeyboardButton(text="📦 Mahsulot", callback_data="manage_products")
            ],
            [
                InlineKeyboardButton(text="👥 Foydalanuvchilar (PDF)", callback_data="stats"),
                InlineKeyboardButton(text="📨 Xabar yuborish", callback_data="send_broadcast")
            ]
        ]
    )
    return keyboard


def operator_products_inline_buttons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Mahsulot qo'shish", callback_data="add_product"),
                InlineKeyboardButton(text="❌ Mahsulotni o'chirish", callback_data="delete_product")
            ],
            [
                InlineKeyboardButton(text="➕ Kategoriya qo'shish", callback_data="add_category")
            ],
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_operator_main")
            ]
        ]
    )
    return keyboard


# KATEGORIYALAR: Har qatorda 2 tadan chiroyli joylashadi
def categories_inline_buttons(categories: list):
    builder = InlineKeyboardBuilder()
    
    for cat_id, cat_name in categories:
        builder.add(InlineKeyboardButton(text=f"{cat_name}", callback_data=f"category_{cat_id}"))
    
    # Tugmalarni 2 tadan qilib tartiblaymiz
    builder.adjust(2)
    
    # Oxiriga Ortga tugmasini alohida qatorda qo'shamiz
    builder.row(InlineKeyboardButton(text="⬅️ Ortga", callback_data="back_to_start"))
    
    return builder.as_markup()


def products_inline_buttons(products: list):
    builder = InlineKeyboardBuilder()
    
    for prod_id, prod_name in products:
        builder.add(InlineKeyboardButton(text=f"{prod_name}", callback_data=f"product_{prod_id}"))
        
    builder.adjust(2)
    
    builder.row(InlineKeyboardButton(text="⬅️ Ortga", callback_data="main_menu"))
    
    return builder.as_markup()


def product_detail_inline_buttons(category_id: int, quantity: int = 1):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [ 
                InlineKeyboardButton(text="-", callback_data="minus"),
                InlineKeyboardButton(text="1", callback_data="son"),
                InlineKeyboardButton(text="+", callback_data="plus"),
            ],
            [
                InlineKeyboardButton(text="📥 Savatga qo'shish", callback_data="add_to_cart")
            ],
            [
                InlineKeyboardButton(text="⬅️ Ortga", callback_data=f"category_{category_id}")
            ]
        ]
    )
    return keyboard