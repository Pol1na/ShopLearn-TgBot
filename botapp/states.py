from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    main = State()

    class PersonalCab(StatesGroup):
        main = State()

        class EditData(StatesGroup):
            name = State()
            address = State()
            phone = State()

    class Order(StatesGroup):
        main = State()

        class CreateData(StatesGroup):
            name = State()
            address = State()
            phone = State()
            accept = State()
            decline = State()


class Admin(StatesGroup):
    main = State()

    class EditProduct(StatesGroup):
        product_id = State()
        name = State()
        desc = State()
        price = State()
        photo = State()

    class AddProduct(StatesGroup):
        category_id = State()
        name = State()
        desc = State()
        price = State()
        photo = State()

    class AddCategory(StatesGroup):
        parent_id = State()
        name = State()

    class AddMainCategory(StatesGroup):
        parent_id = State()
        name = State()
