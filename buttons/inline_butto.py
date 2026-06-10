from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_inline_buttons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🍔 Menyu", callback_data="main_menu")
            ],
            [
                InlineKeyboardButton(text="🛒 Savatcha", callback_data="show_cart"),
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
            # Siz aytgan asosiy maxsulotlar tugmasi
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


def categories_inline_buttons(categories: list):
    inline_keyboard = []
    
    for cat_id, cat_name in categories:
        row = [InlineKeyboardButton(text=cat_name, callback_data=f"category_{cat_id}")]
        inline_keyboard.append(row)
        
    inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Ortga", callback_data="back_to_start")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def products_inline_buttons(products: list):
    inline_keyboard = []
    
    for prod_id, prod_name in products:
        row = [InlineKeyboardButton(text=prod_name, callback_data=f"product_{prod_id}")]
        inline_keyboard.append(row)
        
    inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Kategoriyalarga qaytish", callback_data="main_menu")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def product_detail_inline_buttons(category_id: int, quantity: int = 1):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📥 Savatga qo'shish", callback_data="add_to_cart")
            ],
            [
                InlineKeyboardButton(text="⬅️ Ortga", callback_data=f"category_{category_id}")
            ]
        ]
    )
    return keyboard