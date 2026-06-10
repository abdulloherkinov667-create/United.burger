from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from State import AddCategoryState, AddProductState
from database import insert_category, insert_product, get_all_categories
from buttons.inline_butto import operator_inline_buttons, operator_products_inline_buttons
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
product_router = Router()


@product_router.callback_query(F.data == "manage_products")
async def show_product_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer(
        "📦 Mahsulotlarni boshqarish menyusi:",
        reply_markup=operator_products_inline_buttons()
    )


#----------------------kategorya qoshish jarayoni----------------------
@product_router.callback_query(F.data == "add_category")
async def start_add_category(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddCategoryState.waiting_for_name)
    await call.answer()

    await call.message.answer(
        "📂 **Yangi kategoriya nomini kiriting:**\n\n"
        "*Masalan: Burgerlar, Ichimliklar, Sneklar*"
    )


@product_router.message(AddCategoryState.waiting_for_name)
async def process_category_name(message: types.Message, state: FSMContext):
    cat_name = message.text.strip()

    if not cat_name:
        await message.answer("⚠️ Iltimos, kategoriya nomini to'g'ri yozing.")
        return

    await state.update_data(category_name=cat_name)

    # Keyingi steytga o'tamiz va rasm so'raymiz
    await state.set_state(AddCategoryState.waiting_for_image)
    await message.answer(
        f"📸 **Yaxshi! Endi '{cat_name}' kategoriyasi uchun rasm yuboring:**\n\n"
        "*(Rasm shaklida yuboring, fayl formatida emas)*"
    )


@product_router.message(AddCategoryState.waiting_for_image, F.photo)
async def process_category_image(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    user_data = await state.get_data()
    cat_name = user_data.get("category_name")
    muvaffaqiyatli = await insert_category(name=cat_name, image_path=photo_id)

    if muvaffaqiyatli:
        await message.answer(
            f"✅ **Muvaffaqiyatli saqlandi!**\n\n"
            f"📂 Kategoriya: **{cat_name}**\n"
            f"📸 Rasm muvaffaqiyatli biriktirildi.", reply_markup=operator_inline_buttons())
    else:
        await message.answer(
            f"⚠️ **Xatolik:** `{cat_name}` nomli kategoriya bazada allaqachon mavjud!"
        )
    await state.clear()

@product_router.message(AddCategoryState.waiting_for_image)
async def process_category_image_invalid(message: types.Message):
    await message.answer("⚠️ Iltimos, faqat rasm (photo) yuboring!")
#_________________________________________________________________

# ==================== ➕ MAHSULOT QO'SHISH BOSQICHLARI ====================

@product_router.callback_query(F.data == "cancel_product_add")
async def cancel_product_add(call: types.CallbackQuery, state: FSMContext):
    await state.clear() # FSM xotirasini tozalaymiz
    await call.message.edit_text("❌ **Mahsulot qo'shish jarayoni bekor qilindi.**")
    await call.answer()


@product_router.callback_query(F.data == "cancel_product_add")
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("❌ Mahsulot qo'shish bekor qilindi.")
    await call.message.delete()
    await call.answer()


@product_router.callback_query(F.data == "add_product")
async def start_add_product(call: types.CallbackQuery, state: FSMContext):
    categories = get_all_categories()
    if not categories:
        await call.message.answer("⚠️ Avval kategoriya yarating!")
        return

    await state.set_state(AddProductState.waiting_for_name)
    await call.message.answer("📝 **Mahsulot nomini kiriting:**")
    await call.answer()


@product_router.message(AddProductState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(p_name=message.text.strip())
    await state.set_state(AddProductState.waiting_for_price)
    await message.answer("💰 **Narxini kiriting (faqat raqam):**\n*Masalan: 23000*")


@product_router.message(AddProductState.waiting_for_price)
async def process_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Faqat raqam kiriting!")
        return
    
    price_num = int(message.text)
    formatted_price = f"{price_num:,}".replace(",", ".") 
    
    await state.update_data(p_price=formatted_price)
    await state.set_state(AddProductState.waiting_for_description)
    await message.answer(f"💰 Narx: {formatted_price} so'm\n\nℹ️ **Mahsulot tarkibini kiriting:**\n*(Vergul bilan ajratib yozing)*")


@product_router.message(AddProductState.waiting_for_description)
async def process_desc(message: types.Message, state: FSMContext):
    raw_desc = message.text.strip()
    # Avtomatik ro'yxatga aylantirish
    items = [f"▪️ {i.strip().capitalize()}" for i in raw_desc.split(",") if i.strip()]
    beautiful_desc = "\n".join(items)
    
    await state.update_data(p_desc=beautiful_desc)
    await state.set_state(AddProductState.waiting_for_image)
    await message.answer(f"📝 Tarkibi:\n{beautiful_desc}\n\n🖼 **Endi rasm yuboring:**")


@product_router.message(AddProductState.waiting_for_image, F.photo)
async def process_image(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(p_image=photo_id)
    
    categories = get_all_categories()
    kb = []
    for c_id, c_name in categories:
        kb.append([InlineKeyboardButton(text=f"📁 {c_name}", callback_data=f"save_cat_{c_id}")])
    
    kb.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_product_add")])
    await state.set_state(AddProductState.waiting_for_category)
    await message.answer("📁 **Qaysi kategoriyaga qo'shamiz?**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))


@product_router.callback_query(AddProductState.waiting_for_category, F.data.startswith("save_cat_"))
async def final_save(call: types.CallbackQuery, state: FSMContext):
    cat_id = int(call.data.split("_")[2])
    data = await state.get_data()
    
    insert_product(
        category_id=cat_id,
        name=data['p_name'],
        price=data['p_price'],
        description=data['p_desc'],
        image_id=data['p_image']
    )
    
    caption_text = (
        f"✅ **Mahsulot qo'shildi!**\n\n"
        f"ℹ️ **Tarkibi:**\n{data['p_desc']}\n\n"  
        f"🍔 **{data['p_name']}**\n"               
        f"💰 Narxi: **{data['p_price']} so'm**"     
    )
    
    await call.message.answer_photo(
        photo=data['p_image'],
        caption=caption_text
    )
    
    await call.message.delete()
    await state.clear()
    await call.answer()