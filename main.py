import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


DATA_FILE = "grocery_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

class GroceryItem(BoxLayout):
    def __init__(self, item, index, refresh_callback, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=40, **kwargs)
        self.item = item
        self.index = index
        self.refresh_callback = refresh_callback

        self.add_widget(Label(text=item["name"], size_hint_x=0.3))
        self.add_widget(Label(text=f'₹{item["price_per_kg"]}/kg', size_hint_x=0.3))
        self.add_widget(Label(text=f'{item["quantity"]}kg', size_hint_x=0.2))

        edit_btn = Button(text="Edit", size_hint_x=0.1, on_press=self.edit_item)
        del_btn = Button(text="Delete", size_hint_x=0.1, on_press=self.delete_item)

        self.add_widget(edit_btn)
        self.add_widget(del_btn)

    def edit_item(self, instance):
        self.popup = EditPopup(self.item, self.index, self.refresh_callback)
        self.popup.open()

    def delete_item(self, instance):
        data = load_data()
        data.pop(self.index)
        save_data(data)
        self.refresh_callback()

class EditPopup(Popup):
    def __init__(self, item=None, index=None, refresh_callback=None):
        super().__init__(title="Edit Item" if item else "Add Item", size_hint=(0.9, 0.6))
        self.index = index
        self.refresh_callback = refresh_callback
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.name_input = TextInput(text=item["name"] if item else "", hint_text="Item name", multiline=False)
        self.price_input = TextInput(text=str(item["price_per_kg"]) if item else "", hint_text="Price per kg", multiline=False, input_filter='float')
        self.qty_input = TextInput(text=str(item["quantity"]) if item else "", hint_text="Quantity (kg)", multiline=False, input_filter='float')

        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.price_input)
        self.layout.add_widget(self.qty_input)

        save_btn = Button(text="Save", size_hint_y=None, height=40)
        save_btn.bind(on_press=self.save_item)

        self.layout.add_widget(save_btn)
        self.content = self.layout

    def save_item(self, instance):
        name = self.name_input.text.strip()
        price = float(self.price_input.text or 0)
        qty = float(self.qty_input.text or 0)

        if name and price and qty:
            data = load_data()
            item = {"name": name, "price_per_kg": price, "quantity": qty}

            if self.index is not None:
                data[self.index] = item
            else:
                data.append(item)

            save_data(data)
            self.dismiss()
            if self.refresh_callback:
                self.refresh_callback()

class PriceFinder(Popup):
    def __init__(self):
        super().__init__(title="Price Finder", size_hint=(0.9, 0.7))
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.price_input = TextInput(hint_text="Price per kg", multiline=False, input_filter='float')
        self.amount_input = TextInput(hint_text="Enter ₹ or gram (like 30 or 400)", multiline=False, input_filter='float')

        self.result_label = Label(text="")

        calc_btn = Button(text="Calculate", size_hint_y=None, height=40)
        calc_btn.bind(on_press=self.calculate)

        self.layout.add_widget(self.price_input)
        self.layout.add_widget(self.amount_input)
        self.layout.add_widget(calc_btn)
        self.layout.add_widget(self.result_label)

        self.content = self.layout

    def calculate(self, instance):
        try:
            price = float(self.price_input.text)
            amount = float(self.amount_input.text)
        except:
            self.result_label.text = "Enter valid numbers!"
            return

        # Determine whether it’s ₹ or grams based on context
        if amount <= 1000:
            quantity = round((amount / price), 2)
            self.result_label.text = f"For ₹{amount}: give {quantity} kg"
        if amount <= 2000:
            rupees = round((price * amount) / 1000, 2)
            self.result_label.text += f"\nFor {amount}g: charge ₹{rupees}"

class GroceryApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical')

        top_layout = BoxLayout(size_hint_y=None, height=50)
        self.search_input = TextInput(hint_text="Search...", multiline=False)
        self.search_input.bind(text=self.refresh_items)

        add_btn = Button(text="Add")
        add_btn.bind(on_press=lambda x: EditPopup(refresh_callback=self.refresh_items).open())

        price_btn = Button(text="Price Finder")
        price_btn.bind(on_press=lambda x: PriceFinder().open())

        top_layout.add_widget(self.search_input)
        top_layout.add_widget(add_btn)
        top_layout.add_widget(price_btn)

        self.root_layout.add_widget(top_layout)

        self.scroll_view = ScrollView()
        self.items_layout = GridLayout(cols=1, size_hint_y=None)
        self.items_layout.bind(minimum_height=self.items_layout.setter('height'))

        self.scroll_view.add_widget(self.items_layout)
        self.root_layout.add_widget(self.scroll_view)

        self.refresh_items()
        return self.root_layout

    def refresh_items(self, *args):
        self.items_layout.clear_widgets()
        keyword = self.search_input.text.lower()
        data = load_data()

        for i, item in enumerate(data):
            if keyword in item["name"].lower():
                self.items_layout.add_widget(GroceryItem(item, i, self.refresh_items))

if __name__ == '__main__':
    GroceryApp().run()
